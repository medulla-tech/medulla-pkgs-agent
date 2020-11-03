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

# uses SA to handle sessions

import logging

""" Class to map pkgs.pkgs_ars_web_shares to SA
"""
class Pkgs_ars_web_shares(object):
    """ Mapping between pkgs.pkgs_ars_web_shares and SA
        colunm table: 'id,pkgs_share_id,ars_share_id,packages_id,status,finger_print,size,edition_date'
    """

    def getId(self):
        if self.id is not None:
            return self.id
        else:
            return 0

    def getPkgs_share_id(self):
        if self.pkgs_share_id is not None:
            return self.pkgs_share_id
        else:
            return -1

    def getArs_share_id(self):
        if self.ars_share_id is not None:
            return self.ars_share_id
        else:
            return-1

    def getPackages_id(self):
        if self.packages_id is not None:
            return self.packages_id
        else:
            return ""

    def getStatus(self):
        if self.status is not None:
            return self.status
        else:
            return ""

    def getFinger_print(self):
        if self.finger_print is not None:
            return self.finger_print
        else:
            return ""

    def getSize(self):
        if self.size is not None:
            return self.size
        else:
            return 0

    def getEdition_date(self):
        if self.edition_date is not None:
            return self.edition_date
        else:
            return ""

    def to_array(self):
        return {
            'id': self.getId(),
            'pkgs_share_id': self.getPkgs_share_id(),
            'ars_share_id': self.getArs_share_id(),
            'packages_id': self.getPackages_id(),
            'status': self.getStatus(),
            'finger_print': self.getFinger_print(),
            'size': self.getSize(),
            'edition_date': self.getEdition_date()}

    def toH(self):
        return {
            'id': self.id,
            'pkgs_share_id': self.pkgs_share_id,
            'ars_share_id': self.ars_share_id,
            'packages_id': self.packages_id,
            'status': self.status,
            'finger_print': self.finger_print,
            'size': self.size,
            'edition_date': self.edition_date}
