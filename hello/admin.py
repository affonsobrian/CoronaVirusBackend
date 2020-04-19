from django.contrib import admin
from hello.models import Notification, NotificationType

class NotificationTypeAdmin(admin.ModelAdmin):
    pass

class NotificationAdmin(admin.ModelAdmin):
    pass

admin.site.register(NotificationType, NotificationTypeAdmin)
admin.site.register(Notification, NotificationAdmin)