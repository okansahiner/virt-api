from libvirt import virDomain, virConnect, virStorageVol
from libvirt import open as openHypervisorConnection
import xml.etree.ElementTree as ET
import subprocess, uuid, os


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
        self.__storageVolume=None
        
    def getConnectionPtr(self):
        return self.__connPtr
    
    def refresh(self):
        self.parseCapabilitiesInfo() 

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
        self.__storageVolume=virStorageVol(self.__connPtr)
        
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
    
    def getFreeMemory(self):
        return self.__connPtr.getFreeMemory()/1024
    
    def getHypervisorType(self):
        return self.__connPtr.getType()
    
    def getURI(self):
        return self.__connPtr.getURI()

    def checkConnection(self):
        return self.__connPtr.isAlive()
    
    def listNetworkFilters(self):
        return self.__connPtr.listNWFilters()
    
    def listSecrets(self):
        return self.__connPtr.listSecrets()
    
    def numOfInactiveDomains(self):
        return self.__connPtr.numOfDefinedDomains()
    
    def numOfDefinedInterfaces(self):
        return self.__connPtr.numOfDefinedInterfaces()
    
    def numOfDefinedNetworks(self):
        return self.__connPtr.numOfDefinedNetworks()
    
    def numOfDefinedStoragePools(self):
        return self.__connPtr.numOfDefinedStoragePools()
    
    def numOfActiveDomains(self):
        return self.__connPtr.numOfDomains()
    
    def numOfInterfaces(self):
        return self.__connPtr.numOfInterfaces()
    
    def numOfNetworkFilters(self):
        return self.__connPtr.numOfNWFilters()
    
    def numOfNetworks(self):
        return self.__connPtr.numOfNetworks()
    
    def numOfSecrets(self):
        return self.__connPtr.numOfSecrets()
    
    def numOfStoragePools(self):
        return self.__connPtr.numOfStoragePools()
    
    def getHardwareInfo(self):
        return self.__connPtr.getInfo()
    
    def listDefinedDomains(self):
        return self.__connPtr.listDefinedDomains()
    
    def listDefinedInterfaces(self):
        return self.__connPtr.listDefinedInterfaces()

    def listDefinedNetworks(self):
        return self.__connPtr.listDefinedNetworks()

    def listDefinedStoragePools(self):
        return self.__connPtr.listDefinedStoragePools()

    def listDomainsID(self):
        return self.__connPtr.listDomainsID()
    
    def listInterfaces(self):
        return self.__connPtr.listInterfaces()

    def listNetworks(self):
        return self.__connPtr.listNetworks()
    
    def listStoragePools(self):
        return self.__connPtr.listStoragePools()
    
    def createVM(self, vm_name, vm_cpu, vm_ram ,disk_type, disk_path, disk_size):
        
        domUuid=uuid.uuid4()
        disk_fullpath=disk_path + "/" +vm_name +"/"+vm_name+".qcow2"
        dir=os.path.dirname(disk_fullpath)                    
        subprocess.call(['ssh','root@'+self.__nodeName,'mkdir','-p',dir])

        kvmXmlString="""<domain type='kvm'>
          <name>"""+vm_name+"""</name>
          <uuid>"""+str(domUuid)+"""</uuid>
          <memory>"""+str(vm_ram * 1024)+"""</memory>
          <currentMemory>"""+vm_cpu+"""</currentMemory>
          <vcpu>1</vcpu>
          <os>
            <type arch='x86_64' machine='pc-1.0'>hvm</type>
            <boot dev='hd'/>
          </os>
          <features>
            <acpi/>
            <apic/>
            <pae/>
          </features>
          <clock offset='utc'/>
          <on_poweroff>destroy</on_poweroff>
          <on_reboot>restart</on_reboot>
          <on_crash>restart</on_crash>
          <devices>
            <emulator>/usr/bin/kvm</emulator>
            <disk type='file' device='disk'>
              <driver name='qemu' type='raw'/>
              <source file='"""+disk_fullpath+"""'/>
              <target dev='vda' bus='virtio'/>
              <address type='pci' domain='0x0000' bus='0x00' slot='0x05' function='0x0'/>
            </disk>
            <interface type='bridge'>
              <mac address='52:54:00:70:e6:52'/>
              <source bridge='br0'/>
              <model type='virtio'/>
              <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>
            </interface>
            <serial type='pty'>
              <target port='0'/>
            </serial>
            <console type='pty'>
              <target type='serial' port='0'/>
            </console>
            <input type='mouse' bus='ps2'/>
            <graphics type='vnc' port='-1' autoport='yes'/>
            <sound model='ich6'>
              <address type='pci' domain='0x0000' bus='0x00' slot='0x04' function='0x0'/>
            </sound>
            <video>
              <model type='cirrus' vram='9216' heads='1'/>
              <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x0'/>
            </video>
            <memballoon model='virtio'>
              <address type='pci' domain='0x0000' bus='0x00' slot='0x06' function='0x0'/>
            </memballoon>
          </devices>
        </domain>
        """
        
        qemuXmlString="""<domain type='qemu'>
          <name>"""+vm_name+"""</name>
          <uuid>"""+ str(domUuid) +"""</uuid>
          <memory>"""+ str(vm_ram * 1024)+"""</memory>
          <currentMemory>262144</currentMemory>
          <vcpu>"""+vm_cpu+"""</vcpu>
          <os>
            <type arch='x86_64' machine='pc-1.0'>hvm</type>
            <boot dev='hd'/>
          </os>
          <features>
            <acpi/>
            <apic/>
            <pae/>
          </features>
          <clock offset='utc'/>
          <on_poweroff>destroy</on_poweroff>
          <on_reboot>restart</on_reboot>
          <on_crash>restart</on_crash>
          <devices>
            <emulator>/usr/bin/qemu-system-x86_64</emulator>
            <disk type='file' device='disk'>
              <driver name='qemu' type='raw'/>
              <source file='"""+disk_fullpath+"""'/>
              <target dev='hda' bus='ide'/>
              <address type='drive' controller='0' bus='0' unit='0'/>
            </disk>
            <disk type='block' device='cdrom'>
              <driver name='qemu' type='raw'/>
              <target dev='hdc' bus='ide'/>
              <readonly/>
              <address type='drive' controller='0' bus='1' unit='0'/>
            </disk>
            <controller type='ide' index='0'>
              <address type='pci' domain='0x0000' bus='0x00' slot='0x01' function='0x1'/>
            </controller>
            <interface type='network'>
              <mac address='52:54:00:7e:bb:0f'/>
              <source network='default'/>
              <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>
            </interface>
            <serial type='pty'>
              <target port='0'/>
            </serial>
            <console type='pty'>
              <target type='serial' port='0'/>
            </console>
            <input type='mouse' bus='ps2'/>
            <graphics type='vnc' port='-1' autoport='yes'/>
            <sound model='ich6'>
              <address type='pci' domain='0x0000' bus='0x00' slot='0x04' function='0x0'/>
            </sound>
            <video>
              <model type='cirrus' vram='9216' heads='1'/>
              <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x0'/>
            </video>
            <memballoon model='virtio'>
              <address type='pci' domain='0x0000' bus='0x00' slot='0x05' function='0x0'/>
            </memballoon>
          </devices>
        </domain>
        """
        
        subprocess.call(['ssh','root@'+self.__nodeName,
                         'qemu-img', 'create','-f',disk_type,disk_fullpath,str(disk_size*1024)])
        self.__connPtr.defineXML(kvmXmlString)
        
    def getGuestPtr(self,guestName):
        return self.__connPtr.lookupByName(guestName)


host=Host("10.0.1.50")

host.openConnection()
host.refresh()

ptr=host.getConnectionPtr()

vm_name="my_vm1"
vm_cpu="1"
vm_ram=256
disk_type="qcow2"
disk_path="/share"
disk_size=1


host.createVM(vm_name, vm_cpu, vm_ram, disk_type, disk_path, disk_size)

host.closeConnection()



        
        