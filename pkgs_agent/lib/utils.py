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
from twisted.internet import ssl
import logging

logger = logging.getLogger()


def writePid(PIDFile):
    pid = os.getpid()
    f = open(PIDFile, 'w')
    try:
        f.write('%s\n' % pid)
    finally:
        f.close()

def cleanPid(PIDFile):
    if os.path.exists(PIDFile):
        os.unlink(PIDFile)

def makeSSLContext(verifypeer, cacert, localcert):
    """
    Make the SSL context for the server, according to the parameters

    @returns: a SSL context
    @rtype: twisted.internet.ssl.ContextFactory
    """
    if verifypeer:
        fd = open(localcert)
        localCertificate = ssl.PrivateCertificate.loadPEM(fd.read())
        fd.close()
        fd = open(cacert)
        caCertificate = ssl.Certificate.loadPEM(fd.read())
        fd.close()
        ctx = localCertificate.options(caCertificate)
        ctx.verify = True
        ctx.verifyDepth = 9
        ctx.requireCertification = True
        ctx.verifyOnce = True
        ctx.enableSingleUseKeys = True
        ctx.enableSessions = True
        ctx.fixBrokenPeers = False
        logger.debug("CA certificate informations: %s" % cacert)
        logger.debug(caCertificate.inspect())
        logger.debug("MMC agent certificate: %s" % localcert)
        logger.debug(localCertificate.inspect())
    else:
        logger.warning("SSL enabled, but peer verification is disabled.")
        ctx = ssl.DefaultOpenSSLContextFactory(localcert, cacert)
    return ctx

