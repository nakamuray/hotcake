# vim: fileencoding=utf-8
import base64

from twisted.web import proxy, http

# TODO: access log
# TODO: CONNECT


class AuthorizedProxy(proxy.Proxy):
    username = None
    password = None

    def __init__(self, username, password, *args, **kwargs):
        proxy.Proxy.__init__(self, *args, **kwargs)

        self.username = username
        self.password = password

    def allContentReceived(self):
        if not self.authenticated():
            # XXX: should I do this on Request class?
            self.transport.write(
                b'HTTP/1.1 407 Proxy Authentication Required\r\n\r\n')
            self.transport.loseConnection()
            return

        return proxy.Proxy.allContentReceived(self)

    def authenticated(self):
        if not self.username:
            return True

        # Authorization, (mostly) per the RFC
        try:
            req = self.requests[-1]

            authh = req.getHeader(b"Proxy-Authorization")
            req.requestHeaders.removeHeader(b'Proxy-Authorization')

            if not authh:
                return False

            bas, upw = authh.split()

            if bas.lower() != b"basic":
                return False

            upw = base64.decodestring(upw)
            user, password = upw.split(b':', 1)

            return user == self.username and password == self.password
        except:
            from twisted.python import log
            log.err()
            return False


class HttpProxyFactory(http.HTTPFactory):
    def __init__(self, username, password, *args, **kwargs):
        self.username = username
        self.password = password

        http.HTTPFactory.__init__(self, *args, **kwargs)

    def buildProtocol(self, addr):
        return AuthorizedProxy(self.username, self.password)
