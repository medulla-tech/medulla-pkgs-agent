#! /usr/bin/python
# -*- coding: utf-8; -*-
# (c) 2016-2020 Siveo, http://www.siveo.net
# $Id$
#
# This file is part of Management Console (MMC).
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

        self.port = 7081
        if Config.has_option("xmlrpc", "port"):
            self.port = Config.getint('xmlrpc',
                                      'port')


        self.host = "localhost"
        if Config.has_option("xmlrpc", "host"):
            self.host = Config.get('xmlrpc',
                                   'host')

        self.timeoutheader = 15
        if Config.has_option("xmlrpc", "timeoutheader"):
            self.host = Config.get('xmlrpc',
                                   'timeoutheader')

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

        # activate connection to base module
        self.plugins_list = ["xmpp", "pkgs"]
        if Config.has_option("global", "activate_plugin"):
            listplugsql = Config.get('global', 'activate_plugin')
            self.plugins_list = [x.strip().lower() for x in listplugsql.split(",") if x.strip() != ""]

        if "glpi" in self.plugins_list:
            self.readConfglpi(Config)

        if "xmpp" in self.plugins_list:
            self.readConfxmpp(Config)

        if "kiosk" in self.plugins_list:
            self.readConfkiosk(Config)

        if "msc" in self.plugins_list:
            self.readConfmsc(Config)

        if "pkgs" in self.plugins_list:
            self.readConfpkgs(Config)



    def readConfkiosk(self, confiobject):
        self.kiosk_dbhost = "localhost"
        if confiobject.has_option("kioskdatabase", "kiosk_dbhost"):
            self.kiosk_dbhost = confiobject.get('kioskdatabase', 'kiosk_dbhost')

        self.kiosk_dbport = "3306"
        if confiobject.has_option("kioskdatabase", "kiosk_dbport"):
            self.kiosk_dbport = confiobject.get('kioskdatabase', 'kiosk_dbport')

        self.kiosk_dbname = "kiosk"
        if confiobject.has_option("kioskdatabase", "kiosk_dbname"):
            self.kiosk_dbname = confiobject.get('kioskdatabase', 'kiosk_dbname')

        self.kiosk_dbuser = "mmc"
        if confiobject.has_option("kioskdatabase", "kiosk_dbuser"):
            self.kiosk_dbuser = confiobject.get('kioskdatabase', 'kiosk_dbuser')

        self.kiosk_dbpasswd = "mmc"
        if confiobject.has_option("kioskdatabase", "kiosk_dbpasswd"):
            self.kiosk_dbpasswd = confiobject.get('kioskdatabase', 'kiosk_dbpasswd')

    def readConfmsc(self, confiobject):
        self.msc_dbpooltimeout = 30
        if confiobject.has_option("mscdatabase", "msc_dbpooltimeout"):
            self.msc_dbpooltimeout = confiobject.getint('mscdatabase', 'msc_dbpooltimeout')
        self.msc_dbhost = "localhost"
        if confiobject.has_option("mscdatabase", "msc_dbhost"):
            self.msc_dbhost = confiobject.get('mscdatabase', 'msc_dbhost')

        self.msc_dbport = "3306"
        if confiobject.has_option("mscdatabase", "msc_dbport"):
            self.msc_dbport = confiobject.get('mscdatabase', 'msc_dbport')

        self.msc_dbname = "msc"
        if confiobject.has_option("mscdatabase", "msc_dbname"):
            self.msc_dbname = confiobject.get('mscdatabase', 'msc_dbname')

        self.msc_dbuser = "mmc"
        if confiobject.has_option("mscdatabase", "msc_dbuser"):
            self.msc_dbuser = confiobject.get('mscdatabase', 'msc_dbuser')

        self.msc_dbpasswd = "mmc"
        if confiobject.has_option("mscdatabase", "msc_dbpasswd"):
            self.msc_dbpasswd = confiobject.get('mscdatabase', 'msc_dbpasswd')

    def readConfpkgs(self, confiobject):
        self.pkgs_dbpooltimeout = 30
        if confiobject.has_option("pkgsdatabase", "pkgs_dbpooltimeout"):
            self.pkgs_dbpooltimeout = confiobject.getint('pkgsdatabase', 'pkgs_dbpooltimeout')
        self.pkgs_dbhost = "localhost"
        if confiobject.has_option("pkgsdatabase", "pkgs_dbhost"):
            self.pkgs_dbhost = confiobject.get('pkgsdatabase', 'pkgs_dbhost')

        self.pkgs_dbport = "3306"
        if confiobject.has_option("pkgsdatabase", "pkgs_dbport"):
            self.pkgs_dbport = confiobject.get('pkgsdatabase', 'pkgs_dbport')

        self.pkgs_dbname = "pkgs"
        if confiobject.has_option("pkgsdatabase", "pkgs_dbname"):
            self.pkgs_dbname = confiobject.get('pkgsdatabase', 'pkgs_dbname')

        self.pkgs_dbuser = "mmc"
        if confiobject.has_option("pkgsdatabase", "pkgs_dbuser"):
            self.pkgs_dbuser = confiobject.get('pkgsdatabase', 'pkgs_dbuser')

        self.pkgs_dbpasswd = "mmc"
        if confiobject.has_option("pkgsdatabase", "pkgs_dbpasswd"):
            self.pkgs_dbpasswd = confiobject.get('pkgsdatabase', 'pkgs_dbpasswd')

        self.pkgs_dbpoolrecycle = 5
        if confiobject.has_option("pkgsdatabase", "pkgs_dbpoolrecycle"):
            self.pkgs_dbpoolrecycle = confiobject.get('pkgsdatabase', 'pkgs_dbpoolrecycle')

        self.pkgs_dbpoolsize = 60
        if confiobject.has_option("pkgsdatabase", "pkgs_dbpoolsize"):
            self.pkgs_dbpoolsize = confiobject.get('pkgsdatabase', 'pkgs_dbpoolsize')
    def readConfxmpp(self, confiobject):
        self.xmpp_dbhost = "localhost"
        if confiobject.has_option("xmppdatabase", "xmpp_dbhost"):
            self.xmpp_dbhost = confiobject.get('xmppdatabase', 'xmpp_dbhost')

        self.xmpp_dbport = "3306"
        if confiobject.has_option("xmppdatabase", "xmpp_dbport"):
            self.xmpp_dbport = confiobject.get('xmppdatabase', 'xmpp_dbport')

        self.xmpp_dbname = "xmppmaster"
        if confiobject.has_option("xmppdatabase", "xmpp_dbname"):
            self.xmpp_dbname = confiobject.get('xmppdatabase', 'xmpp_dbname')

        self.xmpp_dbuser = "mmc"
        if confiobject.has_option("xmppdatabase", "xmpp_dbuser"):
            self.xmpp_dbuser = confiobject.get('xmppdatabase', 'xmpp_dbuser')

        self.xmpp_dbpasswd = "mmc"
        if confiobject.has_option("xmppdatabase", "xmpp_dbpasswd"):
            self.xmpp_dbpasswd = confiobject.get('xmppdatabase', 'xmpp_dbpasswd')

        self.xmpp_dbpoolrecycle = 5
        if confiobject.has_option("xmppdatabase","xmpp_dbpoolrecycle"):
            self.xmpp_dbpoolrecycle = confiobject.get('xmppdatabase', 'xmpp_bdpoolrecycle')

        self.xmpp_dbpoolsize = 60
        if confiobject.has_option("xmppdatabase", "xmpp_dbpoolsize"):
            self.xmpp_dbpoolsize = confiobject.get('xmppdatabase', 'xmpp_dbpoolsize')

    def readConfglpi(self, confiobject):
        self.inventory_url = "http://localhost:9999/"
        if confiobject.has_option("glpi", "inventory_server_url"):
            self.inventory_url = confiobject.get('glpi', 'inventory_server_url')

        #Configuration sql
        #configuration glpi
        self.glpi_dbhost = "localhost"
        if confiobject.has_option("glpidatabase", "glpi_dbhost"):
            self.glpi_dbhost = confiobject.get('glpidatabase', 'glpi_dbhost')

        self.glpi_dbport = "3306"
        if confiobject.has_option("glpidatabase", "glpi_dbport"):
            self.glpi_dbport = confiobject.get('glpidatabase', 'glpi_dbport')

        self.glpi_dbname = "glpi"
        if confiobject.has_option("glpidatabase", "glpi_dbname"):
            self.glpi_dbname = confiobject.get('glpidatabase', 'glpi_dbname')

        self.glpi_dbuser = "mmc"
        if confiobject.has_option("glpidatabase", "glpi_dbuser"):
            self.glpi_dbuser = confiobject.get('glpidatabase', 'glpi_dbuser')

        self.glpi_dbpasswd = "mmc"
        if confiobject.has_option("glpidatabase", "glpi_dbpasswd"):
            self.glpi_dbpasswd = confiobject.get('glpidatabase', 'glpi_dbpasswd')

        try:
            self.activeProfiles = confiobject.get('glpi', 'active_profiles').split(' ')
        except:
            # put the GLPI default values for actives profiles
            logging.getLogger().warn("Apply default parameters for GLPI active profiles")
            self.activeProfiles = ['Super-Admin', 'Admin', 'Supervisor', 'Technician']

        self.ordered = 1
        if confiobject.has_option("computer_list", "ordered"):
            self.ordered = confiobject.getint("computer_list", "ordered")


        filter = "state="
        if confiobject.has_option("glpi", "filter_on"):
            filter = confiobject.get("glpi", "filter_on")
        self.filter_on = self._parse_filter_on(filter)

        self.orange = 10
        self.red = 35
        if confiobject.has_option("state", "orange"):
            self.orange = confiobject.getint("state", "orange")
        if confiobject.has_option("state", "red"):
            self.red = confiobject.getint("state", "red")

        self.summary = ['cn', 'description', 'os', 'type', 'user', 'entity']
        if confiobject.has_option("computer_list", "summary"):
            self.summary = confiobject.get("computer_list", "summary").split(' ')

        self.av_false_positive = []
        if confiobject.has_option("antivirus", "av_false_positive"):
            self.av_false_positive = confiobject.get("antivirus", "av_false_positive").split('||')

        # associate manufacturer's names to their warranty url
        # manufacturer must have same key in 'manufacturer' and 'manufacturer_warranty_url' sections
        # for adding its warranty url
        self.manufacturerWarranty = {}
        if '' in confiobject.sections():
            logging.getLogger().debug('[GLPI] Get manufacturers and their warranty infos')
            for manufacturer_key in confiobject.options('manufacturers'):
                if confiobject.has_section('manufacturer_' + manufacturer_key) and confiobject.has_option('manufacturer_' + manufacturer_key, 'url'):
                    try:
                        type = confiobject.get('manufacturer_' + manufacturer_key, 'type')
                    except NoOptionError:
                        type = "get"
                    try:
                        params = confiobject.get('manufacturer_' + manufacturer_key, 'params')
                    except NoOptionError:
                        params = ""
                    self.manufacturerWarranty[manufacturer_key] = {'names': confiobject.get('manufacturers', manufacturer_key).split('||'),
                                                                   'type': type,
                                                                   'url': confiobject.get('manufacturer_' + manufacturer_key, 'url'),
                                                                   'params': params}
            logging.getLogger().debug(self.manufacturerWarranty)
