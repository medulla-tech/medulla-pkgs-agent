#! /usr/bin/python
# -*- coding: utf-8; -*-
# (c) 2016 Siveo, http://www.siveo.net
# $Id$
#
# This file is part of Mandriva Management Console (MMC).
#
# MMC is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# MMC is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with MMC.  If not, see <http://www.gnu.org/licenses/>.
from twisted.web import xmlrpc, server
from twisted.internet import defer
import xmlrpclib
import logging

try:
    from twisted.web import http
except ImportError:
    from twisted.protocols import http  # pyflakes.ignore

logger = logging.getLogger()


Fault = xmlrpclib.Fault

class TwistedRPCServer(xmlrpc.XMLRPC):
    """ A class which works as an XML-RPC server with
    HTTP basic authentication """

    def __init__(self, user='', password=''):
        self._user = user
        self._password = password
        self._auth = (self._user !='')
        xmlrpc.XMLRPC.__init__(self)

    def echo(self, x):
        """Return all passed args."""
        return x

    def xmlrpc_ping(self):
        return 'OK'

    def xmlrpc_echo(self, x):
        """Return all passed args."""
        return x

    def xmlrpc_add(self, a, b):
        """Return sum of arguments."""
        return a + b

    def render(self, request):
        """ Overridden 'render' method which takes care of
        HTTP basic authorization """

        if self._auth:
            cleartext_token = self._user + ':' + self._password
            user = request.getUser()
            passwd = request.getPassword()
        
            if user=='' and passwd=='':
                request.setResponseCode(http.UNAUTHORIZED)
                return 'Authorization required!'
            else:
                token = user + ':' + passwd
                if token != cleartext_token:
                    request.setResponseCode(http.UNAUTHORIZED)
                    return 'Authorization Failed!'
        request.content.seek(0, 0)
        args, functionPath = xmlrpclib.loads(request.content.read())
        try:
            #function = self._getFunction(functionPath)
            function = self.lookupProcedure(functionPath)
        except Fault, f:
            self._cbRender(f, request)
        else:
            request.setHeader("content-type", "text/xml")
            defer.maybeDeferred(function, *args).addErrback(
                self._ebRender
                ).addCallback(
                self._cbRender, request
                )

        return server.NOT_DONE_YET
