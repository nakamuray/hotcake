# vim: fileencoding=utf-8
from twisted.conch import avatar
from twisted.conch.ssh import forwarding, session
from twisted.conch.openssh_compat import factory
from twisted.cred import checkers, portal
from twisted.python import components
from zope.interface import implementer


class ProxyUser(avatar.ConchUser):
    def __init__(self, username):
        avatar.ConchUser.__init__(self)

        self.username = username
        self.channelLookup.update({
            'session': session.SSHSession,
            'direct-tcpip': forwarding.openConnectForwardingClient,
        })


@implementer(portal.IRealm)
class Realm(object):
    def requestAvatar(self, avatarId, mind, *interfaces):
        return interfaces[0], ProxyUser(avatarId), lambda: None


class Session(object):
    def __init__(self, avatar):
        pass

    def getPty(self, term, windowSize, attrs):
        pass

    def execCommand(self, proto, cmd):
        raise Exception('not executing commands')

    def openShell(self, transport):
        raise Exception('not opening shells')

    def eofReceived(self):
        pass

    def closed(self):
        pass


components.registerAdapter(Session, ProxyUser, session.ISession)


class SshProxyFactory(factory.OpenSSHFactory):
    def __init__(self, username, password,
                 dataRoot='/etc/ssh', moduliRoot='/etc/ssh'):
        self.dataRoot = dataRoot
        self.moduliRoot = moduliRoot

        self.portal = portal.Portal(Realm())

        passwdDB = checkers.InMemoryUsernamePasswordDatabaseDontUse()
        passwdDB.addUser(username, password)
        self.portal.registerChecker(passwdDB)
