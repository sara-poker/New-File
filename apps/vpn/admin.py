from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Vpn ,Test

# Register your models here.
class VpnAdmin(admin.ModelAdmin):
    list_per_page = 30

class TestAdmin(admin.ModelAdmin):
    list_per_page = 30

admin.site.register(Vpn,VpnAdmin)
admin.site.register(Test,TestAdmin)

