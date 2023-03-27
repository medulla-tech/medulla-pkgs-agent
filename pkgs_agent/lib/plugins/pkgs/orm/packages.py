# -*- coding: utf-8; -*-
#
# (c) 2004-2007 Linbox / Free&ALter Soft, http://linbox.com
# (c) 2007-2009 Mandriva, http://www.mandriva.com/
#
# $Id$
#
# This file is part of Pulse 2, http://pulse2.mandriva.org
#
# Pulse 2 is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Pulse 2 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pulse 2; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.

""" Class to map msc.commands_on_host to SA
"""

import logging
import time
import datetime
import sqlalchemy.orm


class Packages(object):
    """ Mapping between msc.commands_on_host and SA
    """

    def getId(self):
        return self.id if self.id is not None else 0

    def getLabel(self):
        return self.label if self.label != None else ""

    def getDescription(self):
        return self.description if self.description is not None else ""

    def getUuid(self):
        return self.uuid if self.uuid is not None else ""

    def getVersion(self):
        return self.version if self.version is not None else ""

    def getOs(self):
        return self.os if self.os is not None else ""

    def getMetaGenerator(self):
        return self.metagenerator if self.metagenerator is not None else "expert"

    def getEntity_id(self):
        return self.entity_id if self.entity_id is not None else "0"

    def getSub_packages(self):
        return self.sub_packages if self.sub_packages is not None else ""

    def getReboot(self):
        return self.getReboot if self.reboot is not None else ""

    def getInventory_associateinventory(self):
        if self.inventory_associateinventory is not None:
            return self.inventory_associateinventory
        else:
            return ""

    def getInventory_licenses(self):
        return self.inventory_licenses if self.inventory_licenses is not None else ""

    def getQversion(self):
        return self.Qversion if self.Qversion is not None else ""

    def getQvendor(self):
        return self.Qvendor if self.Qvendor is not None else ""

    def getQsoftware(self):
        return self.Qsoftware if self.Qsoftware is not None else ""

    def getBoolcnd(self):
        return self.boolcnd if self.boolcnd is not None else 0

    def getPostCommandSuccess_command(self):
        if self.postCommandSuccess_command is not None:
            return self.postCommandSuccess_command
        else:
            return ""

    def getPostCommandSuccess_name(self):
        if self.postCommandSuccess_name is not None:
            return self.postCommandSuccess_name
        else:
            return ""
    def getInstallInit_command(self):
        return self.installInit_command if self.installInit_command is not None else ""

    def getInstallInit_name(self):
        return self.installInit_name if self.installInit_name is not None else ""

    def getPostCommandFailure_command(self):
        if self.postCommandFailure_command is not None:
            return self.postCommandFailure_command
        else:
            return ""

    def getPostCommandFailure_name(self):
        if self.postCommandFailure_name is not None:
            return self.postCommandFailure_name
        else:
            return ""

    def getCommand_command(self):
        return self.command_command if self.command_command is not None else ""

    def getCommand_name(self):
        return self.command_name if self.command_name is not None else ""

    def getPreCommand_command(self):
        return self.preCommand_command if self.preCommand_command is not None else ""

    def getPreCommand_name(self):
        return self.preCommand_name if self.preCommand_name is not None else ""


    def to_array(self):
        """
        This function serialize the object to dict.

        Returns:
            Dict of elements contained into the object.
        """
        return {
            'entity_id' : self.getEntity_id(),
            'description' : self.getDescription(),
            'sub_packages' : self.getSub_packages(),
            'id': self.getUuid(),
            'pk_id': self.getId(),
            'commands':{
                'postCommandSuccess': {
                    'command': self.getPostCommandSuccess_command(),
                    'name': self.getPostCommandSuccess_name()
                },
                'installInit':{
                    'command': self.getInstallInit_command(),
                    'name': self.getInstallInit_name()
                },
                "postCommandFailure": {
                    "command": self.getPostCommandFailure_command(),
                    "name": self.getPostCommandFailure_name(),
                },
                "command": {
                    "command": self.getCommand_command(),
                    "name": self.getCommand_name(),
                },
                "preCommand": {
                    "command": self.getPreCommand_command(),
                    "name": self.getPreCommand_name()
                }
            },
            'name': self.getLabel(),
            'targetos': self.getOs(),
            'reboot': self.getReboot(),
            'version': self.getVersion(),
            'inventory': {
                'associateinventory': self.getInventory_associateinventory(),
                'licenses': self.getInventory_licenses(),
                "queries": {
                    "Qversion": self.getQversion(),
                    "Qvendor": self.getQvendor(),
                    "boolcnd": self.getBoolcnd(),
                    "Qsoftware": self.getQsoftware()
                },
                "metagenerator": self.getMetaGenerator()
            }
        }


    def toH(self):
        return {'id': self.id,
                "label": self.label,
                "description": self.description,
                "uuid": self.uuid,
                "version": self.version,
                "os": self.os,
                "metagenerator": self.metagenerator,
                "entity_id": self.entity_id,
                "sub_packages": self.sub_packages,
                "reboot": self.reboot,
                "inventory_associateinventory": self.inventory_associateinventory,
                "inventory_licenses": self.inventory_licenses,
                "Qversion": self.Qversion,
                "Qvendor": self.Qvendor,
                "Qsoftware": self.Qsoftware,
                "boolcnd": self.boolcnd,
                "postCommandSuccess_command": self.postCommandSuccess_command,
                "postCommandSuccess_name": self.postCommandSuccess_name,
                "installInit_command": self.installInit_command,
                "installInit_name": self.installInit_name,
                "postCommandFailure_command": self.postCommandFailure_command,
                "postCommandFailure_name": self.postCommandFailure_name,
                "command_command": self.command_command,
                "command_name": self.command_name,
                "preCommand_command": self.preCommand_command,
                "preCommand_name": self.preCommand_name}
