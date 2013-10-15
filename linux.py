# linux api for getting some info from linux hosts
# you need psutil python package installed
# pip install psutil

import platform, psutil, datetime, subprocess, os, logging
from libvirt_api import getVirtServicePid, isAgentDebuggingEnabled, getAgentDebuggingPath


if isAgentDebuggingEnabled():
        debugPath=getAgentDebuggingPath()
        logging.basicConfig(level=logging.DEBUG, filename=debugPath, format='%(asctime)s %(levelname)s: %(message)s',datefmt='%Y-%m-%d %H:%M:%S')



class Linux():
    def __init__(self):
        logging.debug("Host.constructor(): New Host Constructor invoked")
        self.__machine_type=None
        self.__network_name=None
        self.__processor=None
        self.__python_version=None
        self.__linuxKernel_version=None
        #self.__name=None
        self.__distroName=None
        self.__distroVersion=None
        self.__distroCode=None
        self.__vm_manager_pid=None
        self.__cpuUsage=None
        self.__freePhyMem=None
        self.__freeVirtMem=None
        self.__usedPhyMem=None
        self.__totalVirtMem=None
        self.__manager_process=None
        self.__virt_process=None
        self.__processUptime=None
        #self.__processOwner=None
        self.__virtProcessPid=None
        self.__virtProcessName=None
        #self.__virtProcessUsername=None
       # self.__numOfProcessThreads=None
        #self.__numOfVirtProcessThreads=None
        #self.__virtProcessThreadIDs=[]
        #self.__processThreadIDs=[]
        self.__proccessCpuUsage=None
        self.__virtProcessCpuUsage=None
        self.__processMemUsage=None
        self.__virtProcessMemUsage=None
        #self.__processOpenedFilesSpecs=None
        #self.__virtProcessOpenedFilesSpecs=None
        #self.__processConnectionsSpecs=None
        #self.__virtProcessConnectionsSpecs=None 
        self.__systemSpecsList={}      
        self.refresh()
        self.setList()
        
    def setList(self):
        logging.debug("Host.setList(): setting all host entries as list")
        self.__systemSpecsList["machine type"]=self.__machine_type
        self.__systemSpecsList["network name"]=self.__network_name
        self.__systemSpecsList["processor"]=self.__processor
        self.__systemSpecsList["python version"]=self.__python_version
        self.__systemSpecsList["kernel version"]=self.__linuxKernel_version
        self.__systemSpecsList["linux distro name"]=self.__distroName
        self.__systemSpecsList["linux distro version"]=self.__distroVersion
        self.__systemSpecsList["linux distro code"]=self.__distroCode
        self.__systemSpecsList["agent PID"]=self.__vm_manager_pid
        self.__systemSpecsList["cpu usage"]=self.__cpuUsage
        self.__systemSpecsList["free physical memory"]=self.__freePhyMem
        self.__systemSpecsList["free virtual memory"]=self.__freeVirtMem
        self.__systemSpecsList["used physical memory"]=self.__usedPhyMem
        self.__systemSpecsList["total virtual memory"]=self.__totalVirtMem
        self.__systemSpecsList["agent process uptime"]=self.__processUptime
        self.__systemSpecsList["virtualization process PID"]=self.__virtProcessPid
        self.__systemSpecsList["virtualization process name"]=self.__virtProcessName
        self.__systemSpecsList["agent process cpu usage"]=self.__proccessCpuUsage
        self.__systemSpecsList["virtualization process cpu usage"]=self.__virtProcessCpuUsage
        self.__systemSpecsList["agent process memory usage"]=self.__processMemUsage
        self.__systemSpecsList["virtualization process memory usage"]=self.__virtProcessMemUsage
        
    def getList(self):
        logging.debug("Host.getList(): getting all host entries as list")
        return self.__systemSpecsList

        
    def refresh(self):
        logging.debug("Host.refresh(): Refreshing all host entries")
        self.refreshVirtServiceSpecs()
        self.__machine_type=platform.machine()
        self.__network_name=platform.node()
        self.__processor=platform.processor()
        self.__python_version=platform.python_version()
        self.__linuxKernel_version=platform.release()
        #self.__name=platform.system()
        dist_info=platform.linux_distribution(distname='', version='', id='', supported_dists=('SuSE', 'debian', 'redhat'), full_distribution_name=1)
        self.__distroName=dist_info[0]
        self.__distroVersion=dist_info[1]
        self.__distroCode=dist_info[2]
        self.__vm_manager_pid=os.getpid()
        self.__freePhyMem=psutil.avail_phymem()/1048576
        self.__freeVirtMem=psutil.avail_virtmem()/1048576
        self.__totalVirtMem=psutil.total_virtmem()/1048576
        self.__usedPhyMem=psutil.used_phymem()/1048576
        self.__manager_process=psutil.Process(self.__vm_manager_pid)
        self.__virt_process=psutil.Process(int(self.__virtProcessPid))
        self.__processUptime=datetime.datetime.fromtimestamp(self.__manager_process.create_time).strftime("%Y-%m-%d %H:%M")
        #self.__processOwner=self.__manager_process.username
        #self.__numOfProcessThreads=self.__manager_process.get_num_threads()
        #self.__numOfVirtProcessThreads=self.__virt_process.get_num_threads()
    
        #for thread in self.__virt_process.get_threads():
        #    self.__virtProcessThreadIDs.append(thread[0])
            
        #for thread in self.__manager_process.get_threads():
        #    self.__processThreadIDs.append(thread[0])

        self.__virtProcessCpuUsage=self.__virt_process.get_cpu_percent()
        self.__proccessCpuUsage=self.__manager_process.get_cpu_percent()
        mem=self.__virt_process.get_memory_info()
        self.__virtProcessMemUsage=mem[1]/1048576
        mem=self.__manager_process.get_memory_info()
        self.__processMemUsage=mem[1]/1048576
        #self.__processOpenedFilesSpecs=self.__manager_process.get_open_files()
        #self.__virtProcessOpenedFilesSpecs=self.__virt_process.get_open_files()
        #self.__processConnectionsSpecs=self.__manager_process.get_connections()
        #self.__virtProcessConnectionsSpecs=self.__virt_process.get_connections()
        self.__cpuUsage=psutil.cpu_percent()

        
    def refreshVirtServiceSpecs(self):
        logging.debug("Host. refreshVirtServiceSpecs(): Refreshing libvirt service specs")
        if self.isVirtServiceRunning() is False:
            if self.startVirtService() is False:
                logging.debug("Host. refreshVirtServiceSpecs(): Failed in refreshing libvirt service specs")
                return None
        
        self.__virtProcessPid=getVirtServicePid()
	virtProcess=psutil.Process(self.__virtProcessPid)
        self.__virtProcessName=virtProcess.name
        #self.__virtProcessUsername=virtProcess.username
        
    def isVirtServiceRunning(self):
        self.__virtProcessPid=getVirtServicePid()
        if self.__virtProcessPid==None:
            logging.debug("Host.isVirtServiceRunning(): libvirtd is not running")            
            return False
        else:
            logging.debug("Host.isVirtServiceRunning(): libvirtd is running")
            return True
        
    def startVirtService(self):
        ret_val=subprocess.call(["/etc/init.d/libvirt-bin", "start"])
        if ret_val==0:
            logging.debug("Host.startVirtService(): libvirtd is successfully started")
            self.__virtProcessPid=getVirtServicePid()
            return True
        else:
            logging.debug("Host.startVirtService(): Failed in starting libvirtd")
            return False
        
    def stopVirtService(self):
        ret_val=subprocess.call(["/etc/init.d/libvirt-bin", "stop"])
        if ret_val==0:
            logging.debug("Host.stopVirtService(): libvirtd is successfully stopped")
            return True
        else:
            logging.debug("Host.startVirtService(): Failed in stopping libvirtd")
            return False
        
    def restartVirtService(self):
        ret_val=subprocess.call(["/etc/init.d/libvirt-bin", "restart"])
        if ret_val==0:
            logging.debug("Host.restartVirtService(): libvirtd is successfully restarted")
            
            self.__virtProcessPid=getVirtServicePid()
	    return True
        else:
            logging.debug("Host.restartVirtService(): Failed in restarting libvirtd")
            return False
        
    def killVirtService(self):
        try:
            self.__virt_process.kill()
        except:
            logging.debug("Host.killVirtService(): Failed in killing libvirtd")
        else:
            logging.debug("Host.killVirtService(): libvirtd is successfully killed")
            
    def getCpuUsage(self):
         logging.debug("Host.getCpuUsage(): Host's cpu usage %s" %self.__cpuUsage)
         return self.__cpuUsage

    def getAgentPid(self):
        logging.debug("Host.getPid(): vm-agent pid %s" %self.__vm_manager_pid)
        return self.__vm_manager_pid
    
    def getLinuxDistroCode(self):
        logging.debug("Host.getLinuxDistroCode(): linux distro code is "+ self.__distroCode)
        return self.__distroCode
    
    def getLinuxDistroName(self):
        logging.debug("Host.getLinuxDistroName(): linux distro name is "+ self.__distroName)
        return self.__distroName
    
    def getLinuxDistroVersion(self):
        logging.debug("Host.getLinuxDistroVersion(): linux distro version is "+ self.__distroVersion)
        return self.__distroVersion
    
    def getFreePhysicalMemory(self):
        logging.debug("Host.getPhysicalMemory(): free physical memory %s" %self.__freePhyMem)
        return self.__freePhyMem
    
    def getFreeVirtualMemory(self):
        logging.debug("Host.getFreeVirtualMemory(): free virtual memory %s" %self.__freeVirtMem)
        return self.__freeVirtMem
    
    def getLinuxKernelVersion(self):
        logging.debug("Host.getLinuxKernelVersion(): linux kernel version "+ self.__linuxKernel_version)
        return self.__linuxKernel_version
    
    def getArchType(self):
        logging.debug("Host.getMachineType(): machine type "+ self.__machine_type)
        return self.__machine_type
    
    def getNetworkName(self):
        logging.debug("Host.getNetworkName(): network name "+ self.__network_name)
        return self.__network_name

    def getProcessCpuUsage(self):
        logging.debug("Host.getProcessCpuUsage(): vm-agent cpu usage "+ self.__proccessCpuUsage)
        return self.__proccessCpuUsage
    
