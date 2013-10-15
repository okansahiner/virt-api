import ConfigParser, sys


class agentConfig:
    def __init__(self):
        self.__loggingConfig={}
        self.__connectionConfig={}
        self.__file="/root/vm_agent/vm_agent.conf"
        self.__sections=[]
        self.__configFile=ConfigParser.RawConfigParser()
	self.__boolErrorLoggingEnabled=None
	self.__boolDebuggingEnabled=None
	self.__ErrorLoggingPath=None
	self.__DebuggingPath=None
	self.__ListenIp=None
	self.__ListenPort=None
        try:
            self.__configFile.readfp(open(self.__file))
        except Exception, e:
            sys.stderr.write("Agent Config file: " + self.__file + str(e) + "\n")
            sys.exit(1)
        else:
            sys.stdout.write("Agent Config file: " + self.__file + " successfully read\n")

	    for confSec in self.__configFile.sections():
		if not ((confSec == "Logging") or (confSec == "Connection")):
			sys.stderr.write("Agent Config File: Unknown section " + confSec +"\n")
			sys.exit(1)
		else:
			for confOp in self.__configFile.options(confSec):
				if not ((confOp=="error logging") or (confOp=="error file") or (confOp=="debugging") or (confOp=="debug file") or (confOp=="ip") or (confOp=="listening port")):
					sys.stderr.write("Agent Config File: Unknown option " + confOp + " in section " + confSec + "\n")
					sys.exit(1)
			

 	    try:
			self.__ListenIp=self.__configFile.get("Connection", "IP")
			self.__ListenPort=self.__configFile.get("Connection", "Listening port")
	    except Exception, e:
			sys.stderr.write("Agent Config file: " + str(e)  + "\n")
			sys.exit(1)
            
	    try:
			self.__boolDebuggingEnabled=self.__configFile.getboolean("Logging", "Debugging")
	    except Exception,e:
			self.__boolDebuggingEnabled=False
			sys.stdout.write("Agent Config file: " + self.__file + " "  + str(e) + ", setting default value False\n" )
	    finally:
			sys.stdout.write("Agent Config file: Debugging value " + str(self.__boolDebuggingEnabled) + "\n")

	    if self.__boolDebuggingEnabled:
	            try:
        	    	self.__DebuggingPath=self.__configFile.get("Logging", "debug file")		  
		    except Exception,e:
                        self.__DebuggingPath="/var/log/vm_agent_debug.log"
                        sys.stdout.write("Agent Config file: " + str(e) + ", setting default path is /var/log/vm_agent_debug.log\n" )
	            finally:
                        sys.stdout.write("Agent Config file: Debugging file " + self.__DebuggingPath + "\n")


	    try:
		self.__boolErrorLoggingEnabled=self.__configFile.getboolean("Logging","Error Logging")
	    except Exception,e:
		self.__boolErrorLoggingEnabled=True
		sys.stdout.write("Agent Config file: " + self.__file + " "  + str(e) + ", setting default value True\n" )
	    finally:
		sys.stdout.write("Agent Config file: Error Logging value " + str(self.__boolErrorLoggingEnabled)  + "\n" )


	    if self.__boolErrorLoggingEnabled:
		     try:
			self.__ErrorLoggingPath=self.__configFile.get("Logging","error file")
		     except Exception,e:
			self.__ErrorLoggingPath="/var/log/vm_agent_error.log"
			sys.stdout.write("Agent Config file: " + str(e) + ", setting default path is /var/log/vm_agent_error.log\n" )
		     finally:
			sys.stdout.write("Agent Config file: Error logging file " + self.__ErrorLoggingPath + "\n")
	    else:
		     self.__ErrorLoggingPath="/dev/null"
		     sys.stdout.write("Agent Config file: Error logging redirected to /dev/null\n")

	sys.stdout.write("Agent Config File: " + self.__file + " successfuly read, exitting\n")
	
        
    def isDebuggingEnabled(self):
        	return self.__boolDebuggingEnabled
    
    def getDebuggingPath(self):
        	return self.__DebuggingPath
    
    def isErrorLoggingEnabled(self):
        	return self.__boolErrorLoggingEnabled
    
    def getErrorLoggingPath(self):
        	return self.__ErrorLoggingPath

    def getListeningIp(self):
        	return self.__ListenIp
    
    def getListeningPort(self):
        	return self.__ListenPort

"""
agentConf=agentConfig() 
print agentConf.isDebuggingEnabled()
print agentConf.getDebuggingPath()
print agentConf.isErrorLoggingEnabled()
print agentConf.getErrorLoggingPath()
print agentConf.getListeningIp()
print agentConf.getListeningPort()

"""

