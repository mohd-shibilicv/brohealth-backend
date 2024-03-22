from django.db import models
from django.conf import settings

from patients.models import Patient
from doctors.models import Doctor


class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    )

    CONSULTATION_TYPE_CHOICES = (
        ('new_consultation', 'New Consultation'),
        ('prescription', 'Prescription Request'),
        ('follow_up', 'Follow-up Appointment'),
    )

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments_as_patient')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments_as_doctor')
    consultation_type = models.CharField(max_length=30, choices=CONSULTATION_TYPE_CHOICES, default='new_consultation')
    date_and_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    additional_notes = models.TextField(blank=True)
    paid = models.BooleanField(default=False)
    reminder_sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'appointment'
        verbose_name_plural = 'appointments'
        ordering = ['date_and_time']

    def __str__(self):
        return f"Appointment of {self.patient.user.first_name} {self.patient.user.last_name} with Dr. {self.doctor.user.first_name} {self.doctor.user.last_name} on {self.date_and_time}"


class AppointmentRoom(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.appointment.id} - {self.name}"


class AppointmentChat(models.Model):
    room = models.ForeignKey(AppointmentRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.first_name} {self.sender.last_name}: {self.message}"
