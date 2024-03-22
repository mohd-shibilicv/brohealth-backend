from django.db import models
from  django.conf import settings


class Admin(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'admin'
        verbose_name_plural = 'admins'

    def __str__(self):
        return f"{self.user.email}"
