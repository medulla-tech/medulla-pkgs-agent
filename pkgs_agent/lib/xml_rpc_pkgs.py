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

import time
from twisted.web import xmlrpc
import logging

logger = logging.getLogger()


class pkgsxmlrpc(xmlrpc.XMLRPC):
    """Serve the XML-RPC 'time' method."""
    def xmlrpc_time(self):
        """Return UNIX time."""
        return time.time()

    def xmlrpc_test(self):
        """Return text testUNIX time."""
        return "test"
    # fonction declare en rpc
    
    
    
#class Example(xmlrpc.XMLRPC):
    #"""An example object to be published."""

    #def xmlrpc_echo(self, x):
        #"""Return all passed args."""
        #return x

    #def xmlrpc_add(self, a, b):
        #"""Return sum of arguments."""
        #return a + b

#class Date(xmlrpc.XMLRPC):
    #"""Serve the XML-RPC 'time' method."""
    #def xmlrpc_time(self):
        #"""Return UNIX time."""
        #return time.time()
