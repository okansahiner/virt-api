
import sys, os, time, atexit, logging
from signal import SIGTERM
from vm_host import vmHost
#from config_parser import agentConfig

from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)
    
class Daemon:
        def __init__(self, listenPort, stdErr ):
            self.__server=None
            self.__agentConfig=None
            self.__stdin = '/dev/null'
            self.__stdout =  '/dev/null'
            self.__stderr= stdErr
            self.__pidfile='/var/run/vm-agent.pid'
            self.__listenPort=listenPort         
                             
        def daemonize(self):
                try:
                        pid = os.fork()
                        if pid > 0:
                                sys.exit(0)
                except OSError, e:
                        sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
                        sys.exit(1)

                os.chdir("/")
                os.setsid()
                os.umask(0)
                try:
                        pid = os.fork()
                        if pid > 0:
                                sys.exit(0)
                except OSError, e:
                        sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
                        sys.exit(1)
                        
                sys.stdout.flush()
                sys.stderr.flush()
                si = file(self.__stdin, 'r')
                so = file(self.__stdout, 'a+')
                se = file(self.__stderr, 'a+', 0)
                os.dup2(si.fileno(), sys.stdin.fileno())
                os.dup2(so.fileno(), sys.stdout.fileno())
                os.dup2(se.fileno(), sys.stderr.fileno())
                atexit.register(self.delpid)
                pid = str(os.getpid())
                file(self.__pidfile,'w+').write("%s\n" % pid)
       
        def delpid(self):
                os.remove(self.__pidfile)
 
        def start(self):
                try:
                        pf = file(self.__pidfile,'r')
                        pid = int(pf.read().strip())
                        pf.close()
                except IOError:
                        pid = None
       
                if pid:
                        message = "pidfile %s already exist. Daemon already running?\n"
                        sys.stderr.write(message % self.__pidfile)
                        sys.exit(1)     
                self.daemonize()
                self.run()
 
        def stop(self):
                try:
                        pf = file(self.__pidfile,'r')
                        pid = int(pf.read().strip())
                        pf.close()
                except IOError:
                        pid = None
       
                if not pid:
                        message = "pidfile %s does not exist. Daemon not running?\n"
                        sys.stderr.write(message % self.__pidfile)
                        return

                try:
                        while 1:
                                os.kill(pid, SIGTERM)
                                time.sleep(0.1)
                except OSError, err:
                        err = str(err)
                        if err.find("No such process") > 0:
                                if os.path.exists(self.__pidfile):
                                        os.remove(self.__pidfile)
                        else:
                                print str(err)
                                sys.exit(1)
 
        def restart(self):
                self.stop()
                self.start()
 
        def run(self):
            self.__server = SimpleXMLRPCServer(("10.0.1.10", int(self.__listenPort)), requestHandler=RequestHandler, allow_none=True)
            self.__server.register_introspection_functions()
            self.__server.register_instance(vmHost())
            self.__server.serve_forever()