#    def getProcessConnectionSpecs(self):
#        logging.debug("Host.getProcessConnectionSpecs(): vm-agent connection %s" %self.__processConnectionsSpecs)
#        return self.__processConnectionsSpecs
    
    def getProcessMemoryUsage(self):
        logging.debug("Host.getProcessMemoryUsage(): vm-agent memory usage %s"  %self.__processMemUsage)
        return self.__processMemUsage
    
#    def getFiles_OpenedbyProcess(self):
#        logging.debug("Host.getFiles_OpenedbyProcess(): files "+  self.__processOpenedFilesSpecs)
#        return self.__processOpenedFilesSpecs
    
    def getProcessorSpecs(self):
        logging.debug("Host.getProcessorSpecs(): processor "+  self.__processor)
        return self.__processor

    def getAgentUptime(self):
        logging.debug("Host.getAgentUptime(): uptime "+ self.__processUptime)
        return self.__processUptime
        
    def getPythonVersion(self):
        logging.debug("Host.getPythonVersion(): python version "+ self.__python_version)
        return self.__python_version
    
    def getTotalVirtualMemory(self):
        logging.debug("Host.getTotalVirtualMemory(): total virtual memory %s" %self.__totalVirtMem)
        return self.__totalVirtMem
    
    def getUsedPhysicalMemory(self):
        logging.debug("Host. getUsedPhysicalMemory(): used physical memory %s" %self.__usedPhyMem)
        return self.__usedPhyMem
    
