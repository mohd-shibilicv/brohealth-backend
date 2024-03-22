from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, permission_classes
from django.http import Http404
from django.db.models import Q
from django.http import JsonResponse
from calendar import monthrange
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Sum, Case, When, IntegerField
from django.db.models.functions import TruncMonth, ExtractYear

from accounts.permissions import IsDoctor
from patients.models import Patient
from appointments.models import Appointment
from doctors.models import Doctor, DoctorVerification
from doctors.serializers import DoctorSerializer, DoctorVerificationSerializer


class DoctorModelViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    permission_classes = [IsDoctor]
    serializer_class = DoctorSerializer

    def get_queryset(self):
        return Doctor.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class DoctorVerificationViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]
    queryset = DoctorVerification.objects.all()
    serializer_class = DoctorVerificationSerializer


class DoctorListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Doctor.objects.filter(is_approved=True)
        search_term = self.request.query_params.get("search", None)
        if search_term:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search_term)
                | Q(user__last_name__icontains=search_term)
                | Q(specialization__icontains=search_term)
            )
        return queryset

    def get(self, request, format=None):
        queryset = self.get_queryset()
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = DoctorSerializer(page, many=True)
        return Response(serializer.data)


class DoctorDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Doctor.objects.get(pk=pk)
        except Doctor.DoesNotExist:
            raise Http404("Doctor does not exists.")

    def get(self, request, pk, format=None):
        doctor = self.get_object(pk)
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_role_counts(request):
    # Query the database to get the counts of users with roles as patients and doctors
    patients = Patient.objects.all()
    patient_count = 0
    user = request.user
    for patient in patients:
        if Appointment.objects.filter(doctor__user=user, patient=patient).exists():
            patient_count += 1

    apppointments_count = Appointment.objects.filter(doctor__user=user).count()
    paid_appointments_count = Appointment.objects.filter(
        doctor__user=user, paid=True
    ).count()
    revenue = paid_appointments_count * (1000 * 0.9)

    # Prepare the response data
    data = {
        "patients": patient_count,
        "apppointments_count": apppointments_count,
        "revenue": revenue,
    }

    # Return the counts as a JSON response
    return JsonResponse(data)


class DoctorMonthlyAppointmentsAndRevenueView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        current_year = timezone.now().year
        appointments = (
            Appointment.objects.filter(date_and_time__year=current_year)
            .filter(doctor__user=request.user)
            .annotate(month=TruncMonth("date_and_time"))
            .values("month")
            .annotate(
                appointments_count=Count("id"),
                paid_appointments_count=Count(
                    Case(When(paid=True, then=1), output_field=IntegerField())
                ),
                revenue=Sum(
                    Case(When(paid=True, then=1000), output_field=IntegerField())
                ),
            )
            .order_by("month")
        )

        data = list(appointments)

        return Response(data)


class DoctorDailyAppointmentsAndRevenueView(APIView):
    def get(self, request):
        current_year = timezone.now().year
        current_month = timezone.now().month
        days_in_month = monthrange(current_year, current_month)[1]

        data = []
        for day in range(1, days_in_month + 1):
            date = timezone.datetime(current_year, current_month, day).date()
            appointments = Appointment.objects.filter(
                doctor__user=request.user, date_and_time__date=date
            ).aggregate(
                appointments_count=Count("id"),
                paid_appointments_count=Count(
                    Case(When(paid=True, then=1), output_field=IntegerField())
                ),
                revenue=Sum(
                    Case(When(paid=True, then=1000), output_field=IntegerField())
                ),
            )

            data.append(
                {
                    "day": date,
                    "appointments_count": appointments["appointments_count"],
                    "paid_appointments_count": appointments["paid_appointments_count"],
                    "revenue": appointments["revenue"],
                }
            )

        return Response(data)


class DoctorYearlyAppointmentsAndRevenueView(APIView):
    def get(self, request):
        appointments = (
            Appointment.objects.filter(doctor__user=request.user)
            .annotate(year=ExtractYear("date_and_time"))
            .values("year")
            .annotate(
                appointments_count=Count("id"),
                paid_appointments_count=Count(
                    Case(When(paid=True, then=1), output_field=IntegerField())
                ),
                revenue=Sum(
                    Case(When(paid=True, then=1000), output_field=IntegerField())
                ),
            )
            .order_by("year")
        )

        data = list(appointments)

        return Response(data)
