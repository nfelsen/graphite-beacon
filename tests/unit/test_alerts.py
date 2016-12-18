import mock

from graphite_beacon.alerts import BaseAlert, GraphiteAlert, URLAlert


def test_alert(reactor):
    alert1 = BaseAlert.get(reactor, name='Test', query='*', rules=["normal: == 0"])
    assert alert1
    assert isinstance(alert1, GraphiteAlert)

    alert2 = BaseAlert.get(reactor, name='Test', query='*', source='url', rules=["normal: == 0"])
    assert isinstance(alert2, URLAlert)

    assert alert1 != alert2

    alert3 = BaseAlert.get(reactor, name='Test', query='*', interval='2m', rules=["normal: == 0"])
    assert alert3.interval == '2minute'

    assert alert1 == alert3
    assert set([alert1, alert3]) == set([alert1])

    alert = BaseAlert.get(reactor, name='Test', query='*', rules=["warning: >= 3MB"])
    assert alert.rules[0]['exprs'][0]['value'] == 3145728


def test_multimetrics(reactor):
    alert = BaseAlert.get(
        reactor, name="Test", query="*", rules=[
            "critical: > 100", "warning: > 50", "warning: < historical / 2"])
    reactor.alerts = set([alert])

    with mock.patch.object(reactor, 'notify'):
        alert.check([(110, 'metric1'), (60, 'metric2'), (30, 'metric3')])

        assert reactor.notify.call_count == 2

        # metric1 - critical
        assert reactor.notify.call_args_list[0][0][0] == 'critical'
        assert reactor.notify.call_args_list[0][1]['target'] == 'metric1'

        # metric2 - warning
        assert reactor.notify.call_args_list[1][0][0] == 'warning'
        assert reactor.notify.call_args_list[1][1]['target'] == 'metric2'

    assert list(alert.history['metric1']) == [110]

    with mock.patch.object(reactor, 'notify'):
        alert.check([(60, 'metric1'), (60, 'metric2'), (30, 'metric3')])
        assert reactor.notify.call_count == 1

        # metric1 - warning, metric2 didn't change
        assert reactor.notify.call_args_list[0][0][0] == 'warning'
        assert reactor.notify.call_args_list[0][1]['target'] == 'metric1'

    assert list(alert.history['metric1']) == [110, 60]

    with mock.patch.object(reactor, 'notify'):
        alert.check([(60, 'metric1'), (30, 'metric2'), (105, 'metric3')])
        assert reactor.notify.call_count == 2

        # metric2 - normal
        assert reactor.notify.call_args_list[0][0][0] == 'normal'
        assert reactor.notify.call_args_list[0][1]['target'] == 'metric2'

        # metric3 - critical
        assert reactor.notify.call_args_list[1][0][0] == 'critical'
        assert reactor.notify.call_args_list[1][1]['target'] == 'metric3'

    assert list(alert.history['metric1']) == [110, 60, 60]

    with mock.patch.object(reactor, 'notify'):
        alert.check([(60, 'metric1'), (30, 'metric2'), (105, 'metric3')])
        assert reactor.notify.call_count == 0

    with mock.patch.object(reactor, 'notify'):
        alert.check([(70, 'metric1'), (21, 'metric2'), (105, 'metric3')])
        assert reactor.notify.call_count == 1

        # metric2 - historical warning
        assert reactor.notify.call_args_list[0][0][0] == 'warning'
        assert reactor.notify.call_args_list[0][1]['target'] == 'metric2'

    assert list(alert.history['metric1']) == [60, 60, 60, 70]
    assert alert.state['metric1'] == 'warning'

    reactor.repeat()

    assert alert.state == {
        None: 'normal', 'metric1': 'normal', 'metric2': 'normal', 'metric3': 'normal',
        'waiting': 'normal', 'loading': 'normal'}


def test_multiexpressions(reactor):
    alert = BaseAlert.get(
        reactor, name="Test", query="*", rules=["warning: > historical * 1.05 AND > 70"])
    reactor.alerts = set([alert])

    with mock.patch.object(reactor, 'notify'):
        alert.check([
            (50, 'metric1'), (65, 'metric1'), (85, 'metric1'), (65, 'metric1'),
            (68, 'metric1'), (75, 'metric1')])

        assert reactor.notify.call_count == 1

        # metric2 - warning
        assert reactor.notify.call_args_list[0][0][0] == 'warning'
        assert reactor.notify.call_args_list[0][1]['target'] == 'metric1'

    assert list(alert.history['metric1']) == [85, 65, 68, 75]