from django.db import models
from django.conf import settings


class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100, blank=True)
    years_of_experience = models.IntegerField(blank=True, null=True)
    education = models.TextField(blank=True)
    clinic_address = models.TextField(blank=True)
    clinic_phone_number = models.CharField(max_length=15, blank=True)
    clinic_website = models.URLField(blank=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'doctor'
        verbose_name_plural = 'doctors'
        ordering = ['-years_of_experience']

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Certificate(models.Model):
    class FileTypeChoices:
        IMAGE = 'image', 'image'
        PDF = 'pdf', 'pdf'

    file = models.FileField(upload_to='certificates/')
    type = models.CharField(
        max_length=20,
        choices=FileTypeChoices.choices,
        default=FileTypeChoices.IMAGE,
    )

    def __str__(self):
        return f'{self.file.name}'


class VerificationStatusChoices(models.TextChoices):
    PENDING = 'pending', 'Pending'
    APPROVED = 'approved', 'Approved'
    REJECTED = 'rejected', 'Rejected'


class DoctorVerification(models.Model):
    doctor = models.OneToOneField(Doctor, related_name='verification', on_delete=models.CASCADE)
    license_number = models.CharField(max_length=100, unique=True)
    licensure_information = models.TextField()
    verification_status = models.CharField(
        max_length=20,
        choices=VerificationStatusChoices.choices,
        default=VerificationStatusChoices.PENDING,
    )
    certificates = models.ManyToManyField(Certificate)

    def __str__(self):
        return f'{self.license_number}'
    
    def delete(self, *args, **kwargs):
        self.certificates.all().delete()
        super().delete(*args, **kwargs)


class DoctorAvailability(models.Model):
    doctor = models.OneToOneField('Doctor', on_delete=models.CASCADE, related_name="doctor_availability")
    availability_schedule = models.JSONField(default=dict)

    class Meta:
        verbose_name = 'doctor availability'
        verbose_name_plural = 'doctor availabilities'
        ordering = ['doctor']

    def __str__(self):
        return f"Availability for Dr. {self.doctor.user.first_name} {self.doctor.user.last_name}"
    
    def add_availability(self, date, slots):
        """
        Add or update availability for a specific date.
        """
        self.availability_schedule[date] = slots
        self.save()
