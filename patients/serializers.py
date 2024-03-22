import base64
from django.core.files.base import ContentFile
from rest_framework import serializers
from django.core.validators import MinLengthValidator, RegexValidator
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from  rest_framework_simplejwt.tokens import RefreshToken

from patients.models import Patient
from accounts.models import User
from accounts.serializers import UserSerializer


class PatientSerializer(serializers.ModelSerializer):
    """
    A Serializer for the Patient Model.
    """
    user = UserSerializer(read_only=True)

    class Meta:
        model = Patient
        fields = ('id', 'user', 'medical_history', 'prescription', 'preferred_timezone', 'preferred_language', 'emergency_contact', 'is_verified')

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
