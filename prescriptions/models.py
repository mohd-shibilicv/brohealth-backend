from django.db import models

from patients.models import Patient
from doctors.models import Doctor
from appointments.models import Appointment


class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='prescriptions_given')
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='prescription', blank=True, null=True)
    diagnosis = models.CharField(max_length=255)
    medication_details = models.TextField()
    dosage = models.CharField(max_length=255)
    prescription_image = models.ImageField(upload_to='prescription_images/', blank=True, null=True)
    additional_instructions = models.TextField(blank=True, null=True)
    prescription_date = models.DateField(auto_now=True)
