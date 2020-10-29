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

import os
import ConfigParser
import logging

logger = logging.getLogger()

class SingletonDecorator:
    def __init__(self, klass):
        self.klass = klass
        self.instance = None

    def __call__(self, *args, **kwds):
        if self.instance == None:
            self.instance = self.klass(*args, **kwds)
        return self.instance

@SingletonDecorator
class confParameter:
    def __init__(self, dft_inifile):
        self.dft_inifile = dft_inifile
        Config = ConfigParser.ConfigParser()
        Config.read(self.dft_inifile)
        if os.path.exists(self.dft_inifile + ".local"):
            Config.read(self.dft_inifile + ".local")    

        if Config.has_option("xmlrpc", "user"):
            self.user = Config.get('xmlrpc',
                                   'user')
        else:
            self.user = "user"
        if Config.has_option("xmlrpc", "password"):
            self.password = Config.get('xmlrpc',
                                       'password')
        else:
            self.password = "password"

        self.dir_keys_pen = "/home/jfk/script/agent_xmlrpc/keys/"

        if Config.has_option("xmlrpc", "dir_keys_pen"):
            self.dir_keys_pen = Config.get('xmlrpc',
                                           'dir_keys_pen')

        self.enablessl = True
        if Config.has_option("xmlrpc", "enablessl"):
            self.enablessl = Config.getboolean('xmlrpc',
                                               'enablessl')

        self.localcert = "privkey.pem"
        if Config.has_option("xmlrpc", "localcert"):
            self.localcert = Config.get('xmlrpc',
                                        'localcert')
        self.localcert = os.path.join(self.dir_keys_pen,
                                      self.localcert)

        self.cacert ="cacert.pem"
        if Config.has_option("xmlrpc", "cacert"):
            self.cacert = Config.get('xmlrpc',
                                     'cacert')
        self.cacert = os.path.join(self.dir_keys_pen,
                                      self.cacert)

        self.verifypeer = False
        if Config.has_option("xmlrpc", "verifypeer"):
            self.verifypeer = Config.getboolean('xmlrpc',
                                                'verifypeer')

        self.port = 7080
        if Config.has_option("xmlrpc", "port"):
            self.host = Config.getint('xmlrpc',
                                      'port')

        self.host = "localhost"
        if Config.has_option("xmlrpc", "host"):
            self.host = Config.get('xmlrpc',
                                   'host')
 
        self.log_level = "INFO"
        if Config.has_option("global", "log_level"):
            self.log_level = Config.get('global',
                                        'log_level')

        self.logfile = "/var/log/pkgs/pkgs_agent.log" 
        if Config.has_option("global", "logfile"):
            self.logfile = Config.get('global',
                                      'logfile')

        if self.log_level.upper() == "CRITICAL":
            self.log_level = 50
        elif self.log_level.upper() == "ERROR":
            self.log_level = 40
        elif self.log_level.upper() == "WARNING":
            self.log_level = 30
        elif self.log_level.upper() == "INFO":
            self.log_level = 20
        elif self.log_level.upper() == "DEBUG":
            self.log_level = 10
        elif self.log_level.upper() == "NOTSET":
            self.log_level = 0
        else:
            self.log_level = 20
