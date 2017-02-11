
import ConfigParser, sys, logging

class agentConfig:
    def __init__(self):
        self.__loggingConfig={}
        self.__connectionConfig={}
        self.__file="/root/vm-agent/vm-agent.conf"
        self.__sections=[]
        self.__configFile=ConfigParser.ConfigParser()
        
        try:
            self.__configFile.read(self.__file)
        except:
            err=sys.exc_info()[1]
            sys.stderr.write("agentConfig.constructor():Agent Config file" + self.__file + " couldnt read, " + str(err))
            sys.exit(1)
        else:
            logging.debug("agentConfig.constructor():Agent Config file" + self.__file + " successfully read")
            self.__sections=self.__configFile.sections()
        
        self.refreshAllParameters()
    
    def refreshLoggingParameters(self):
        self.__loggingConfig["debugging"]="no"
        self.__loggingConfig["debug file"]="/var/log/vm-agent-debug.log"
        self.__loggingConfig["error logging"]="no"
        self.__loggingConfig["error file"]="/var/log/vm-agent-error.log"        
        loggingConfig=None
        
        for section in self.__sections:
            if section == "Logging":
                loggingConfig=section
                break

        if loggingConfig == None:
            sys.stderr.write("agentConfig.refreshLoggingParameters(): Logging parameters section couldnt found")
            sys.exit(1)
        
        else:
            keys=self.__configFile.options(loggingConfig)
 
            for key in keys:
                if self.__loggingConfig.has_key(key):
                                        
                    if key == "debugging" or key=="error logging":
                        try:
                            self.__loggingConfig[key]=self.__configFile.getboolean(loggingConfig, key)
                        except:
                            err=sys.exc_info()[1]
                            sys.stderr.write("agentConfig.refreshLoggingParameters(): Logging parameters section, key "+self.__loggingConfig[key]+ ": "+str(err))
                            sys.exit(1)
                            
                    else:
                        self.__loggingConfig[key] = self.__configFile.get(loggingConfig, key)

                else:
                    sys.stderr.write("agentConfig.refreshLoggingParameters(): No such an option " +key)
                    sys.exit(1)
            

    def refreshConnectionParameters(self):
        self.__connectionConfig["interface"]=None
        self.__connectionConfig["listening port"]="4444"
        self.__connectionConfig["connecting port"]="4444"
        connectingConfig=None
        
        for section in self.__sections:
            if section=="Connection":
                connectionConfig=section
                break
        
        if connectionConfig==None:
            sys.stderr.write("agentConfig.refreshConnectionParameters(): Connection parameters section couldnt found")
            sys.exit(1)
            
        else:
             keys=self.__configFile.options(connectionConfig)
             
             for key in keys:
                if self.__connectionConfig.has_key(key):
                    self.__connectionConfig[key] = self.__configFile.get(connectionConfig, key)
                    
                else:
                    sys.stderr.write("agentConfig.refreshConnectionParameters(): No such an option " +key)
                    sys.exit(1)
            
    def refreshAllParameters(self):
        self.refreshLoggingParameters()
        self.refreshConnectionParameters()
        
    def isDebuggingEnabled(self):
        logging.debug("agentConfig.isDebuggingEnabled(): "+ str(self.__loggingConfig["debugging"]))
        return self.__loggingConfig["debugging"]
    
    def getDebuggingPath(self):
        logging.debug("agentConfig.getDebuggingPath(): "+ self.__loggingConfig["debug file"])
        return self.__loggingConfig["debug file"]
    
    def isErrorLoggingEnabled(self):
        logging.debug("agentConfig.isErrorLoggingEnabled(): "+ str(self.__loggingConfig["error logging"]))
        return self.__loggingConfig["error logging"]
    
    def getErrorLoggingPath(self):
        logging.debug("agentConfig. getErrorLoggingPath(): "+ self.__loggingConfig["error file"])
        return self.__loggingConfig["error file"]

    def getInterface(self):
        logging.debug("agentConfig.getInterface(): "+ self.__connectionConfig["interface"])
        return self.__connectionConfig["interface"]
    
    def getListeningPort(self):
        logging.debug("agentConfig.getListeningPort((): "+self.__connectionConfig["listening port"])        
        return self.__connectionConfig["listening port"]

    def getConnectingPort(self):
        logging.debug("agentConfig.getConnectingPort(): "+self.__connectionConfig["connecting port"])         
        return self.__connectionConfig["connecting port"]


#conf=agentConfig("/root/vm-agent/vm-agent.conf")

#print conf.isErrorLoggingEnabled()