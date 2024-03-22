from django.db import models
from django.conf import settings


class Patient(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    medical_history = models.TextField(blank=True)
    prescription = models.TextField(blank=True)
    preferred_timezone = models.CharField(max_length=50, blank=True)
    preferred_language = models.CharField(max_length=10, blank=True)
    emergency_contact = models.JSONField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'patient'
        verbose_name_plural = 'patients'

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
