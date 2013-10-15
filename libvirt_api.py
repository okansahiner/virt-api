# libvirt api for kvm
# you need libvirt-bin and python-libvirt package installed
# tested on ubuntu 12.04.3 server, libvirtd version 0.9.8
#

from libvirt import *
from libvirt import open as openconn
import xml.etree.ElementTree as xml
import logging
from io import open as openfile
import config_parser

agentConf=config_parser.agentConfig()


def isAgentDebuggingEnabled():
	return agentConf.isDebuggingEnabled()

def getAgentDebuggingPath():
	return agentConf.getDebuggingPath()

def getAgentIp():
	return agentConf.getListeningIp()

def getAgentPort():
	return agentConf.getListeningPort()

def getAgentErrorLogPath():
	return agentConf.getErrorLoggingPath()

if agentConf.isDebuggingEnabled():
	debugPath=agentConf.getDebuggingPath()
	logging.basicConfig(level=logging.DEBUG, filename=debugPath, format='%(asctime)s %(levelname)s: %(message)s',datefmt='%Y-%m-%d %H:%M:%S')        


def getVirtServicePid():
    logging.debug(" getLibvirtServicePid(): Getting libvirtd pid from pid file")
    try:
        pidFile=openfile('/var/run/libvirtd.pid','r')
    except:
        logging.debug(" getLibvirtServicePid(): Failed in reading libvirtd pid file")
        return None
    else:
        pid=int(pidFile.readline())
        logging.debug(" getLibvirtServicePid(): libvirtd pid %s" %pid)
        pidFile.close()
        return pid
    
