from rest_framework import serializers

from notifications.models import DoctorNotification, PatientNotification, AdminNotification


class PatientNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientNotification
        fields = ['id', 'message', 'timestamp', 'is_read', 'notification_type', 'patient', 'related_appointment']
        read_only_fields = ['id', 'timestamp']


class DoctorNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorNotification
        fields = ['id', 'message', 'timestamp', 'is_read', 'notification_type', 'doctor', 'related_appointment']
        read_only_fields = ['id', 'timestamp']


class AdminNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminNotification
        fields = ['id', 'message', 'timestamp', 'is_read', 'notification_type', 'admin']
        read_only_fields = ['id', 'timestamp']
