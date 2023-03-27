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
from plugins.xmpp import XmppMasterDatabase

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
        return PkgsDatabase().get_shares()

    def xmlrpc_pkgs_sharing_rule_search(self, loginname, type="local"):
        return PkgsDatabase().pkgs_sharing_rule_search(loginname)

    def xmlrpc_xmpp_packages_list(self, path):
        """
        Create a list of xmpp packages and return the list and the information for each of them
        Params:
            path string of the packages directory path
        Returns:
        list of packages
        """

        # path = _path_package()

        # 1 - list the packages directories
        if not os.path.isdir(path):
            return []
        list_all = os.listdir(path)
        xmpp_list = []

        for dirname in list_all:
            # 2 - if the directory contains xmppdeploy.json
            if os.path.isfile(os.path.join(path, dirname, 'xmppdeploy.json')) is True:
                # 3 - Extracts the package information and add it to the package list
                #json_content = json.load(file(path+'/'+dirname+'/xmppdeploy.json'))
                json_content = json.load(file(os.path.join(path, dirname, 'xmppdeploy.json')))
                json_content['info']['uuid'] = dirname;
                xmpp_list.append(json_content['info'])
        return xmpp_list
