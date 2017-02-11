from vmhost.models import Vmhost
from vmhost.models import Guest
from django.contrib import admin

class VmhostAdmin(admin.ModelAdmin):
	fields=['name','virtType']

class GuestAdmin(admin.ModelAdmin):
	fiealds=['vmhost','name','currCpu','currMemory']


admin.site.register(Vmhost, VmhostAdmin)
admin.site.register(Guest, GuestAdmin)

