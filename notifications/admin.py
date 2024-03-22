from django.contrib import admin

from notifications.models import PatientNotification, DoctorNotification, AdminNotification


@admin.register(PatientNotification)
class PatientNotificationAdmin(admin.ModelAdmin):
    list_display = ('patient', 'notification_type')

@admin.register(DoctorNotification)
class DoctorNotificationAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'notification_type')

@admin.register(AdminNotification)
class AdminNotificationAdmin(admin.ModelAdmin):
    list_display = ('admin', 'notification_type')