class Guest:
    def __init__(self, virDom, isSecure):
        logging.debug("Guest.constructor(): New Guest Constructor invoked")
        self.__virDomPointer=virDomain
        self.__virDomPointer=virDom
        try:
            self.__xmlFile= self.__virDomPointer.XMLDesc(isSecure)
        except:
            logging.debug("Guest.constructor(): Failed in parsing XML string for Guest")
        else:
            logging.debug("Guest.constructor(): Guest XML string successfully parsed")   
            
        self.__virtType=None
        self.__id=None
        self.__name=None
        self.__uuid=None
        self.__maxMemory=None
        self.__currentMemory=None
        self.__maxVcpu=None
        self.__currentVcpu=None
        self.__osArch=None
        self.__guestType=None
        self.__bootDevice=None
        self.__status="unknown"
        self.__acpi=None
        self.__apic=None
        self.__pae=None
        self.__cpuModel=None
        self.__clockOffset=None
        self.__actions={}
        self.__deviceEmulator=None
        self.__disks=[]
        self.__controllers=[]
        self.__interfaces=[]
        self.__serialConnectors=[]
        self.__consoles=[]
        self.__inputs=[]
        self.__monitors=[]
        self.__soundCards=[]
        self.__videoCards=[]
        self.__memBaloons=[]
        self.__guestSpecs={}
        self.__guestDevices=[]
        self.initialize()
        self.setList()
                
    def setStatus(self, status):
        logging.debug("Guest.setStatus(): Guest status is changed as " + self.__status)  
        self.__status=status
        self.__guestSpecs["status"]=self.__status
        
    def getSpecsList(self):
        logging.debug("Guest.getList(): Guest specs list returned")  
        return self.__guestSpecs
    
    def getDevicesList(self):
        logging.debug("Guest.getList(): Guest devices list returned")  
        return self.__guestDevices
        
    def setList(self):
        logging.debug("Guest.setList(): Guest specs setting from values")
        self.__guestSpecs["status"]=self.__status  
        self.__guestSpecs[" virtualization type"]=self.__virtType
        self.__guestSpecs["id"]=self.__id
        self.__guestSpecs["name"]=self.__name
        self.__guestSpecs["uuid"]=self.__uuid
        self.__guestSpecs["maximum memory"]=self.__maxMemory
        self.__guestSpecs["current memory"]=self.__currentMemory
        self.__guestSpecs["max virtual cpu"]=self.__maxVcpu
        self.__guestSpecs["current virtual cpu"]=self.__currentVcpu
        self.__guestSpecs["os arch"]=self.__osArch
        self.__guestSpecs["guest type"]=self.__guestType
        self.__guestSpecs["boot device"]=self.__bootDevice
        self.__guestSpecs["acpi enabled"]=self.__acpi
        self.__guestSpecs["apic enabled"]=self.__apic
        self.__guestSpecs["pae enabled"]=self.__pae
        self.__guestSpecs["cpu model"]=self.__cpuModel
        self.__guestSpecs["clock offset"]=self.__clockOffset
        self.__guestSpecs['action on power off']=self.__actions['on power off']
        self.__guestSpecs['action on reboot']=self.__actions['on reboot']
        self.__guestSpecs['action on reboot']=self.__actions['on crash']
        self.__guestSpecs["device emulator"]=self.__deviceEmulator
        self.__guestDevices.append(self.__disks)
        self.__guestDevices.append(self.__monitors)
        self.__guestDevices.append(self.__videoCards)
        self.__guestDevices.append(self.__inputs)
        self.__guestDevices.append(self.__interfaces)
        self.__guestDevices.append(self.__soundCards)
        self.__guestDevices.append(self.__controllers)
        self.__guestDevices.append(self.__interfaces)        
          
    def initialize(self):
        logging.debug(" Guest.initialize(): initializing Guest entries")
        xmlstr=xml.fromstring(self.__xmlFile)
        self.__virtType=xmlstr.get("type")
        self.__id=xmlstr.get("id")
        self.__name=xmlstr.find("name").text
        self.__uuid=xmlstr.find("uuid").text
        self.__maxMemory=int(xmlstr.find("memory").text)/1024
        self.__currentMemory=int(xmlstr.find("currentMemory").text)/1024
        self.__maxVcpu=xmlstr.find("vcpu").text
        self.__currentVcpu=xmlstr.find("vcpu").get("current")
        if self.__currentVcpu==None: self.__currentVcpu=self.__maxVcpu
        self.__guestType=xmlstr.find("os/type").text
        self.__osArch=xmlstr.find("os/type").get("arch")
        self.__bootDevice=xmlstr.find("os/boot").get("dev")
        
        if xmlstr.find("features/acpi") is not None: self.__acpi=True
        else: self.__acpi=False
        if xmlstr.find("features/apic") is not None: self.__apic=True
        else: self.__apic=False
        if xmlstr.find("features/pae") is not None: self.__pae=True
        else: self.__pae=False
        if xmlstr.find("cpu") is not None: self.__cpuModel=xmlstr.find("cpu/model").text
        else: self.__cpuModel="Same with Host"
        
        self.__clockOffset=xmlstr.find("clock").get("offset")
        self.__actions['on power off']=xmlstr.find("on_poweroff").text
        self.__actions['on reboot']=xmlstr.find("on_reboot").text
        self.__actions['on crash']=xmlstr.find("on_crash").text
        self.__deviceEmulator=xmlstr.find("devices/emulator").text
        
        for device in xmlstr.find("devices"):            
            if device.tag=="disk":
                disk={}
                disk['disk type']=device.get("type")
                disk['device']=device.get("device")
                disk['driver name']=device.find("driver").get("name")
                disk['extension']=device.find("driver").get("type")
                if device.find("source") is not None: 
                    disk['source file']=device.find("source").get("file")
                disk['target device']=device.find("target").get("dev")
                disk['target bus']=device.find("target").get("bus")
                if device.find("address") is not None:
                    disk['address type']=device.find("address").get("type")
                    disk['address domain']=device.find("address").get("domain")
                    disk['address bus']=device.find("address").get("bus")
                    disk['address slot']=device.find("address").get("slot")
                    disk['address function']=device.find("address").get("function")
                self.__disks.append(disk)
            
            if device.tag=="controller":
                controller={}
                controller['controller type']=device.get("type")
                controller['controller index']=device.get("index")
                if device.find("address") is not None:
                    controller['address type']=device.find("address").get("type")
                    controller['address domain']=device.find("address").get("domain")
                    controller['address bus']=device.find("address").get("bus")
                    controller['address slot']=device.find("address").get("slot")
                    controller['address function']=device.find("address").get("function")
                self.__controllers.append(controller)
                
            if device.tag=="interface":
                interface={}
                interface['interface type']=device.get("type")
                interface['mac address']=device.find("mac").get("address")
                interface['source network']=device.find("source").get("network")
                if device.find("model") is not None:
                    interface['model type']=device.find("model").get("type")
                if device.find("address") is not None:
                    interface['address type']=device.find("address").get("type")
                    interface['address domain']=device.find("address").get("domain")
                    interface['address bus']=device.find("address").get("bus")
                    interface['address slot']=device.find("address").get("slot")
                    interface['address function']=device.find("address").get("function")
                self.__interfaces.append(interface)
            
            if device.tag=="serial":
                serialConnector={}
                serialConnector['serial connector type']=device.get("type")
                serialConnector['port']=device.find("target").get("port")
                self.__serialConnectors.append(serialConnector)

            if device.tag=="console":
                console={}
                console['console type']=device.get("type")
                console['connection type']=device.find("target").get("type")
                console['connection port']=device.find("target").get("port")
                self.__consoles.append(console)
            
            if device.tag=="input":
                input_={}
                input_['input type']=device.get("type")
                input_['bus']=device.get("bus")
                self.__inputs.append(input_)
                
            if device.tag=="graphics":
                graphic={}
                graphic['monitor type']=device.get("type")
                graphic['monitor port']=device.get("port")
                if device.get("autoport")=="yes": graphic['autoport enabled']=True
                else: graphic['autoport enabled']=False
                self.__monitors.append(graphic)
                
            if device.tag=="sound":
                soundCard={}
                soundCard['sound card model']=device.get("model")
                if device.find("address") is not None:
                    soundCard['sound card type']=device.find('address').get("type")
                    soundCard['address domain']=device.find("address").get("domain")
                    soundCard['address bus']=device.find("address").get("bus")
                    soundCard['address slot']=device.find("address").get("slot")
                    soundCard['address function']=device.find("address").get("function")
                self.__soundCards.append(soundCard)
                
            if device.tag=="video":
                videoCard={}
                videoCard["video card model"]=device.find("model").get("type")
                videoCard["video ram"]=device.find("model").get("vram")
                videoCard["video card heads"]=device.find("model").get("heads")
                if device.find("address") is not None:
                    videoCard['address type']=device.find("address").get("type")
                    videoCard['address domain']=device.find("address").get("domain")
                    videoCard['address bus']=device.find("address").get("bus")
                    videoCard['address slot']=device.find("address").get("slot")
                    videoCard['address function']=device.find("address").get("function")
                self.__videoCards.append(videoCard)
                
            if device.tag=="memballoon":
                memBalloon={}
                memBalloon['memory ballooning model']=device.get('model')
                if device.find("address") is not None:
                    memBalloon['address type']=device.find("address").get("type")
                    memBalloon['address domain']=device.find("address").get("domain")
                    memBalloon['address bus']=device.find("address").get("bus")
                    memBalloon['address slot']=device.find("address").get("slot")
                    memBalloon['address function']=device.find("address").get("function")
                self.__memBaloons.append(memBalloon)
                
    def launch(self):
        try:
            ret_val=self.__virDomPointer.create()
        except:
            logging.debug("Guest.launch(): failed in starting guest " + self.__name)
        else:
            logging.debug("Guest.launch(): started guest " + self.__name)
        return ret_val
    
    def shutdown(self):
        try:
            ret_val=self.__virDomPointer.shutdown()
        except:
            logging.debug("Guest.shutdown(): failed in shutting down guest " + self.__name)
        else:
            logging.debug("Guest.shutdown(): shut down guest " + self.__name)
        return ret_val
    
    def poweroff(self):
        try:
            ret_val=self.__virDomPointer.destroy()
        except:
            logging.debug("Guest.poweroff(): failed in powering off guest " + self.__name)
        else:
            logging.debug("Guest.poweroff(): power off guest " + self.__name)
        return ret_val
    
    def reboot(self):
        try:
            ret_val=self.__virDomPointer.reboot(VIR_DOMAIN_EVENT_ID_REBOOT)
        except:
            logging.debug("Guest.reboot(): failed in shutting down guest " + self.__name)
        else:
            logging.debug("Guest.reboot(): shut down guest " + self.__name)
        return ret_val
    
    def isRunning(self):
        try:
            ret_val=self.__virDomPointer.isActive()
        except:            
            logging.debug("Guest.isRunning(): checking "+ self.__name+ " failed ")
        else:
            logging.debug("Guest.isRunning(): checked "+ self.__name+ " state, "+ str(ret_val))
        return ret_val
    
    def isPersistent(self):
        try:
            ret_val=self.__virDomPointer.isPersistent()
        except:
            logging.debug("Guest.isPersistent(): checked "+ self.__name+ " failed ")
        else:
            logging.debug("Guest.isPersistent(): checked "+ self.__name+ " persistency, "+str(ret_val))
        return ret_val
    
    def getVirtType(self):
        logging.debug("Guest.getVirtType(): "+self.__name+" virtualization type "+self.__virtType)
        return self.__virtType
            
    def getId(self):
        logging.debug("Guest.getId(): "+self.__name+" id "+str(self.__id))
        return self.__id
    
    def getName(self):
        logging.debug("Guest.getName(): name "+self.__name)
        return self.__name
    
    def getUuid(self):
        logging.debug("Guest.getUuid(): uuid "+self.__uuid)
        return self.__uuid
    
    def getMaxMemory(self):
        logging.debug("Guest.getMaxMemory(): "+ self.__name+" max memory %s" %self.__maxMemory)
        return self.__maxMemory
    
    def getCurrentMemory(self):
        logging.debug("Guest.getCurrentMemory(): "+self.__name+" current memory %s" %self.__currentMemory)
        return self.__currentMemory
    
    def getMaxVcpu(self):
        logging.debug("Guest.getMaxVcpu(): "+self.__name+" max vcpu "+self.__maxVcpu)
        return self.__maxVcpu
    
    def getCurrentVcpu(self):
        logging.debug("Guest.getCurrentVcpu(): "+self.__name+" current vcpu "+self.__currentVcpu)
        return self.__currentVcpu
    
    def getArch(self):
        logging.debug("Guest.getArch(): "+self.__name+" arch "+self.__osArch)
        return self.__osArch

    def getGuestType(self):
        logging.debug("Guest.getGuestType(): "+self.__name+" guest type "+self.__guestType)
        return self.__guestType
    
    def getBootDevice(self):
        logging.debug("Guest.getBootDevice(): "+self.__name+" boot dev "+self.__bootDevice)
        return self.__bootDevice
    
    def isAcpiEnabled(self):
        logging.debug("Guest.isAcpiEnabled(): "+self.__name+" acpi enabled "+str(self.__acpi))
        return self.__acpi
    
    def isApicEnabled(self):
        logging.debug("Guest.isApicEnabled(): "+self.__name+" apic enabled "+str(self.__apic))
        return self.__apic
        
    def isPaeEnabled(self):
        logging.debug("Guest.isPaeEnabled(): "+self.__name+" apic enabled "+str(self.__apic))
        return self.__pae
    
    def getCpuModel(self):
        logging.debug("Guest.getCpuModel(): "+self.__name+" cpu model "+self.__cpuModel)
        return self.__cpuModel
    
    def getClockOffset(self):
        logging.debug("Guest.getClockOffset(): "+self.__name+" clock offset "+self.__clockOffset)
        return self.__clockOffset
    
    def getActions(self):
        logging.debug("Guest.getActions(): "+self.__name+" actions on power button "+str(self.__actions))
        return self.__actions
    
    def getDeviceEmulator(self):
        logging.debug("Guest.getDeviceEmulator(): "+self.__name+" device emulator "+self.__deviceEmulator)
        return self.__deviceEmulator
    
    def getDisks(self):
        logging.debug("Guest.getDisks(): "+self.__name+" disks "+str(self.__disks))
        return self.__disks
    
    def getControllers(self):
        logging.debug("Guest.getControllers(): "+self.__name+" controllers "+str(self.__controllers))
        return self.__controllers
    
    def getInterfaces(self):
        logging.debug("Guest.getInterfaces(): "+self.__name+" interfaces "+str(self.__interfaces))
        return self.__interfaces
    
    def getSerialConnectors(self):
        logging.debug("Guest.getSerialConnectors(): "+self.__name+" serial connectors "+str(self.__serialConnectors))
        return self.__serialConnectors
    
    def getConsoleTypes(self):
        logging.debug("Guest.getConsoleTypes(): "+self.__name+" console types "+str(self.__consoles))
        return self.__consoles
    
    def getInputs(self):
        logging.debug("Guest.getInputs(): "+self.__name+" input types "+str(self.__inputs))
        return self.__inputs
    
    def getMonitors(self):
        logging.debug("Guest.getMonitors(): "+self.__name+" monitor types "+str(self.__monitors))
        return self.__monitors
    
    def getSoundCards(self):
        logging.debug("Guest.getSoundCards(): "+self.__name+" sound cards "+str(self.__soundCards))
        return self.__soundCards
    
    def getVideoCards(self):
        logging.debug("Guest.getVideoCards(): "+self.__name+" video cards "+str(self.__videoCards))
        return self.__videoCards
    
    def getMemBalloons(self):
        logging.debug("Guest.getMemBalloons(): "+self.__name+" memory ballooning "+str(self.__memBaloons))
        return self.__memBaloons


