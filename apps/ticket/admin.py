from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *

# Register your models here.
class MessageAdmin(admin.ModelAdmin):
    list_per_page = 30

class NotificationAdmin(admin.ModelAdmin):
    list_per_page = 30

admin.site.register(Message,MessageAdmin)
admin.site.register(Notification,NotificationAdmin)


