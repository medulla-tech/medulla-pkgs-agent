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

import logging

""" Class to map pkgs.dependencies to SA
"""

class Dependencies(object):
    """ Mapping between msc.bundle and SA
    """
    def getId(self):
        return self.id if self.id is not None else 0

    def getUuid_package(self):
        return self.uuid_package if self.uuid_package is not None else ""

    def getUuid_dependency(self):
        return self.uuid_dependency if self.uuid_dependency is not None else ""

    def to_array(self):
        """
        This function serialize the object to dict.

        Returns:
            Dict of elements contained into the object.
        """
        return {
            'id' : self.getId(),
            'uuid_package': self.getUuid_package(),
            'uuid_dependency': self.getUuid_dependency()
        }

    def toH(self):
        return {'id': self.id,
                'uuid_package': self.uuid_package,
                'uuid_dependency': self.uuid_dependency}
