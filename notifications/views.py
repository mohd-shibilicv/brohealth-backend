from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import DoctorNotification, PatientNotification, AdminNotification
from .serializers import DoctorNotificationSerializer, PatientNotificationSerializer, AdminNotificationSerializer


class PatientNotificationList(generics.ListCreateAPIView):
    serializer_class = PatientNotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Override the queryset to return appointments based on the user role.
        """
        user = self.request.user
        return PatientNotification.objects.filter(patient__user=user)


class PatientNotificationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PatientNotification.objects.all()
    serializer_class = PatientNotificationSerializer
    permission_classes = [IsAuthenticated]


class DoctorNotificationList(generics.ListCreateAPIView):
    serializer_class = DoctorNotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Override the queryset to return appointments based on the user role.
        """
        user = self.request.user
        return DoctorNotification.objects.filter(doctor__user=user)


class DoctorNotificationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DoctorNotification.objects.all()
    serializer_class = DoctorNotificationSerializer
    permission_classes = [IsAuthenticated]


class AdminNotificationList(generics.ListCreateAPIView):
    serializer_class = AdminNotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Override the queryset to return appointments based on the user role.
        """
        user = self.request.user
        return AdminNotification.objects.filter(admin__user=user)


class AdminNotificationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = AdminNotification.objects.all()
    serializer_class = AdminNotificationSerializer
    permission_classes = [IsAuthenticated]