#    def getVirtProcessConnectionSpecs(self):
#        logging.debug("Host.getVirtProcessConnectionSpecs(): virt process conn specs "+ self.__virtProcessConnectionsSpecs)
#        return self.__virtProcessConnectionsSpecs
    
    def getVirtProcessCpuUsage(self):
        logging.debug("Host.getVirtProcessCpuUsage(): virt process cpu usage %s"  %self.__virtProcessCpuUsage)
        return self.__virtProcessCpuUsage
    
    def getVirtProcessMemUsage(self):
        logging.debug("Host.getVirtProcessMemUsage(): virt process memory usage %s" %self.__virtProcessMemUsage)
        return self.__virtProcessMemUsage
    
    def getVirtProcessName(self):
        logging.debug("Host.getVirtProcessName(): virt process name "+  self.__virtProcessName)
        return self.__virtProcessName
    
#    def getVirtProcessOpenedFilesSpecs(self):
#        logging.debug("Host.getVirtProcessOpenedFilesSpecs(): virt process opened files specs "+ self.__virtProcessOpenedFilesSpecs)
#        return self.__virtProcessOpenedFilesSpecs
    
    def getVirtProcessId(self):
        logging.debug("Host.getVirtProcessId(): virt process id %s" %self.__virtProcessPid)
        return self.__virtProcessPid
    
#    def getVirtProcessUsername(self):
#        logging.debug("Host.getVirtProcessUsername(): virt process owner name "+ self.__virtProcessUsername)
#        return self.__virtProcessUsername


"""
host=Linux()

for x,y in host.getList().iteritems():
    print x,y

"""



