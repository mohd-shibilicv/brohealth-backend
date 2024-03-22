from rest_framework import serializers

from prescriptions.models import Prescription
from patients.serializers import PatientSerializer
from doctors.serializers import DoctorSerializer
from appointments.serializers import AppointmentSerializer


class PrescriptionSerializer(serializers.ModelSerializer):
    """
    A serializer for Prescription model
    """
    patient = PatientSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)
    appointment = AppointmentSerializer(read_only=True)

    class Meta:
        model = Prescription
        fields = [
            'id',
            'patient',
            'doctor',
            'appointment',
            'diagnosis',
            'medication_details',
            'dosage',
            'prescription_image',
            'additional_instructions',
            'prescription_date'
        ]
        read_only_fields = ['prescription_date']


class CreatePrescriptionSerializer(serializers.ModelSerializer):
    """
    A serializer for Prescription model
    """

    class Meta:
        model = Prescription
        fields = [
            'id',
            'patient',
            'doctor',
            'appointment',
            'diagnosis',
            'medication_details',
            'dosage',
            'prescription_image',
            'additional_instructions',
            'prescription_date'
        ]
        read_only_fields = ['prescription_date']
