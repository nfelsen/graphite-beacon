graphite-beacon
===============

![logo](https://raw.github.com/klen/graphite-beacon/develop/beacon.png)

Simple allerting system for [Graphite](http://graphite.wikidot.com/) metrics.

Features:

- Simplest installation (one python package dependency);
- No software dependencies (Databases, AMPQ and etc);
- Light and full asyncronous;
- SMTP, Hipchat handlers (Please make a request for additional handlers);

[![Build status](http://img.shields.io/travis/klen/graphite-beacon.svg?style=flat-square)](http://travis-ci.org/klen/graphite-beacon)
[![Coverage](http://img.shields.io/coveralls/klen/graphite-beacon.svg?style=flat-square)](https://coveralls.io/r/klen/graphite-beacon)
[![Donate](http://img.shields.io/gratipay/klen.svg?style=flat-square)](https://www.gratipay.com/klen/)


Requirements
------------

- python (2.7, 3.3, 3.4)
- tornado

Installation
------------

### Python package

**Graphite-beacon** could be installed using pip:

    pip intall graphite-beacon

### Debian package

TODO

Usage
-----

Just run `graphite-beacon`:

    $ graphite-beacon
    [I 141025 11:16:23 core:141] Read configuration
    [I 141025 11:16:23 core:55] Memory (10minute): init
    [I 141025 11:16:23 core:166] Loaded with options:
    ...

### Configuration

**Graphite-beacon** default options are:

> Comment lines are not allowed in real JSON!

```js

    {
        // Path to a configuration
        "config": "config.json",

        // Graphite server URL
        "graphite_url": "http://localhost",

        // HTTP AUTH username
        "graphite_user": null,

        // HTTP AUTH password
        "graphite_password": null,

        // Path to a pidfile
        "pidfile": null,

        // Default query interval
        // Can be redfined for each alert.
        "interval": "10minute",

        // Default loglevel
        "logging": "info",

        // Default method (average, last_value).
        // Can be redfined for each alert.
        "method": "average",

        // Default prefix (used for notifications)
        "prefix": "[BEACON]",

        // Default handlers (log, smtp, hipchat)
        "critical_handlers": ["log", "smtp"],
        "warning_handlers": ["log", "smtp"],
        "normal_handlers": ["log", "smtp"],

        // Default alerts (see configuration below)
        "alerts": []
    }
```

You can setup options with a configuration file. See
`example-config.json`.

### Setup alerts

> Comment lines are not allowed in real JSON!

```js

  "alerts": [
    {
      // Alert name (required)
      "name": "Memory",

      // Alert query (required)
      "query": "*.memory.memory-free",

      // Alert method (optional)
      "method": "average",

      // Alert interval (optional)
      "interval": "1minute",

      // Alert rules
      "rules": [
        {
          // Level
          "level": "critical",
          // Conditional (gt (>), ge (>=), lt (<), le (<=), eq (==))
          "operator": "gt",

          // Value to compare
          "value": 80
        },
        {
          "level": "warning",
          "operator": "gt",
          "value": 60
        }
      ]
    }
  ]
```

### Command line

```
  $ graphite-beacon --help
  Usage: graphite-beacon [OPTIONS]

  Options:

    --config                         Path to an configuration file (YAML)
                                    (default config.json)
    --graphite_url                   Graphite URL (default http://localhost)
    --help                           show this help information
    --pidfile                        Set pid file

    --log_file_max_size              max size of log files before rollover
                                    (default 100000000)
    --log_file_num_backups           number of log files to keep (default 10)
    --log_file_prefix=PATH           Path prefix for log files. Note that if you
                                    are running multiple tornado processes,
                                    log_file_prefix must be different for each
                                    of them (e.g. include the port number)
    --log_to_stderr                  Send log output to stderr (colorized if
                                    possible). By default use stderr if
                                    --log_file_prefix is not set and no other
                                    logging is configured.
    --logging=debug|info|warning|error|none
                                    Set the Python log level. If 'none', tornado
                                    won't touch the logging configuration.
                                    (default info)
```

Bug tracker
-----------

If you have any suggestions, bug reports or annoyances please report them to
the issue tracker at https://github.com/klen/graphite-beacon/issues

Contributors
-------------

* Kirill Klenov     (https://github.com/klen, horneds@gmail.com)

License
--------

Licensed under a [MIT license](http://www.linfo.org/mitlicense.html)