from django.contrib import admin

from appointments.models import Appointment, AppointmentRoom, AppointmentChat


@admin.register(Appointment)
class AppointmentsAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'patient', 'date_and_time', 'status', 'paid']


@admin.register(AppointmentRoom)
class AppointmentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'appointment']


@admin.register(AppointmentChat)
class AppointmentsAdmin(admin.ModelAdmin):
    list_display = ['room', 'sender', 'timestamp']