class libvirtHypervisor:
    def __init__(self):
        logging.debug(" libvirtHypervisor.constructor(): libvirt hypervisor invoked")
        self.__sock_type='qemu:///system'
        self.__conn=None
        self.__numOfActiveGuests=None
        self.__numOfInactiveGuests=None
        self.__numOfAllGuests=None
        self.__activeGuestPtrList=[]
        self.__inactiveGuestPtrList=[]
        self.__allGuestPtrList=[]
        self.__live_migration=None
        self.__uri_transport_models=[]
        self.__virt_type=None
        self.__virt_version=None
        self.__virt_libversion=None
        self.__virt_uri=None
        self.__virt_isEncrypted=None
        self.__virt_isSecure=None
        self.__hypervisorList={}
        self.initialize()
          
    def getList(self):
        logging.debug(" libvirtHypervisor.getList(): getting hypervisor specs list")
        return self.__hypervisorList
    
    def initialize(self):
        self.openConnection()
        logging.debug(" libvirtHypervisor.initialize(): initializing Hypervisor entries")
        
        self.__virt_type=self.__conn.getType()
        #self.__virt_version=self.__conn.getVersion()
        self.__virt_libversion=self.__conn.getLibVersion()
        self.__virt_uri=self.__conn.getURI()
        self.__virt_isEncrypted=self.__conn.isEncrypted()
        self.__virt_isSecure=self.__conn.isSecure()
        self.__numOfActiveGuests=self.__conn.numOfDomains()
        self.__numOfInactiveGuests=self.__conn.numOfDefinedDomains()
        self.__numOfAllGuests=self.__numOfActiveGuests+self.__numOfInactiveGuests
        self.parseXML()
                    
        for i in self.__conn.listDomainsID():
            ptr=self.__conn.lookupByID(i)
            guest=Guest(ptr, self.__virt_isSecure)
            guest.setStatus("running")
            self.__activeGuestPtrList.append(guest)
            self.__allGuestPtrList.append(guest)

        for i in self.__conn.listDefinedDomains():
            ptr=self.__conn.lookupByName(i)
            guest=Guest(ptr, self.__virt_isSecure)
            guest.setStatus("powered off")
            self.__inactiveGuestPtrList.append(guest)
            self.__allGuestPtrList.append(guest)
            
        self.closeConnection()
        self.setlist()
        
    def setlist(self):
        logging.debug(" libvirtHypervisor.getHypservisorSpecs(): Setting Hypervisor Spec list " )
        self.__hypervisorList['socket type']=self.__sock_type
        self.__hypervisorList['number of running guests']=self.__numOfActiveGuests
        self.__hypervisorList['number of powered off guests']= self.__numOfInactiveGuests
        self.__hypervisorList['number of all guests']=self.__numOfAllGuests
        if self.__live_migration is True:
            self.__hypervisorList['live migration supported?']="yes"
        elif self.__live_migration is False:
            self.__hypervisorList['live migration supported?']="no"
        else:
            self.__hypervisorList['live migration supported?']="unknown"
            
        self.__hypervisorList['URI transport model']=self.__uri_transport_models
        self.__hypervisorList['virtualization type']=self.__virt_type
        #self.__hypervisorList['virtualization version']=self.__virt_version
        self.__hypervisorList['virtualization library version']=self.__virt_libversion
        self.__hypervisorList['URI type']=self.__virt_uri
        if self.__virt_isEncrypted == 0:
            self.__hypervisorList['hypervisor connection is encrypted']="no"
        elif self.__virt_isEncrypted == 1:
            self.__hypervisorList['hypervisor connection is encrypted']="yes"
        else:
            self.__hypervisorList['hypervisor connection is encrypted']="unknown"
            
        if self.__virt_isSecure == 0:
            self.__hypervisorList['hypervisor connection is secure?']="no"
        elif self.__virt_isSecure ==1:
            self.__hypervisorList['hypervisor connection is secure?']="yes"
        else:
            self.__hypervisorList['hypervisor connection is secure?']="unknown"          

        
    def parseXML(self):
        capsxml=xml.fromstring(self.__conn.getCapabilities())
        
        features=capsxml.findall("host/migration_features")
        for feature in features:
            if feature.find("live") is not None: self.__live_migration=True
            else: self.__live_migration=False
        
        features=capsxml.findall("host/migration_features/uri_transports")
        for feature in features:
            self.__uri_transport_models.append(feature.find("uri_transport").text)
        
        logging.debug(" libvirtHypervisor.parseXML(): Hypervisor XML parsed " )
            
    def getHypservisorSpecs(self):
        logging.debug(" libvirtHypervisor.getHypservisorSpecs(): Returned Hypervisor spec list " )
        return self.__hypervisorList
                
    def openConnection(self):
        if self.__conn ==None: 
            self.__conn=virConnect
            try:
                self.__conn=openconn(self.__sock_type)
            except:
                logging.debug(" libvirtHypervisor.openConnection(): failed in connecting to " + self.__sock_type)
            else:
                logging.debug(" libvirtHypervisor.openConnection(): successfully connected to " + self.__sock_type)
        else: 
            logging.debug(" libvirtHypervisor.openConnection(): already connected to " + self.__sock_type)
        
    def getInfo(self):
        return self.__conn.getInfo()

    def closeConnection(self):
        if not self.__conn ==None:
            logging.debug(" libvirtHypervisor.closeConnection(): closing connection " + self.__sock_type)
            try:
                self.__conn.close()
            except:
                logging.debug(" libvirtHypervisor.closeConnection(): failed in closing connection " + self.__sock_type)
            else:
                self.__conn=None
        else: 
            logging.debug(" libvirtHypervisor.closeConnection(): connection already closed with " + self.__sock_type)
    
    def isConnected(self):
        if self.__conn==None:
            logging.debug( "libvirtHypervisor.isConnected(): there is no connection to " +self.__sock_type +" hypervisor") 
            return False
        else:
            logging.debug("libvirtHypervisor.isConnected(): there is a connection to " +self.__sock_type +" hypervisor" )
            return True
        
