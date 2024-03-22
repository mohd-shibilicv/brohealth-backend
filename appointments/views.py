import json

from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from django.views import View
from django.conf import settings
from django.template.loader import render_to_string
from rest_framework.decorators import api_view
from django.core.mail import EmailMultiAlternatives
from django.db import transaction

from accounts.permissions import IsPatient
from patients.models import Patient
from doctors.models import Doctor
from appointments.models import Appointment, AppointmentRoom, AppointmentChat
from appointments.serializers import AppointmentSerializer, AppointmentRoomSerializer, AppointmentChatSerializer
from appointments.token04 import generate_token04
from notifications.models import PatientNotification
from appointments.tasks import send_session_email_task


class AppointmentListCreateView(generics.ListCreateAPIView):
    """
    API view for listing and creating Appointments.
    """
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Override the queryset to return appointments based on the user role.
        """
        limit = self.request.query_params.get('limit')
        user = self.request.user
        if Doctor.objects.filter(user=user).exists():
            if limit:
                return Appointment.objects.filter(doctor__user=user).order_by('-date_and_time')[:5]
            return Appointment.objects.filter(doctor__user=user)
        elif Patient.objects.filter(user=user).exists():
            if limit:
                return Appointment.objects.filter(patient__user=user).order_by('-date_and_time')[:5]
            return Appointment.objects.filter(patient__user=user)
        else:
            return Appointment.objects.all()

    def perform_create(self, serializer):
        doctor_id = self.request.query_params.get('doctor_id')
        doctor = get_object_or_404(Doctor, pk=doctor_id)
        patient = get_object_or_404(Patient, user=self.request.user)
        serializer.save(patient=patient, doctor=doctor)


class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting Appointments.
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class AppointmentCancelView(generics.UpdateAPIView):
    """
    API view for canceling Appointments.
    """
    queryset = Appointment.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = AppointmentSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.status not in ['canceled', 'completed']:
            instance.status = 'canceled'
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Appointment cannot be canceled'}, status=status.HTTP_400_BAD_REQUEST)


class AppointmentRescheduleView(generics.UpdateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        new_date_and_time = request.data.get('date_and_time')
        instance.date_and_time = new_date_and_time
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GenerateRoomAccessToken(View):
    def get(self, request, *args, **kwargs):
        # Extract parameters from the request
        app_id = int(request.GET.get('appID'))
        server_secret = request.GET.get('serverSecret')
        user_id = request.GET.get('userID')

        # Token expiration time, in seconds
        effective_time_in_seconds = 128000

        # Additional configuration information
        payload = {
            "tokenPayload": "" # When generating a basic authentication token, the payload should be set to an empty string
        }

        # Call the function to generate the token
        # Assuming generate_token04 is a function you've defined elsewhere that generates the token
        token_info = generate_token04(app_id, user_id, server_secret, effective_time_in_seconds, json.dumps(payload))
        # Prepare the response
        response_data = {
            "token": token_info.token,
            "error_code": token_info.error_code,
            "message": token_info.error_message
        }

        # Return the response
        return JsonResponse(response_data)


@transaction.atomic
@api_view(['POST'])
def send_session_email(request):
    appointment_id = request.data.get('appointment_id')
    patient_id = request.data.get('patient_id')
    doctor_id = request.data.get('doctor_id')
    room_url = request.data.get('room_url')

    appointment = get_object_or_404(Appointment, pk=appointment_id)
    doctor = get_object_or_404(Doctor, pk=doctor_id)
    patient = get_object_or_404(Patient, pk=patient_id)

    # Construct the email message
    subject = 'Your appointment is starting'
    from_email = settings.EMAIL_HOST_USER

    # Prepare plain text version of the email
    text_content = f'Hello, your appointment with Dr. {doctor.user.first_name} {doctor.user.last_name} is starting. Click or open the following link to join: {room_url}'

    # Prepare HTML version of the email
    html_content = render_to_string('session_email_template.html', {
        'appointment': appointment,
        'patient': patient,
        'doctor': doctor,
        'room_url': room_url,
    })

    PatientNotification.objects.create(
        patient=patient,
        message=text_content,
        related_appointment=appointment,
        notification_type=PatientNotification.WARNING
    )

    # Send the email asynchronously using Celery
    send_session_email_task.delay(
        subject,
        text_content,
        html_content,
        from_email,
        [patient.user.email]
    )

    return JsonResponse({'status': 'success', 'message': 'Email scheduled for sending'})


class AppointmentRoomList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AppointmentRoomSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == "doctor":
            return AppointmentRoom.objects.filter(appointment__doctor__user=user).exclude(appointment__status='completed')
        elif user.role == "patient":
            return AppointmentRoom.objects.filter(appointment__patient__user=user).exclude(appointment__status='completed')
        return AppointmentRoom.objects.none()


class AppointmentRoomCreate(generics.CreateAPIView):
    queryset = AppointmentRoom.objects.all()
    serializer_class = AppointmentRoomSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        appointment_id = self.request.data.get('appointment_id')
        appointment = get_object_or_404(Appointment, id=appointment_id)
        serializer.save(appointment=appointment)


class AppointmentChatList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AppointmentChatSerializer

    def get_queryset(self):
        room_id = self.kwargs['room_id']
        return AppointmentChat.objects.filter(room__id=room_id)


class AppointmentChatCreate(generics.CreateAPIView):
    queryset = AppointmentChat.objects.all()
    serializer_class = AppointmentChatSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        room_id = self.kwargs['room_id']
        message = self.kwargs['message']
        room = get_object_or_404(AppointmentRoom, id=room_id)
        serializer.save(room=room, sender=self.request.user, message=message)
