from rest_framework import serializers
from django.utils import timezone
import pytz

from patients.serializers import PatientSerializer
from doctors.serializers import DoctorSerializer
from appointments.models import Appointment, AppointmentRoom, AppointmentChat


class AppointmentSerializer(serializers.ModelSerializer):
    """
    A Serializer for the Appointment model.
    """

    patient = PatientSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = [
            "id",
            "patient",
            "doctor",
            "consultation_type",
            "date_and_time",
            "status",
            "paid",
            "additional_notes",
            "created_at",
        ]
        read_only_fields = ["created_at"]


class AppointmentRoomSerializer(serializers.ModelSerializer):
    """
    A Serializer for the AppointmentRoom model.
    """
    appointment = AppointmentSerializer(read_only=True)

    class Meta:
        model = AppointmentRoom
        fields = ['id', 'appointment', 'name', 'description']


class AppointmentChatSerializer(serializers.ModelSerializer):
    """
    A Serializer for the AppointmentChat model.
    """
    class Meta:
        model = AppointmentChat
        fields = ['room', 'sender', 'message', 'timestamp']
        read_only_fields =  ['timestamp']
