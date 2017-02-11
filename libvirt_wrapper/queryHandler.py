import xmlrpclib

class queryHandler:
    def __init__(self,name,host,port='4444'): 
        self.name=name
        self.host=host
        self.id=None
        self.port=port
        self.__conn = xmlrpclib.ServerProxy('http://'+self.host+':'+self.port, allow_none=True)
        self.cpuUsage=self.__conn.getCpuUsage()
        self.memUsage=self.__conn.getFreePhysicalMemory()
        self.hostType=self.__conn.getLinuxDistroName()
        self.hostSpecsList=self.__conn.getHostSpecsList()
        self.hypervisorSpecsList=self.__conn.getHypervisorSpecsList()
        
        
    def getHostSpecsList(self):
        return self.__conn.getHostSpecsList()
    
    def getHypervisorSpecsList(self):
        return self.__conn.getHypervisorSpecsList()
            
    def getHostVirtType(self):
        return self.__conn.getHostVirtType()
    
    def getHostVirtVersion(self):
        return self.__conn.getHostVirtVersion()
        
    def getHostVirtLibVersion(self):
        return self.__conn.getHostVirtLibVersion()
    
    def getHostVirtURI(self):
        return self.__conn.getHostVirtURI()
    
    def getNumofActiveVms(self):
        return self.__conn.getNumofActiveVms()
    
    def getNumofInactiveVms(self):
        return self.__conn.getNumofInactiveVms()
    
    def getNumofAllVms(self):
        return self.__conn.getNumofAllVms()
    
    def getActiveVmNames(self):
        return self.__conn.getActiveVmNames()
    
    def getInactiveVmNames(self):
        return self.__conn.getInactiveVmNames()
    
    def getAllVmNames(self):
        return self.__conn.getAllVmNames()

    def getVmDevicesList(self,guest_id=None,guest_uuid=None,guest_name=None):
        if (guest_id is not None) and (guest_uuid is None) and (guest_name is None):
                return self.__conn.getVmDevicesList(guest_id, None, None)
        elif  (guest_uuid is not None) and (guest_id is None) and (guest_name is None):
                return self.__conn.getVmDevicesList(None, guest_uuid, None)    
        elif  (guest_name is not None) and (guest_id is None) and (guest_uuid is None):
                return self.__conn.getVmDevicesList(None, None, guest_name)
        
    def getVmSpecsList(self,guest_id=None,guest_uuid=None,guest_name=None):
        if (guest_id is not None) and (guest_uuid is None) and (guest_name is None):
                return self.__conn.getVmSpecsList(guest_id, None, None)
        elif  (guest_uuid is not None) and (guest_id is None) and (guest_name is None):
                return self.__conn.getVmSpecsList(None, guest_uuid, None)    
        elif  (guest_name is not None) and (guest_id is None) and (guest_uuid is None):
                return self.__conn.getVmSpecsList(None, None, guest_name)

    def launchVm(self,guest_id=None,guest_uuid=None,guest_name=None):
        if (guest_id is not None) and (guest_uuid is None) and (guest_name is None):
                return self.__conn.launchVm(guest_id, None, None)
        elif  (guest_uuid is not None) and (guest_id is None) and (guest_name is None):
                return self.__conn.launchVm(None, guest_uuid, None)    
        elif  (guest_name is not None) and (guest_id is None) and (guest_uuid is None):
                return self.__conn.launchVm(None, None, guest_name)
            
    def shutdownVm(self,guest_id=None,guest_uuid=None,guest_name=None):
        if (guest_id is not None) and (guest_uuid is None) and (guest_name is None):
                return self.__conn.shutdownVm(guest_id, None, None)
        elif  (guest_uuid is not None) and (guest_id is None) and (guest_name is None):
                return self.__conn.shutdownVm(None, guest_uuid, None)    
        elif  (guest_name is not None) and (guest_id is None) and (guest_uuid is None):
                return self.__conn.shutdownVm(None, None, guest_name)

    def poweroffVm(self,guest_id=None,guest_uuid=None,guest_name=None):
        if (guest_id is not None) and (guest_uuid is None) and (guest_name is None):
                return self.__conn.poweroffVm(guest_id, None, None)
        elif  (guest_uuid is not None) and (guest_id is None) and (guest_name is None):
                return self.__conn.poweroffVm(None, guest_uuid, None)    
        elif  (guest_name is not None) and (guest_id is None) and (guest_uuid is None):
                return self.__conn.poweroffVm(None, None, guest_name)
    
    def rebootVm(self,guest_id=None,guest_uuid=None,guest_name=None):
        if (guest_id is not None) and (guest_uuid is None) and (guest_name is None):
                return self.__conn.rebootVm(guest_id, None, None)
        elif  (guest_uuid is not None) and (guest_id is None) and (guest_name is None):
                return self.__conn.rebootVm(None, guest_uuid, None)    
        elif  (guest_name is not None) and (guest_id is None) and (guest_uuid is None):
                return self.__conn.rebootVm(None, None, guest_name)
    
    def VmIsRunning(self,guest_id=None,guest_uuid=None,guest_name=None):
        if (guest_id is not None) and (guest_uuid is None) and (guest_name is None):
                return self.__conn.VmIsRunning(guest_id, None, None)
        elif  (guest_uuid is not None) and (guest_id is None) and (guest_name is None):
                return self.__conn.VmIsRunning(None, guest_uuid, None)    
        elif  (guest_name is not None) and (guest_id is None) and (guest_uuid is None):
                return self.__conn.VmIsRunning(None, None, guest_name)
    
    def VmIsPersistent(self,guest_id=None,guest_uuid=None,guest_name=None):
        if (guest_id is not None) and (guest_uuid is None) and (guest_name is None):
                return self.__conn.VmIsPersistent(guest_id, None, None)
        elif  (guest_uuid is not None) and (guest_id is None) and (guest_name is None):
                return self.__conn.VmIsPersistent(None, guest_uuid, None)    
        elif  (guest_name is not None) and (guest_id is None) and (guest_uuid is None):
                return self.__conn.VmIsPersistent(None, None, guest_name)
    
    def getVmVirtType(self,guest_id=None,guest_uuid=None,guest_name=None):
        if (guest_id is not None) and (guest_uuid is None) and (guest_name is None):
                return self.__conn.getVmVirtType(guest_id, None, None)
        elif  (guest_uuid is not None) and (guest_id is None) and (guest_name is None):
                return self.__conn.getVmVirtType(None, guest_uuid, None)    
        elif  (guest_name is not None) and (guest_id is None) and (guest_uuid is None):
                return self.__conn.getVmVirtType(None, None, guest_name)
            
    def getVmId(self,guest_id=None,guest_uuid=None,guest_name=None):
        if (guest_id is not None) and (guest_uuid is None) and (guest_name is None):
                return self.__conn.getVmId(guest_id, None, None)
        elif  (guest_uuid is not None) and (guest_id is None) and (guest_name is None):
                return self.__conn.getVmId(None, guest_uuid, None)    
        elif  (guest_name is not None) and (guest_id is None) and (guest_uuid is None):
                return self.__conn.getVmId(None, None, guest_name)
    
    def getVmName(self,guest_id=None,guest_uuid=None,guest_name=None):
        if (guest_id is not None) and (guest_uuid is None) and (guest_name is None):
                return self.__conn.getVmName(guest_id, None, None)
        elif  (guest_uuid is not None) and (guest_id is None) and (guest_name is None):
                return self.__conn.getVmName(None, guest_uuid, None)    
        elif  (guest_name is not None) and (guest_id is None) and (guest_uuid is None):
                return self.__conn.getVmName(None, None, guest_name)
    
    def getVmUuid(self,guest_id=None,guest_uuid=None,guest_name=None):
        if (guest_id is not None) and (guest_uuid is None) and (guest_name is None):
                return self.__conn.getVmUuid(guest_id, None, None)
        elif  (guest_uuid is not None) and (guest_id is None) and (guest_name is None):
                return self.__conn.getVmUuid(None, guest_uuid, None)    
        elif  (guest_name is not None) and (guest_id is None) and (guest_uuid is None):
                return self.__conn.getVmUuid(None, None, guest_name)
    
    def getVmMaxMemory(self,guest_id=None,guest_uuid=None,guest_name=None):
        if (guest_id is not None) and (guest_uuid is None) and (guest_name is None):
                return self.__conn.getVmMaxMemory(guest_id, None, None)
        elif  (guest_uuid is not None) and (guest_id is None) and (guest_name is None):
                return self.__conn.getVmMaxMemory(None, guest_uuid, None)    
        elif  (guest_name is not None) and (guest_id is None) and (guest_uuid is None):
                return self.__conn.getVmMaxMemory(None, None, guest_name)
    
    def getVmCurrentMemory(self,guest_id=None,guest_uuid=None,guest_name=None):
        if (guest_id is not None) and (guest_uuid is None) and (guest_name is None):
                return self.__conn.getVmCurrentMemory(guest_id, None, None)
        elif  (guest_uuid is not None) and (guest_id is None) and (guest_name is None):
                return self.__conn.getVmCurrentMemory(None, guest_uuid, None)    
        elif  (guest_name is not None) and (guest_id is None) and (guest_uuid is None):
                return self.__conn.getVmCurrentMemory(None, None, guest_name)
    
    def getVmMaxVcpu(self,guest_id=None,guest_uuid=None,guest_name=None):
        if (guest_id is not None) and (guest_uuid is None) and (guest_name is None):
                return self.__conn.getVmMaxVcpu(guest_id, None, None)
        elif  (guest_uuid is not None) and (guest_id is None) and (guest_name is None):
                return self.__conn.getVmMaxVcpu(None, guest_uuid, None)    
        elif  (guest_name is not None) and (guest_id is None) and (guest_uuid is None):
                return self.__conn.getVmMaxVcpu(None, None, guest_name)
    
    def getVmCurrentVcpu(self,guest_id=None,guest_uuid=None,guest_name=None):
        if (guest_id is not None) and (guest_uuid is None) and (guest_name is None):
                return self.__conn.getVmCurrentVcpu(guest_id, None, None)
        elif  (guest_uuid is not None) and (guest_id is None) and (guest_name is None):
                return self.__conn.getVmCurrentVcpu(None, guest_uuid, None)    
        elif  (guest_name is not None) and (guest_id is None) and (guest_uuid is None):
                return self.__conn.getVmCurrentVcpu(None, None, guest_name)
    
    def getVmArch(self,guest_id=None,guest_uuid=None,guest_name=None):
        if (guest_id is not None) and (guest_uuid is None) and (guest_name is None):
                return self.__conn.getVmArch(guest_id, None, None)
        elif  (guest_uuid is not None) and (guest_id is None) and (guest_name is None):
                return self.__conn.getVmArch(None, guest_uuid, None)    
        elif  (guest_name is not None) and (guest_id is None) and (guest_uuid is None):
                return self.__conn.getVmArch(None, None, guest_name)

    def getGuestType(self,guest_id=None,guest_uuid=None,guest_name=None):
        if (guest_id is not None) and (guest_uuid is None) and (guest_name is None):
                return self.__conn.getGuestType(guest_id, None, None)
        elif  (guest_uuid is not None) and (guest_id is None) and (guest_name is None):
                return self.__conn.getGuestType(None, guest_uuid, None)    
        elif  (guest_name is not None) and (guest_id is None) and (guest_uuid is None):
                return self.__conn.getGuestType(None, None, guest_name)
    
    def getVmBootDevice(self,guest_id=None,guest_uuid=None,guest_name=None):
        if (guest_id is not None) and (guest_uuid is None) and (guest_name is None):
                return self.__conn.getVmBootDevice(guest_id, None, None)
        elif  (guest_uuid is not None) and (guest_id is None) and (guest_name is None):
                return self.__conn.getVmBootDevice(None, guest_uuid, None)    
        elif  (guest_name is not None) and (guest_id is None) and (guest_uuid is None):
                return self.__conn.getVmBootDevice(None, None, guest_name)
    
    def isVmAcpiEnabled(self,guest_id=None,guest_uuid=None,guest_name=None):
        if (guest_id is not None) and (guest_uuid is None) and (guest_name is None):
                return self.__conn.isVmAcpiEnabled(guest_id, None, None)
        elif  (guest_uuid is not None) and (guest_id is None) and (guest_name is None):
                return self.__conn.isVmAcpiEnabled(None, guest_uuid, None)    
        elif  (guest_name is not None) and (guest_id is None) and (guest_uuid is None):
                return self.__conn.isVmAcpiEnabled(None, None, guest_name)
    
    def isVmApicEnabled(self,guest_id=None,guest_uuid=None,guest_name=None):
        if (guest_id is not None) and (guest_uuid is None) and (guest_name is None):
                return self.__conn.isVmApicEnabled(guest_id, None, None)
        elif  (guest_uuid is not None) and (guest_id is None) and (guest_name is None):
                return self.__conn.isVmApicEnabled(None, guest_uuid, None)    
        elif  (guest_name is not None) and (guest_id is None) and (guest_uuid is None):
                return self.__conn.isVmApicEnabled(None, None, guest_name)
        
    def isVmPaeEnabled(self,guest_id=None,guest_uuid=None,guest_name=None):
        if (guest_id is not None) and (guest_uuid is None) and (guest_name is None):
                return self.__conn.isVmPaeEnabled(guest_id, None, None)
        elif  (guest_uuid is not None) and (guest_id is None) and (guest_name is None):
                return self.__conn.isVmPaeEnabled(None, guest_uuid, None)    
        elif  (guest_name is not None) and (guest_id is None) and (guest_uuid is None):
                return self.__conn.isVmPaeEnabled(None, None, guest_name)
    
    def getVmCpuModel(self,guest_id=None,guest_uuid=None,guest_name=None):
        if (guest_id is not None) and (guest_uuid is None) and (guest_name is None):
                return self.__conn.getVmCpuModel(guest_id, None, None)
        elif  (guest_uuid is not None) and (guest_id is None) and (guest_name is None):
                return self.__conn.getVmCpuModel(None, guest_uuid, None)    
        elif  (guest_name is not None) and (guest_id is None) and (guest_uuid is None):
                return self.__conn.getVmCpuModel(None, None, guest_name)
    
    def getVmClockOffset(self,guest_id=None,guest_uuid=None,guest_name=None):
        if (guest_id is not None) and (guest_uuid is None) and (guest_name is None):
                return self.__conn.getVmClockOffset(guest_id, None, None)
        elif  (guest_uuid is not None) and (guest_id is None) and (guest_name is None):
                return self.__conn.getVmClockOffset(None, guest_uuid, None)    
        elif  (guest_name is not None) and (guest_id is None) and (guest_uuid is None):
                return self.__conn.getVmClockOffset(None, None, guest_name)
    
    def getVmActions(self,guest_id=None,guest_uuid=None,guest_name=None):
        if (guest_id is not None) and (guest_uuid is None) and (guest_name is None):
                return self.__conn.getVmActions(guest_id, None, None)
        elif  (guest_uuid is not None) and (guest_id is None) and (guest_name is None):
                return self.__conn.getVmActions(None, guest_uuid, None)    
        elif  (guest_name is not None) and (guest_id is None) and (guest_uuid is None):
                return self.__conn.getVmActions(None, None, guest_name)
    
    def getVmDeviceEmulator(self,guest_id=None,guest_uuid=None,guest_name=None):
        if (guest_id is not None) and (guest_uuid is None) and (guest_name is None):
                return self.__conn.getVmDeviceEmulator(guest_id, None, None)
        elif  (guest_uuid is not None) and (guest_id is None) and (guest_name is None):
                return self.__conn.getVmDeviceEmulator(None, guest_uuid, None)    
        elif  (guest_name is not None) and (guest_id is None) and (guest_uuid is None):
                return self.__conn.getVmDeviceEmulator(None, None, guest_name)
    
    def getVmDisks(self,guest_id=None,guest_uuid=None,guest_name=None):
        if (guest_id is not None) and (guest_uuid is None) and (guest_name is None):
                return self.__conn.getVmDisks(guest_id, None, None)
        elif  (guest_uuid is not None) and (guest_id is None) and (guest_name is None):
                return self.__conn.getVmDisks(None, guest_uuid, None)    
        elif  (guest_name is not None) and (guest_id is None) and (guest_uuid is None):
                return self.__conn.getVmDisks(None, None, guest_name)
    
    def getVmControllers(self,guest_id=None,guest_uuid=None,guest_name=None):
        if (guest_id is not None) and (guest_uuid is None) and (guest_name is None):
                return self.__conn.getVmControllers(guest_id, None, None)
        elif  (guest_uuid is not None) and (guest_id is None) and (guest_name is None):
                return self.__conn.getVmControllers(None, guest_uuid, None)    
        elif  (guest_name is not None) and (guest_id is None) and (guest_uuid is None):
                return self.__conn.getVmControllers(None, None, guest_name)
    
    def getVmInterfaces(self,guest_id=None,guest_uuid=None,guest_name=None):
        if (guest_id is not None) and (guest_uuid is None) and (guest_name is None):
                return self.__conn.getVmInterfaces(guest_id, None, None)
        elif  (guest_uuid is not None) and (guest_id is None) and (guest_name is None):
                return self.__conn.getVmInterfaces(None, guest_uuid, None)    
        elif  (guest_name is not None) and (guest_id is None) and (guest_uuid is None):
                return self.__conn.getVmInterfaces(None, None, guest_name)
    
    def getVmSerialConnectors(self,guest_id=None,guest_uuid=None,guest_name=None):
        if (guest_id is not None) and (guest_uuid is None) and (guest_name is None):
                return self.__conn.getVmSerialConnectors(guest_id, None, None)
        elif  (guest_uuid is not None) and (guest_id is None) and (guest_name is None):
                return self.__conn.getVmSerialConnectors(None, guest_uuid, None)    
        elif  (guest_name is not None) and (guest_id is None) and (guest_uuid is None):
                return self.__conn.getVmSerialConnectors(None, None, guest_name)
    
    def getVmConsoleTypes(self,guest_id=None,guest_uuid=None,guest_name=None):
        if (guest_id is not None) and (guest_uuid is None) and (guest_name is None):
                return self.__conn.getVmConsoleTypes(guest_id, None, None)
        elif  (guest_uuid is not None) and (guest_id is None) and (guest_name is None):
                return self.__conn.getVmConsoleTypes(None, guest_uuid, None)    
        elif  (guest_name is not None) and (guest_id is None) and (guest_uuid is None):
                return self.__conn.getVmConsoleTypes(None, None, guest_name)
            
    def getVmInputs(self,guest_id=None,guest_uuid=None,guest_name=None):
        if (guest_id is not None) and (guest_uuid is None) and (guest_name is None):
                return self.__conn.getVmInputs(guest_id, None, None)
        elif  (guest_uuid is not None) and (guest_id is None) and (guest_name is None):
                return self.__conn.getVmInputs(None, guest_uuid, None)    
        elif  (guest_name is not None) and (guest_id is None) and (guest_uuid is None):
                return self.__conn.getVmInputs(None, None, guest_name)
    
    def getVmMonitors(self,guest_id=None,guest_uuid=None,guest_name=None):
        if (guest_id is not None) and (guest_uuid is None) and (guest_name is None):
                return self.__conn.getVmMonitors(guest_id, None, None)
        elif  (guest_uuid is not None) and (guest_id is None) and (guest_name is None):
                return self.__conn.getVmMonitors(None, guest_uuid, None)    
        elif  (guest_name is not None) and (guest_id is None) and (guest_uuid is None):
                return self.__conn.getVmMonitors(None, None, guest_name)
    
    def getVmSoundCards(self,guest_id=None,guest_uuid=None,guest_name=None):
        if (guest_id is not None) and (guest_uuid is None) and (guest_name is None):
                return self.__conn.getVmSoundCards(guest_id, None, None)
        elif  (guest_uuid is not None) and (guest_id is None) and (guest_name is None):
                return self.__conn.getVmSoundCards(None, guest_uuid, None)    
        elif  (guest_name is not None) and (guest_id is None) and (guest_uuid is None):
                return self.__conn.getVmSoundCards(None, None, guest_name)
    
    def getVmVideoCards(self,guest_id=None,guest_uuid=None,guest_name=None):
        if (guest_id is not None) and (guest_uuid is None) and (guest_name is None):
                return self.__conn.getVmVideoCards(guest_id, None, None)
        elif  (guest_uuid is not None) and (guest_id is None) and (guest_name is None):
                return self.__conn.getVmVideoCards(None, guest_uuid, None)    
        elif  (guest_name is not None) and (guest_id is None) and (guest_uuid is None):
                return self.__conn.getVmVideoCards(None, None, guest_name)
    
    def getVmMemBalloons(self,guest_id=None,guest_uuid=None,guest_name=None):
        if (guest_id is not None) and (guest_uuid is None) and (guest_name is None):
                return self.__conn.getVmMemBalloons(guest_id, None, None)
        elif  (guest_uuid is not None) and (guest_id is None) and (guest_name is None):
                return self.__conn.getVmMemBalloons(None, guest_uuid, None)    
        elif  (guest_name is not None) and (guest_id is None) and (guest_uuid is None):
                return self.__conn.getVmMemBalloons(None, None, guest_name)
              
    def isVirtServiceRunning(self):
        return self.__conn.isVirtServiceRunning()
        
    def startVirtService(self):
        return self.__conn.startVirtService()
        
    def stopVirtService(self):
        return self.__conn.stopVirtService()
        
    def restartVirtService(self):
        return self.__conn.restartVirtService()
        
    def killVirtService(self):
        return self.__conn.killVirtService()
            
    def getCpuUsage(self):
        return self.__conn.getCpuUsage()

    def getAgentPid(self):
        return self.__conn.getAgentPid()
    
    def getLinuxDistroCode(self):
        return self.__conn.getLinuxDistroCode()
    
    def getLinuxDistroName(self):
        return self.__conn.getLinuxDistroName()
    
    def getLinuxDistroVersion(self):
        return self.__conn.getLinuxDistroVersion()
    
    def getFreePhysicalMemory(self):
        return self.__conn.getFreePhysicalMemory()
    
    def getFreeVirtualMemory(self):
        return self.__conn.getFreeVirtualMemory()
    
    def getLinuxKernelVersion(self):
        return self.__conn.getLinuxKernelVersion()
    
    def getArchType(self):
        return self.__conn.getArchType()
    
    def getNetworkName(self):
        return self.__conn.getNetworkName()

    def getProcessCpuUsage(self):
        return self.__conn.getProcessCpuUsage()
  
    def getProcessMemoryUsage(self):
        return self.__conn.getProcessMemoryUsage()
    
    def getProcessorSpecs(self):
        return self.__conn.getProcessorSpecs()

    def getAgentUptime(self):
        return self.__conn.getAgentUptime()
        
    def getPythonVersion(self):
        return self.__conn.getPythonVersion()
    
    def getTotalVirtualMemory(self):
        return self.__conn.getTotalVirtualMemory()
    
    def getUsedPhysicalMemory(self):
        return self.__conn.getUsedPhysicalMemory()
    
    def getVirtProcessCpuUsage(self):
        return self.__conn.getVirtProcessCpuUsage()
    
    def getVirtProcessMemUsage(self):
        return self.__conn.getVirtProcessMemUsage()
    
    def getVirtProcessName(self):
        return self.__conn.getVirtProcessName()
    
    def getVirtProcessId(self):
        return self.__conn.getVirtProcessId()
    
    
    
    
    