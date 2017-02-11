
from linux import Linux
from unix import Unix
from windows import Windows

from libvirt_api import libvirtHypervisor
from esx_api import esxHypervisor
from hyperv_api import hyperV_Hypervisor
from vcenter_api import vCenter

import logging

logging.basicConfig(level=logging.DEBUG, filename="/var/log/vm-agent-debug.log", format='%(asctime)s %(levelname)s: %(message)s',datefmt='%Y-%m-%d %H:%M:%S')        

class vmHost:
    def __init__(self):
        self.__conn=libvirtHypervisor()
        self.__hostPtr=Linux()
              
    def getHostSpecsList(self):
        return self.__hostPtr.getList()
    
    def getHypervisorSpecsList(self):
        return self.__conn.getList()
            
    def isConnected(self):
        return self.__conn.isConnected()

    def getHostVirtType(self):
        return self.__conn.getVirtType()
    
    def getHostVirtVersion(self):
        return self.__conn.getVirtVersion()
        
    def getHostVirtLibVersion(self):
        return self.__conn.getVirtLibVersion()
    
    def getHostVirtURI(self):
        return self.__conn.getVirtURI()
    
    def connisEncrypted(self):
        return self.__conn.connisEncrypted()
    
    def connisSecure(self):
        return self.__conn.connisSecure()
    
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
        
    def getGuest(self,guest_id=None,guest_uuid=None,guest_name=None):
        if (guest_id is not None) and (guest_uuid is None) and (guest_name is None):
            return self.__conn.lookUpGuestById(guest_id)
        elif  (guest_uuid is not None) and (guest_id is None) and (guest_name is None):
            return self.__conn.lookUpGuestByUUID(guest_uuid)         
        elif  (guest_name is not None) and (guest_id is None) and (guest_uuid is None):
            return self.__conn.lookUpGuestByName(guest_name)
        
    def getVmDevicesList(self,guest_id=None,guest_uuid=None,guest_name=None):
        return self.getGuest(guest_id, guest_uuid, guest_name).getDevicesList()
        
    def getVmSpecsList(self,guest_id=None,guest_uuid=None,guest_name=None):
        return self.getGuest(guest_id, guest_uuid, guest_name).getSpecsList()
                
    def launchVm(self,guest_id=None,guest_uuid=None,guest_name=None):
        return self.getGuest(guest_id, guest_uuid, guest_name).launch()
            
    def shutdownVm(self,guest_id=None,guest_uuid=None,guest_name=None):
        return self.getGuest(guest_id, guest_uuid, guest_name).shutdown()

    def poweroffVm(self,guest_id=None,guest_uuid=None,guest_name=None):
        return self.getGuest(guest_id, guest_uuid, guest_name).poweroff()
    
    def rebootVm(self,guest_id=None,guest_uuid=None,guest_name=None):
        return self.getGuest(guest_id, guest_uuid, guest_name).reboot()
    
    def VmIsRunning(self,guest_id=None,guest_uuid=None,guest_name=None):
		return self.getGuest(guest_id, guest_uuid, guest_name).isRunning()
    
    def VmIsPersistent(self,guest_id=None,guest_uuid=None,guest_name=None):
		return self.getGuest(guest_id, guest_uuid, guest_name).isPersistent()
    
    def getVmVirtType(self,guest_id=None,guest_uuid=None,guest_name=None):
		return self.getGuest(guest_id, guest_uuid, guest_name).getVirtType()
            
    def getVmId(self,guest_id=None,guest_uuid=None,guest_name=None):
		return self.getGuest(guest_id, guest_uuid, guest_name).getId()
    
    def getVmName(self,guest_id=None,guest_uuid=None,guest_name=None):
		return self.getGuest(guest_id, guest_uuid, guest_name).getName()
    
    def getVmUuid(self,guest_id=None,guest_uuid=None,guest_name=None):
		return self.getGuest(guest_id, guest_uuid, guest_name).getUuid()
    
    def getVmMaxMemory(self,guest_id=None,guest_uuid=None,guest_name=None):
		return self.getGuest(guest_id, guest_uuid, guest_name).getMaxMemory()
    
    def getVmCurrentMemory(self,guest_id=None,guest_uuid=None,guest_name=None):
		return self.getGuest(guest_id, guest_uuid, guest_name).getCurrentMemory() 
    
    def getVmMaxVcpu(self,guest_id=None,guest_uuid=None,guest_name=None):
		return self.getGuest(guest_id, guest_uuid, guest_name).getMaxVcpu()
    
    def getVmCurrentVcpu(self,guest_id=None,guest_uuid=None,guest_name=None):
		return self.getGuest(guest_id, guest_uuid, guest_name).getCurrentVcpu()
    
    def getVmArch(self,guest_id=None,guest_uuid=None,guest_name=None):
		return self.getGuest(guest_id, guest_uuid, guest_name).getArch()

    def getGuestType(self,guest_id=None,guest_uuid=None,guest_name=None):
		return self.getGuest(guest_id, guest_uuid, guest_name).getGuestType()
    
    def getVmBootDevice(self,guest_id=None,guest_uuid=None,guest_name=None):
		return self.getGuest(guest_id, guest_uuid, guest_name).getBootDevice()
    
    def isVmAcpiEnabled(self,guest_id=None,guest_uuid=None,guest_name=None):
		return self.getGuest(guest_id, guest_uuid, guest_name).isAcpiEnabled()
    
    def isVmApicEnabled(self,guest_id=None,guest_uuid=None,guest_name=None):
		return self.getGuest(guest_id, guest_uuid, guest_name).isApicEnabled()
        
    def isVmPaeEnabled(self,guest_id=None,guest_uuid=None,guest_name=None):
		return self.getGuest(guest_id, guest_uuid, guest_name).isPaeEnabled()
    
    def getVmCpuModel(self,guest_id=None,guest_uuid=None,guest_name=None):
		return self.getGuest(guest_id, guest_uuid, guest_name).getCpuModel()
    
    def getVmClockOffset(self,guest_id=None,guest_uuid=None,guest_name=None):
		return self.getGuest(guest_id, guest_uuid, guest_name).getClockOffset()
    
    def getVmActions(self,guest_id=None,guest_uuid=None,guest_name=None):
		return self.getGuest(guest_id, guest_uuid, guest_name).getActions()
    
    def getVmDeviceEmulator(self,guest_id=None,guest_uuid=None,guest_name=None):
		return self.getGuest(guest_id, guest_uuid, guest_name).getDeviceEmulator()
    
    def getVmDisks(self,guest_id=None,guest_uuid=None,guest_name=None):
		return self.getGuest(guest_id, guest_uuid, guest_name).getDisks()
    
    def getVmControllers(self,guest_id=None,guest_uuid=None,guest_name=None):
		return self.getGuest(guest_id, guest_uuid, guest_name).getControllers()
    
    def getVmInterfaces(self,guest_id=None,guest_uuid=None,guest_name=None):
		return self.getGuest(guest_id, guest_uuid, guest_name).getInterfaces()
    
    def getVmSerialConnectors(self,guest_id=None,guest_uuid=None,guest_name=None):
		return self.getGuest(guest_id, guest_uuid, guest_name).getSerialConnectors()
    
    def getVmConsoleTypes(self,guest_id=None,guest_uuid=None,guest_name=None):
		return self.getGuest(guest_id, guest_uuid, guest_name).getConsoleTypes()
    
    def getVmInputs(self,guest_id=None,guest_uuid=None,guest_name=None):
		return self.getGuest(guest_id, guest_uuid, guest_name).getInputs()
    
    def getVmMonitors(self,guest_id=None,guest_uuid=None,guest_name=None):
		return self.getGuest(guest_id, guest_uuid, guest_name).getMonitors()
    
    def getVmSoundCards(self,guest_id=None,guest_uuid=None,guest_name=None):
		return self.getGuest(guest_id, guest_uuid, guest_name).getSoundCards()
    
    def getVmVideoCards(self,guest_id=None,guest_uuid=None,guest_name=None):
		return self.getGuest(guest_id, guest_uuid, guest_name).getVideoCards()
    
    def getVmMemBalloons(self,guest_id=None,guest_uuid=None,guest_name=None):
		return self.getGuest(guest_id, guest_uuid, guest_name).getMemBalloons()
        
    def isVirtServiceRunning(self):
		return self.__hostPtr.isVirtServiceRunning()
        
    def startVirtService(self):
		return self.__hostPtr.startVirtService()
        
    def stopVirtService(self):
		return self.__hostPtr.stopVirtService()
        
    def restartVirtService(self):
		return self.__hostPtr.restartVirtService()
        
    def killVirtService(self):
		return self.__hostPtr.killVirtService()
            
    def getCpuUsage(self):
		return self.__hostPtr.getCpuUsage()

    def getAgentPid(self):
		return self.__hostPtr.getAgentPid()
    
    def getLinuxDistroCode(self):
		return self.__hostPtr.getLinuxDistroCode()
    
    def getLinuxDistroName(self):
		return self.__hostPtr.getLinuxDistroName()
    
    def getLinuxDistroVersion(self):
		return self.__hostPtr.getLinuxDistroVersion()
    
    def getFreePhysicalMemory(self):
		return self.__hostPtr.getFreePhysicalMemory()
    
    def getFreeVirtualMemory(self):
		return self.__hostPtr.getFreeVirtualMemory()
    
    def getLinuxKernelVersion(self):
		return self.__hostPtr.getLinuxKernelVersion()
    
    def getArchType(self):
		return self.__hostPtr.getArchType()
    
    def getNetworkName(self):
		return self.__hostPtr.getNetworkName()

    def getProcessCpuUsage(self):
		return self.__hostPtr.getProcessCpuUsage()
  
    def getProcessMemoryUsage(self):
		return self.__hostPtr.getProcessMemoryUsage()
    
    def getProcessorSpecs(self):
		return self.__hostPtr.getProcessorSpecs()

    def getAgentUptime(self):
		return self.__hostPtr.getAgentUptime()
        
    def getPythonVersion(self):
		return self.__hostPtr.getPythonVersion()
    
    def getTotalVirtualMemory(self):
		return self.__hostPtr.getTotalVirtualMemory()
    
    def getUsedPhysicalMemory(self):
		return self.__hostPtr.getUsedPhysicalMemory()
    
    def getVirtProcessCpuUsage(self):
		return self.__hostPtr.getVirtProcessCpuUsage()
    
    def getVirtProcessMemUsage(self):
		return self.__hostPtr.getVirtProcessMemUsage()
    
    def getVirtProcessName(self):
		return self.__hostPtr.getVirtProcessName()
    
    def getVirtProcessId(self):
		return self.__hostPtr.getVirtProcessId()

		
#host=vmHost()
#
#specs=host.getHostSpecsList()
##
#print "-------host------"
#for x,y in specs.iteritems():
#    print x,y
#    
#specs=host.getHypervisorSpecsList()
#
#print "-------hypervisor------"
#for x,y in specs.iteritems():
#    print x,y
#
#for name in host.getAllVmNames():
#    print "-------guest------"
#    deviceTypes=host.getVmDevicesList(guest_name=name)
#    specs=host.getVmSpecsList(guest_name=name)
#    
#    print "----specs----"
#    for x,y in specs.iteritems():
#        print x,y
#    
#    for deviceType in deviceTypes:   
#        for device in deviceType:
#            print "---device---"
#            for x,y in device.iteritems():
#                print x,y
            




