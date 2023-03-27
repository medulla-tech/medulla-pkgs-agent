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

""" Class to map msc.commands to SA
"""

# big modules
import logging
import sqlalchemy
import datetime

# ORM mappings
from pulse2.database.msc.orm.commands_on_host import CommandsOnHost, stopCommandOnHost
from pulse2.database.msc.orm.commands_on_host import CoHManager
from pulse2.database.msc.orm.target import Target

# Pulse 2 stuff
from pulse2.scheduler.timeaxis import LaunchTimeResolver


class Commands(object):
    """
    Mapping between msc.commands and SA
    """
    def getId(self):
        return self.id

    def getBundleId(self):
        return self.fk_bundle

    def getOrderInBundle(self):
        return self.order_in_bundle

    def isPartOfABundle(self):
        result = self.fk_bundle is not None
        logging.getLogger().debug(f"isPartOfABundle(#{self.id}): {result}")
        return result

    def getNextConnectionDelay(self):
        return self.next_connection_delay

    def hasToWOL(self):
        result = self.do_wol == 'enable'
        logging.getLogger().debug(f"hasToWOL(#{self.id}): {result}")
        return result

    def hasToImagingMenu(self):
        result = self.do_imaging_menu == 'enable'
        logging.getLogger().debug(f"hasToImagingMenu(#{self.id}): {result}")
        return result

    def hasToRunInventory(self):
        result = self.do_inventory == 'enable'
        logging.getLogger().debug(f"hasToRunInventory(#{self.id}): {result}")
        return result

    def hasToReboot(self):
        result = self.do_reboot == 'enable'
        logging.getLogger().debug(f"hasToReboot(#{self.id}): {result}")
        return result

    def hasToHalt(self):
        result = len(self.do_halt) > 0
        logging.getLogger().debug(f"hasToHalt(#{self.id}): {result}")
        return result

    def hasToHaltIfDone(self):
        try:
            result = 'done' in self.do_halt.split(',')
        except AttributeError:  # workaround for buggy v.14 database
            result = 'done' in self.do_halt
        logging.getLogger().debug(f"hasToHaltIfDone(#{self.id}): {result}")
        return result

    def hasToHaltIfFailed(self):
        try:
            result = 'failed' in self.do_halt.split(',')
        except AttributeError:  # workaround for buggy v.14 database
            result = 'failed' in self.do_halt
        logging.getLogger().debug(f"hasToHaltIfFailed(#{self.id}): {result}")
        return result

    def hasToHaltIfOverTime(self):
        try:
            result = 'over_time' in self.do_halt.split(',')
        except AttributeError:  # workaround for buggy v.14 database
            result = 'over_time' in self.do_halt
        logging.getLogger().debug(f"hasToHaltIfOverTime(#{self.id}): {result}")
        return result

    def hasToHaltIfOutOfInterval(self):
        try:
            result = 'out_of_interval' in self.do_halt.split(',')
        except AttributeError:
            result = 'out_of_interval' in self.do_halt
        logging.getLogger().debug(f"hasToHaltIfOutOfInterval(#{self.id}): {result}")
        return result

    def hasSomethingToUpload(self):
        result = (len(self.files) != 0)
        logging.getLogger().debug(f"hasSomethingToUpload(#{self.id}): {result}")
        return result

    def hasSomethingToExecute(self):
        result = len(self.start_file) != 0
        logging.getLogger().debug(f"hasSomethingToExecute(#{self.getId()}): {result}")
        return result

    def hasSomethingToDelete(self):
        result = len(self.files) != 0
        logging.getLogger().debug(f"hasSomethingToDelete(#{self.getId()}): {result}")
        return result

    def hasToUseProxy(self):
        result = self.proxy_mode in ['queue', 'split']
        logging.getLogger().debug(f"hasToUseProxy(#{self.getId()}): {result}")
        return result

    def hasToUseQueueProxy(self):
        result = (self.proxy_mode == 'queue')
        logging.getLogger().debug(f"hasToUseQueueProxy(#{self.getId()}): {result}")
        return result

    def hasToUseSplitProxy(self):
        result = (self.proxy_mode == 'split')
        logging.getLogger().debug(f"hasToUseSplitProxy(#{self.getId()}): {result}")
        return result

    def isQuickAction(self):
        # TODO: a quick action is not only an action with nothing to upload
        result = (len(self.files) == 0)
        logging.getLogger().debug(f"isQuickAction(#{self.id}): {result}")
        return result

    def inDeploymentInterval(self):
        # TODO: a quick action is not only an action with nothing to upload
        result = (
            LaunchTimeResolver().in_deployment_interval(
                self.deployment_intervals, datetime.datetime.now()
            )
            if self.deployment_intervals
            else True
        )
        if not result:
            logging.getLogger().debug(f"inDeploymentInterval(#{self.id}): {result}")
        return result

    def in_valid_time(self):
        now = datetime.datetime.now()
        return now > self.start_date and now < self.end_date

    def getCohIds(self, target_uuids=[]):
        """
        Returns the list of commands_on_host linked to this command
        If list of target_uuids, returns only uuids of this list
        """
        session = sqlalchemy.orm.create_session()
        myCommandOnHosts = session.query(CommandsOnHost)
        if target_uuids:
            myCommandOnHosts = myCommandOnHosts.join(Target)
            myCommandOnHosts = myCommandOnHosts.filter(Target.target_uuid.in_(target_uuids))
        myCommandOnHosts = myCommandOnHosts.filter(CommandsOnHost.fk_commands ==
                                                   self.getId())
        session.close()
        return myCommandOnHosts.all()

    def getFilesList(self):
        return [a.split("/").pop() for a in self.files.split("\n")]

    def setNextConnectionDelay(self, delay):
        """"set delay to the next attept """
        self.next_connection_delay = delay
        self.flush()

    def extend(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.flush()

    def update_stats(self, session=None, **kwargs):
        self.sum_running = kwargs.get("scheduled", 0)
        self.sum_done = kwargs.get("done", 0)
        self.sum_stopped = kwargs.get("stopped", 0)
        self.sum_failed = kwargs.get("failed", 0)
        self.sum_overtimed = kwargs.get("over_timed", 0)
        if not session:
            self.flush()

    def flush(self):
        """ Handle SQL flushing """
        session = sqlalchemy.orm.create_session()
        session.add(self)
        session.flush()
        session.close()

    def toH(self):
        return {
            'id': self.id,
            'state': self.state,
            'creation_date': self.creation_date,
            'sum_running': self.sum_running,
            'sum_done': self.sum_done,
            'sum_stopped': self.sum_stopped,
            'sum_overtimed': self.sum_overtimed,
            'sum_failed': self.sum_failed,
            'start_file': self.start_file,
            'parameters': self.parameters,
            'start_script': self.start_script,
            'clean_on_success': self.clean_on_success,
            'files': self.files,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'target': '',
            'connect_as': self.connect_as,
            'creator': self.creator,
            'dispatched': self.dispatched,
            'title': self.title,
            'do_inventory': self.do_inventory,
            'do_reboot': self.do_reboot,
            'do_wol': self.do_wol,
            'do_imaging_menu': self.do_imaging_menu,
            'do_halt': self.do_halt,
            'next_connection_delay': self.next_connection_delay,
            'max_connection_attempt': self.max_connection_attempt,
            'pre_command_hook': self.pre_command_hook,
            'post_command_hook': self.post_command_hook,
            'pre_run_hook': self.pre_run_hook,
            'post_run_hook': self.post_run_hook,
            'on_success_hook': self.on_success_hook,
            'on_failure_hook': self.on_failure_hook,
            'maxbw': self.maxbw,
            'deployment_intervals': self.deployment_intervals,
            'bundle_id': self.fk_bundle,  # keep it for compatibility
            'fk_bundle': self.fk_bundle,
            'order_in_bundle': self.order_in_bundle,
            'proxy_mode': self.proxy_mode,
            'type': self.type
        }


def stop_commands_on_host(cohs):
    groups = CoHManager.setCoHsStateStopped(cohs)
    session = sqlalchemy.orm.create_session()

    for cmd_id, count in groups.items():
        cmd = session.query(Commands).get(cmd_id)
        # update stats
        cmd.sum_running -= count
        cmd.sum_stopped += count
        session.add(cmd)
    session.close()


def stopCommand(c_id):
    """
    Stop a command, by stopping all its related commands_on_host.
    @returns: the list of all related commands_on_host
    @rtype: list
    """
    session = sqlalchemy.create_session()
    myCommand = session.query(Commands).get(c_id)
    ret = []
    for cmd in myCommand.getCohIds():
        ret.append(cmd)
        stopCommandOnHost(cmd.id)
    session.close()
    return ret
