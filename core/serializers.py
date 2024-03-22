from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from django.core.validators import MinLengthValidator, RegexValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ObjectDoesNotExist

from accounts.serializers import UserSerializer
from patients.serializers import PatientSerializer
from doctors.serializers import DoctorSerializer
from admins.serializers import AdminSerializer
from accounts.models import User
from patients.models import Patient
from doctors.models import Doctor
from admins.models import Admin


class LoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        # Serialize the user
        user_data = UserSerializer(self.user).data

        if self.user.role == 'patient':
            # Serialize the patient
            patient_data = PatientSerializer(Patient.objects.get(user=self.user)).data
            data['patient'] = patient_data
        elif self.user.role == 'doctor':
            # Serialize the doctor
            doctor_data = DoctorSerializer(Doctor.objects.get(user=self.user)).data
            data['doctor'] = doctor_data
        elif self.user.role == 'admin':
            # Serialize the admin
            admin_data = AdminSerializer(Admin.objects.get(user=self.user)).data
            data['admin'] = admin_data

        data['user'] = user_data
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class RegisterSerializer(UserSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all(), message="User with that email already exists.")],
        error_messages={
            'unique': 'User with that email already exists.'
        }
    )
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[
            MinLengthValidator(8),
            RegexValidator(
                regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$',
                message='Password must contain at least eight characters, at least one uppercase letter , one number and one special character'
            ),
        ],
        error_messages={
            'blank': 'Password cannot be blank.',
            'required': 'Password is required.'
        }
    )
    role = serializers.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = ['id', 'role', 'first_name', 'last_name', 'email', 'password', 'is_active']

    def create(self, validated_data):
        role = validated_data.pop('role', None)

        try:
            user = User.objects.get(email=validated_data['email'])
        except ObjectDoesNotExist:
            user = User.objects.create_user(**validated_data)

        if role == 'doctor':
            Doctor.objects.create(user=user)
            user.role = 'doctor'
            user.save()
        elif role == 'patient':
            Patient.objects.create(user=user)
            user.role = 'patient'
            user.save()

        return user
