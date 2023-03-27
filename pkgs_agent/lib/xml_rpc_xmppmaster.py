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

# file : pulse_pkgs_agent/lib/xml_rpc_xmppmaster.py

import time
from twisted.web import xmlrpc
from plugins.xmpp import XmppMasterDatabase
from plugins.pkgs import PkgsDatabase
import logging
import json
from random import randint

logger = logging.getLogger()

class xmlrpc_function_xmppmaster(Exception):
    """
    Exception reverve pour les function xmlrpc
    """

    def __init__(self, msg, f=""):
        Exception.__init__(self, msg)
        self.msg = msg
        self.f = f

    def __str__(self):
        return "exception fonction {0} \n: {1}".format(self.f, self.msg)


class xmppmasterxmlrpc(xmlrpc.XMLRPC):

    def xmlrpc_test(self):
        """Return text testUNIX time."""
        return "test function xmlrpc_test module  xmppmasterxmlrpc OK"

    def xmlrpc_share_local_initialisation(self,
                                          list_cluster_id,
                                          name_partage,
                                          id_ars_electing,
                                          host_server):
        """ Cette function est utilisée pour initialiser
            les partages locaux suivant les clusters choisis.
            paramms : list_cluster_id est la liste des clusters definisant le partage local.
                      name_partage le nom du partage
                      id_ars_electing id de ars choisi si il est None or "" il est choisi au hazard.
                      host_server  host du server permet la creation uri pour le reverse proxy apache
        """
        result = XmppMasterDatabase().get_ars_group_in_list_clusterid(list_cluster_id,None)
        # list des ars en fonction des clusters
        listearsforsharelocal = [int(x['ars_id']) for x in result]
        if not listearsforsharelocal:
            raise xmlrpc_function_xmppmaster(
                f"aucun ars trouve associe a la list des clusters suivants {list_cluster_id}",
                "xmlrpc_share_local_initialisation",
            )
        # recuperation de la liste des id des ars.
        if id_ars_electing in [None, ""]:
            #on choisie dans la liste 1 ars au hazard.
            idchoise = listearsforsharelocal[randint(0, len(listearsforsharelocal)-1)]
        elif id_ars_electing in listearsforsharelocal:
            idchoise = id_ars_electing
        else:
            raise xmlrpc_function_xmppmaster("the parameter id_ars_electing [%s] does"\
                                                    "not belong\nto the server list"\
                                                        " local share"%id_ars_electing,
                                            "xmlrpc_share_local_initialisation")
        for ars in result:
            if ars['ars_id'] == idchoise:
                arselected= ars
                break
        logger.debug(f"the ars web elected is {arselected['nameserver']} [{idchoise}]")
        # creation uri server web package server partage local
        proxy_uri_package_server_on_ars = "http:\\\\%s\\pkgs-%s\\" % (host_server,
                                                                      arselected['nameserver'])
        # creation du partages
        new_id_share = PkgsDatabase().SetPkgs_shares(name_partage,
                                                    "comments",
                                                    1,
                                                    "local",
                                                    proxy_uri_package_server_on_ars,
                                                    arselected['nameserver'],
                                                    idchoise,
                                                    "/var/lib/pulse/local")
        if new_id_share is not None:
            # reseignement de la table pkgs_share_ars.
            # la table doit recuperer les ars participant au deploiement avec le numero du partage qui lui est associer.
            for ars in result:
                PkgsDatabase().SetPkgs_shares_ars(ars['ars_id'], ars['nameserver'], ars['jid'], new_id_share)
        return result


