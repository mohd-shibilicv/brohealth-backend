from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.validators import MinLengthValidator, RegexValidator
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate

from doctors.models import Doctor, Certificate, DoctorVerification, DoctorAvailability
from accounts.serializers import UserSerializer


class DoctorSerializer(serializers.ModelSerializer):
    """
    A Serializer for the Doctor Model.
    """
    user = UserSerializer(read_only=True)

    class Meta:
        model = Doctor
        fields = (
            'id',
            'user',
            'specialization',
            'years_of_experience',
            'education',
            'clinic_address',
            'clinic_phone_number',
            'clinic_website',
            'is_approved',
        )


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = '__all__'


class DoctorVerificationSerializer(serializers.ModelSerializer):
    certificates = CertificateSerializer(many=True, read_only=True)

    class Meta:
        model = DoctorVerification
        fields = [
            'id',
            'doctor',
            'license_number',
            'licensure_information',
            'verification_status',
            'certificates',
        ]

    def create(self, validated_data):
        doctor_verification = DoctorVerification.objects.create(**validated_data)

        index =  0
        certificates_data = []
        while True:
            key = f'certificates[{index}]'
            if key in self.context['request'].FILES:
                certificates_data.append(self.context['request'].FILES[key])
                index +=  1
            else:
                break

        # Create Certificate instances and add them to the doctor_verification instance
        for certificate_data in certificates_data:
            certificate = Certificate.objects.create(file=certificate_data)
            doctor_verification.certificates.add(certificate)

        # Save the doctor_verification instance to update the ManyToManyField
        doctor_verification.save()

        return doctor_verification


class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    """
    A Serializer for the DoctorAvailability Model.
    """
    doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.filter(is_approved=True))

    class Meta:
        model = DoctorAvailability
        fields = [
            'id',
            'doctor',
            'availability_schedule',
        ]
