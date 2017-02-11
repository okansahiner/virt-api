from django.template import Context, loader
from django.http import HttpResponse
from vmhost.models import Vmhost
from vmhost.models import Guest
import os, sys

sys.path.append('/home/hysteria/Folders/calismalar/eclipse_workspace/vm_manager_api')

from queryHandler import queryHandler

def index(request):
    ipList=[]
    ip='10.0.1.10'
    host=queryHandler('host1',ip)
    allHosts=[]
    allHosts.append(host)

    t=loader.get_template('vmhost/index.html')
    c=Context({'host_list':allHosts})
    return HttpResponse(t.render(c))


