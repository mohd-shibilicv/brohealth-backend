from django.db import models

from patients.models import Patient
from doctors.models import Doctor
from admins.models import Admin
from appointments.models import Appointment


class Notification(models.Model):
    INFO = 'INFO'
    WARNING = 'WARNING'
    APPOINTMENT = 'APPOINTMENT'
    NOTIFICATION_TYPE_CHOICES = [
        (INFO, 'Informational'),
        (WARNING, 'Warning'),
        (APPOINTMENT, 'Appointment'),
    ]

    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES, default=INFO)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.notification_type}: {self.message}"


class PatientNotification(Notification):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    related_appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, null=True, blank=True)


class DoctorNotification(Notification):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    related_appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, null=True, blank=True)


class AdminNotification(Notification):
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
