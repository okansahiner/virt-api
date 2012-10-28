from libvirt import virDomain, virConnect
from libvirt import open as openHypervisorConnection
import xml.etree.ElementTree as ET

class Host:
    def __init__(self, nodeName):
        self.__nodeName=nodeName
        self.__sock_type="qemu+ssh://root@"+self.__nodeName+"/system"  
        self.__connPtr=None
        self.__hostUUID=None
        self.__hostCpuArch=None
        self.__hostCpuModel=None
        self.__hostCpuVendor=None
        self.__hostCpuTopology=None
        self.__hostMigrationProtocol=None
        self.__hostCpuFeatures=[]
        self.__hostSupportedArch=[]
        self.__hostSupportedDomains=[]

    def parseCapabilitiesInfo(self):
        root=ET.fromstring(self.__connPtr.getCapabilities())

        # list type
        for child in root.iter("feature"):
            self.__hostCpuFeatures.append(child.attrib.values().pop())
        
        self.__hostUUID=root.find("host/uuid").text
        self.__hostCpuArch=root.find("host/cpu/arch").text
        self.__hostCpuModel=root.find("host/cpu/model").text
        self.__hostCpuVendor=root.find("host/cpu/vendor").text
        # dict type
        self.__hostCpuTopology=root.find("host/cpu/topology").attrib
        self.__hostMigrationProtocol=root.find("host/migration_features/uri_transports/uri_transport").text     
        guests=root.findall("guest")
        
        for child in guests:
            #list type
            self.__hostSupportedArch.append(child.find("arch").attrib.values().pop())
            domains=child.findall("arch/domain")
            
            for domain in domains:
                #list type
                self.__hostSupportedDomains.append(domain.attrib.values().pop())
        
        self.__hostSupportedDomains=list(set(self.__hostSupportedDomains))

    
    def openConnection(self):
        self.__connPtr=virConnect
        self.__connPtr=openHypervisorConnection(self.__sock_type)
        
    def closeConnection(self):
        self.__connPtr.close()
        
    def getLibVersion(self):
        return self.__connPtr.getLibVersion()
    
    def getType(self):
        return self.__connPtr.getType()
    
    def getVersion(self):
        return self.__connPtr.getVersion()
    
    def getURI(self):
        return self.__connPtr.getURI()
    
    def getConnisEncreypted(self):
        return self.__connPtr.isEncrypted()
    
    def getConnisSecure(self):
        return self.__connPtr.isSecure()
    
    def getNumofDomains(self):
        return self.__connPtr.numOfDomains()
    
    def getNumofDefinedDomains(self):
        return self.__connPtr.numOfDefinedDomains()
    
    def getNumofAllDomains(self):
        return self.__connPtr.numOfDomains() + self.__connPtr.numOfDefinedDomains()
        
    def getHostUUID(self):
        return self.__hostUUID
    
    def getHostCpuArch(self):
        return self.__hostCpuArch
    
    def getHostCpuModel(self):
        return self.__hostCpuModel
    
    def getHostCpuVendor(self):
        return self.__hostCpuVendor
    
    def getHostCpuFeatures(self):
        return self.__hostCpuFeatures
    
    def getHostCpuTopology(self):
        return self.__hostCpuTopology
    
    def getHostMigrationProtocol(self):
        return self.__hostMigrationProtocol
    
    def getHostVirtualizationSupportedArch(self):
        return self.__hostSupportedArch
    
    def getHostSupportedDomains(self):
        return self.__hostSupportedDomains
    
    def findStoragePoolResources(self):
        return self.__connPtr.findStoragePoolSources(type, srcSpec, flags)
    
    

    

host=Host("10.0.1.153")
host.openConnection()

host.findStoragePoolResources()

host.closeConnection()




        
        