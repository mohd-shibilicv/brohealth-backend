import os
from calendar import monthrange
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db import transaction
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Sum, Case, When, IntegerField
from django.db.models.functions import TruncMonth, ExtractYear

from admins.models import Admin
from doctors.models import DoctorVerification, VerificationStatusChoices
from admins.serializers import AdminSerializer
from accounts.permissions import IsAdmin
from accounts.models import User
from appointments.models import Appointment

class AdminModelViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = AdminSerializer


@api_view(['POST'])
@permission_classes([IsAdmin])
@transaction.atomic
def approve_doctor_verification(request, verification_id):
    verification = get_object_or_404(DoctorVerification, id=verification_id)

    verification.verification_status = VerificationStatusChoices.APPROVED
    verification.save()

    doctor = verification.doctor
    doctor.is_approved = True
    doctor.save()

    frontend_base_url = os.getenv('FRONTEND_BASE_URL')
    login_url = f"{frontend_base_url}/login"

    # Render the email message
    html_message = render_to_string('verification_approval.html', {
        'doctor': doctor,
        'verification': verification,
        'login_url': login_url
    })

    # Create the email message
    email_message = EmailMultiAlternatives(
        "Account Verification Approved",
        "Please use the link below to login to your account.",
        settings.EMAIL_HOST_USER,
        [doctor.user.email],
    )

    # Send the email
    email_message.attach_alternative(html_message, "text/html")
    email_message.send()

    return Response({"message": "Doctor verification approved successfully."}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAdmin])
@transaction.atomic
def reject_doctor_verification(request, verification_id):
    verification = get_object_or_404(DoctorVerification, id=verification_id)

    verification.verification_status = VerificationStatusChoices.REJECTED
    verification.save()

    return Response({"message": "Doctor verification rejected."}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAdmin])
def delete_doctor_verification(request, verification_id):
    verification = get_object_or_404(DoctorVerification, id=verification_id)

    verification.delete()

    return Response({"message": "Doctor verification Deleted."}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def user_role_counts(request):
    # Query the database to get the counts of users with roles as patients and doctors
    patient_count = User.objects.filter(role='patient').count()
    doctor_count = User.objects.filter(role='doctor').count()
    apppointments_count = Appointment.objects.count()
    paid_appointments_count = Appointment.objects.filter(paid=True).count()
    revenue = paid_appointments_count * 1000

    # Prepare the response data
    data = {
        'patients': patient_count,
        'doctors': doctor_count,
        'apppointments_count': apppointments_count,
        'revenue': revenue
    }

    # Return the counts as a JSON response
    return JsonResponse(data)


class MonthlyAppointmentsAndRevenueView(APIView):
    def get(self, request):
        current_year = timezone.now().year
        appointments = Appointment.objects.filter(
            date_and_time__year=current_year
        ).annotate(
            month=TruncMonth('date_and_time')
        ).values('month').annotate(
            appointments_count=Count('id'),
            paid_appointments_count=Count(Case(When(paid=True, then=1), output_field=IntegerField())),
            revenue=Sum(Case(When(paid=True, then=1000), output_field=IntegerField()))
        ).order_by('month')

        data = list(appointments)

        return Response(data)


class DailyAppointmentsAndRevenueView(APIView):
    def get(self, request):
        current_year = timezone.now().year
        current_month = timezone.now().month
        days_in_month = monthrange(current_year, current_month)[1]

        data = []
        for day in range(1, days_in_month + 1):
            date = timezone.datetime(current_year, current_month, day).date()
            appointments = Appointment.objects.filter(
                date_and_time__date=date
            ).aggregate(
                appointments_count=Count('id'),
                paid_appointments_count=Count(Case(When(paid=True, then=1), output_field=IntegerField())),
                revenue=Sum(Case(When(paid=True, then=1000), output_field=IntegerField()))
            )

            data.append({
                'day': date,
                'appointments_count': appointments['appointments_count'],
                'paid_appointments_count': appointments['paid_appointments_count'],
                'revenue': appointments['revenue']
            })

        return Response(data)


class YearlyAppointmentsAndRevenueView(APIView):
    def get(self, request):
        appointments = Appointment.objects.annotate(
            year=ExtractYear('date_and_time')
        ).values('year').annotate(
            appointments_count=Count('id'),
            paid_appointments_count=Count(Case(When(paid=True, then=1), output_field=IntegerField())),
            revenue=Sum(Case(When(paid=True, then=1000), output_field=IntegerField()))
        ).order_by('year')

        data = list(appointments)

        return Response(data)
