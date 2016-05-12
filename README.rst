hotcake -- HTTP and SSH proxy server
====================================

hotcake is proxy server supporting HTTP and SSH (port forwarding, SOCKS) protocols.


Usage
-----

::

  Usage: hotcake [OPTIONS]

  Options:
    --username TEXT
    --password TEXT
    --http-port INTEGER
    --ssh-port INTEGER
    --ssh-data-dir TEXT
    --help               Show this message and exit.


.. NOTE::

  Options could be set through environment variables.
  Use upper case option name prefixed with ``HOTCAKE_``,
  such as ``HOTCAKE_USERNAME`` or ``HOTCAKE_HTTP_PORT``.
