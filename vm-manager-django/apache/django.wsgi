import os, sys
sys.path.append('/home/hysteria/Folders/calismalar/eclipse_workspace/vm-manager-web')
os.environ['DJANGO_SETTINGS_MODULE'] = 'vm_manager.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
