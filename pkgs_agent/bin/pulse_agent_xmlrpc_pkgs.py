#! /usr/bin/python
# -*- coding: utf-8; -*-
# (c) 2016 Siveo, http://www.siveo.net
# 
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program If not, see <http://www.gnu.org/licenses/>.

import time
import xmlrpclib
# import twisted.internet.error
# import twisted.copyright

from twisted.web import  server
from twisted.internet import reactor # protocol, defer,
# from twisted.python import failure
try:
    from twisted.web import http # pyflakes.ignore
except ImportError:
    from twisted.protocols import http  # pyflakes.ignore


import os
import os.path
import sys
from optparse import OptionParser
import signal

from resource import RLIMIT_NOFILE, RLIM_INFINITY, getrlimit
import logging

# directory pkgs_agent
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")))

from lib.xml_rpc_pkgs import pkgsxmlrpc
from lib.configuration import confParameter
from lib.utils import writePid, cleanPid, makeSSLContext
from lib.xml_rpc_server import TwistedRPCServer

logger = logging.getLogger()

Fault = xmlrpclib.Fault

def createDaemon(opts):
    """
        This function create a service/Daemon that will execute a det. task
    """

    #config = confParameter(opts.dft_inifile)
    try:
        pid = os.fork()
        if pid > 0:
            # Wait for initialization before exiting
            time.sleep(2)
            # exit first parent and return
            sys.exit(0)
    except OSError, e:
        print >>sys.stderr, "fork #1 failed: %d (%s)" % (e.errno, e.strerror)
        sys.exit(1)

    # decouple from parent environment
    os.chdir("/")
    os.setsid()

    # do second fork
    try:
        pid = os.fork()
        if pid > 0:
            # exit from second parent
            sys.exit(0)
    except OSError, e:
        sys.exit(1)

    maxfd = getrlimit(RLIMIT_NOFILE)[1]
    if maxfd == RLIM_INFINITY:
        maxfd = 1024

    for fd in range(0, maxfd):
        # Don't close twisted FDs
        # TODO: make a clean code to be sure nothing is opened before this function
        # ie: daemonize very early, then after import all stuff...
        if fd not in (3, 4, 5, 6, 7, 8):
            try:
                os.close(fd)
            except OSError:
                pass

    if (hasattr(os, "devnull")):
        REDIRECT_TO = os.devnull
    else:
        REDIRECT_TO = "/dev/null"

    os.open(REDIRECT_TO, os.O_RDWR)
    os.dup2(0, 1)
    os.dup2(0, 2)
    # write pidfile
    writePid(opts.PIDFile)
    doTask(opts)

def doTask(opts):
    format = '%(asctime)s - %(levelname)s - %(message)s'
    #logging.handlers.TimedCompressedRotatingFileHandler = TimedCompressedRotatingFileHandler
    # more information log
    # format ='[%(name)s : %(funcName)s : %(lineno)d] - %(levelname)s - %(message)s'
    conf = confParameter(opts.dft_inifile)
    if not opts.deamon:
        if opts.consoledebug :
            logging.basicConfig(level = logging.DEBUG, format=format)
        else:
            logging.basicConfig( level = conf.log_level,
                                 format = format,
                                 filename = conf.logfile,
                                 filemode = 'a')
    else:
        logging.basicConfig( level = conf.log_level,
                             format = format,
                             filename = conf.logfile,
                             filemode = 'a')
    #protocole="http"
    #if conf.enablessl : protocole="https"

    # Start the application
    app = Apppkgs( opts)
    app.run()

class Apppkgs(object):
    """ Represent the Apppkgs """
    def __init__(self, opts):
        self.config = confParameter(opts.dft_inifile)
        self.opts = opts
        self.daemon = opts.deamon
        self.PIDFile = "/var/run/ripright/pkgsagent.pid"
        
    def run(self):
        r = TwistedRPCServer(self.config.user,
                             self.config.password)
        pkgoobj = pkgsxmlrpc()
        r.putSubHandler('pkgsf', pkgoobj)
        if self.config.enablessl:
            logger.debug("SSL Context")
            sslContext = makeSSLContext(self.config.verifypeer,
                                        self.config.cacert,
                                        self.config.localcert)
            
            reactor.listenSSL(self.config.port,
                              server.Site(r),
                              interface=self.config.host,
                              contextFactory=sslContext)
        else:
            reactor.listenTCP(self.config.port,
                              server.Site(r),
                              interface=self.config.host)
        logger.debug("Start xmpp server "\
            "agent pkgs. on %s:%s" % (self.config.host,
                                      self.config.port))
        reactor.run()
        # Add event handler before shutdown
        reactor.addSystemEventTrigger('before',
                                      'shutdown',
                                      self.cleanUp)

    def cleanUp(self):
        """
            function call before shutdown of reactor
        """
        logger.info('Pkgs-agent stop...')
        cleanPid(self.PIDFile)
    
    def kill(self):
        pid = self.readPid(self.PIDFile)
        if pid is None:
            print "Can not find a running Pkgs-agent."
            return 1
        try:
            os.kill(pid, signal.SIGTERM)
        except Exception, e:
            print "Can not terminate running Pkgs-agent: %s" % e
            return 1
        return 0

if __name__ == '__main__':
    if sys.platform.startswith('linux') and  os.getuid() != 0:
        print "Agent must be running as root"
        sys.exit(0)
    elif sys.platform.startswith('win') or sys.platform.startswith('darwin') :
        print "Pulse agent must be running on ARS linux os"
        sys.exit(0)
    
    optp = OptionParser()
    optp.add_option("-d",
                    "--deamon",
                    action="store_true",
                    dest="deamon",
                    default=False,
                    help="deamonize process")
    optp.add_option("-c",
                    "--consoledebug",
                    action="store_true",
                    dest="consoledebug",
                    default = False,
                    help="console debug")
    optp.add_option("-f",
                    "--inifile", 
                    dest="dft_inifile",
                    default=os.path.join("etc",
                                         "pulse",
                                         "agent",
                                         "pulse_agent_xmlrpc_pkgs.ini"),
                      help="Path to configuration file")
    optp.add_option("-p", "--pid",
                    dest="PIDFile",
                    default="/var/run/pkgsagent/pkgsagent.pid",
                    help="Path to pid file")
    optp.add_option("-k",
                    "--kill",
                    dest="kill",
                    default=False,
                    action="store_true",
                    help="Kill running daemon, if any")
    optp.add_option("-r",
                    "--reload",
                    dest="reload",
                    default=False,
                    action="store_true",
                    help="Reload configuration")
    
    opts, args = optp.parse_args()
    config = confParameter(opts.dft_inifile)

    if not opts.deamon :
        doTask(opts)
    else:
        createDaemon(opts)