#    def getGuestsFreeMemory(self):
#        startCell=self.__conn.lookupByName('deneme_vm')
#        return self.__conn.getCellsFreeMemory(startCell, 1)
    
    def getVirtType(self):
        logging.debug( "libvirtHypervisor.getVirtType(): virtualization type: " + self.__virt_type)
        return self.__virt_type
    
    def getVirtVersion(self):
        logging.debug("libvirtHypervisor.getVirtVersion: virtualization version: %s" %self.__virt_version)
        return self.__virt_version
        
    def getVirtLibVersion(self):
        logging.debug("libvirtHypervisor.getVirtLibVersion(): virtualization library version: %s"  %self.__virt_libversion)
        return self.__virt_libversion
    
    def getVirtURI(self):
        logging.debug("libvirtHypevisor.getVIrtURI(): Uniform Resource Identifier: " +self.__sock_type)
        return self.__virt_uri
    
    def connisEncrypted(self):
        logging.debug("libvirtHypevisor.connisEncrypted(): %s" %self.__virt_isEncrypted)
        return self.__virt_isEncrypted
    
    def connisSecure(self):
        logging.debug("libvirtHypevisor.connisSecure(): %s" %self.__virt_isSecure)
        return self.__virt_isSecure
    
    def lookUpGuestByName(self, name):
        for guest in self.__allGuestPtrList:
            if guest.getName()==name:
                logging.debug("libvirtHypevisor.lookUpGuestByName(): "+ name )
                return guest
        logging.debug( "libvirtHypevisor.lookUpGuestByName(): "+ name + " not found" )
        return None
    
    def lookUpGuestById(self, vm_id):
        for guest in self.__activeGuestPtrList:
            if guest.getId()==vm_id:
                logging.debug("libvirtHypevisor.lookUpGuestById(): "+ vm_id )    
                return guest
        logging.debug( "libvirtHypevisor.lookUpGuestById(): "+ vm_id + " not found" )
        return None
        
    def lookUpGuestByUUID(self, uuid):
        for guest in self.__allGuestPtrList:
            if guest.getUuid()==uuid:
                logging.debug("libvirtHypevisor.lookUpGuestById(): "+ uuid )
                return guest
        logging.debug( "libvirtHypevisor.lookUpGuestById(): "+ uuid + " not found" )
        return None
    
    def getNumofActiveVms(self):
        logging.debug("libvirtHypervisor.getNumofActiveVms(): %s" %self.__numOfActiveGuests)
        return self.__numOfActiveGuests
    
    def getNumofInactiveVms(self):
        logging.debug("libvirtHypervisor.getNumofInactiveVms(): %s" %self.__numOfInactiveGuests)
        return self.__numOfInactiveGuests
    
    def getNumofAllVms(self):
        logging.debug("libvirtHypervisor.getNumofAllVms(): %s"  %(self.__numOfAllGuests))
        return self.__numOfActiveGuests+self.__numOfInactiveGuests
    
    def getActiveVmNames(self):
        nameList=[]
        for guest in self.__activeGuestPtrList:
            nameList.append(guest.getName())
        logging.debug("libvirtHypervisor.getActiveVmNames(): "+ str(nameList))
        return nameList
    
    def getInactiveVmNames(self):
        nameList=[]
        for guest in self.__inactiveGuestPtrList:
            nameList.append(guest.getName())
        logging.debug("libvirtHypervisor.getInactiveVmNames(): "+ str(nameList))
        return nameList
    
    def getAllVmNames(self):
        nameList=[]
        for guest in self.__allGuestPtrList:
            nameList.append(guest.getName())
        logging.debug("libvirtHypervisor.getAllVmNames(): "+ str(nameList))
        return nameList
    
"""

host=libvirtHypervisor()
print "----------hypervisor--------------"
for x,y in host.getList().iteritems():
	print x, "=",y


for g in host.getActiveVmNames():
	guest=Guest
	guest=host.lookUpGuestByName(g)
	specs=guest.getSpecsList()
	deviceTypes= guest.getDevicesList()
	print "----------- vm " + g  + " -----------------"
	for x,y in specs.iteritems():
	    print x,"=",y
	
	for dtype in deviceTypes:
	    for device in dtype:
	       for x,y in device.iteritems():
	           print x,"=",y

"""




