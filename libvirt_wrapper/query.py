import sys

sys.path.append('/home/hysteria/Folders/calismalar/eclipse_workspace/vm_manager_api')

from queryHandler import queryHandler

host=queryHandler('host1','10.0.1.11')

specs=host.getHostSpecsList()
#
print "-------host------"
for x,y in specs.iteritems():
    print x,y
    
#specs=host.getHypervisorSpecsList()

print "-------hypervisor------"
for x,y in specs.iteritems():
    print x,y

for name in host.getAllVmNames():
    print "-------guest------"
    deviceTypes=host.getVmDevicesList(guest_name=name)
    specs=host.getVmSpecsList(guest_name=name)
    
    print "----specs----"
    for x,y in specs.iteritems():
        print x,y
    
    for deviceType in deviceTypes:   
        for device in deviceType:
            print "---device---"
            for x,y in device.iteritems():
                print x,y
