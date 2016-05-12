# vim: fileencoding=utf-8
import click

from twisted.internet import reactor

from .http import HttpProxyFactory
from .ssh import SshProxyFactory


@click.command()
@click.option('--username')
@click.option('--password')
@click.option('--http-port', type=int, default=8080)
@click.option('--ssh-port', type=int, default=8022)
@click.option('--ssh-data-dir', default='/etc/ssh')
def run(username, password, http_port, ssh_port, ssh_data_dir):
    reactor.listenTCP(http_port, HttpProxyFactory(username, password))
    reactor.listenTCP(
        ssh_port,
        SshProxyFactory(username, password, ssh_data_dir, ssh_data_dir),
    )
    reactor.run()


def _setup_logger():
    import sys

    from twisted import logger

    logger.globalLogPublisher.addObserver(
        logger.textFileLogObserver(sys.stderr))


def main():
    _setup_logger()

    run(auto_envvar_prefix='HOTCAKE')


if __name__ == '__main__':
    main()
