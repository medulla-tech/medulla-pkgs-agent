#!/usr/bin/python3
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
from plugins.pkgs import PkgsDatabase

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

    def xmlrpc_get_shares(self):
        result = PkgsDatabase().get_shares()
        return result
