import sys

sys.path.append('/home/hysteria/Folders/calismalar/eclipse_workspace/vm_manager_api')

from queryHandler import queryHandler


host=queryHandler('host1','10.0.1.10')

print host.isVmAcpiEnabled(guest_name='guest1')

