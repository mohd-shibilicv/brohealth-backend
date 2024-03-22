from django.contrib import admin

from prescriptions.models import Prescription


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'appointment', 'prescription_date']
