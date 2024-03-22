from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"account-verification", views.DoctorVerificationViewSet)

app_name = "doctors"

urlpatterns = [
    path("api/", include(router.urls)),
    path("", views.DoctorListView.as_view(), name="doctor-list"),
    path("<int:pk>/", views.DoctorDetailView.as_view(), name="doctor-detail"),
    path("user-role-counts/", views.user_role_counts, name="user_role_counts"),
    path(
        "monthly-appointments-and-revenue/",
        views.DoctorMonthlyAppointmentsAndRevenueView.as_view(),
        name="monthly_appointments_and_revenue",
    ),
    path(
        "daily-appointments-and-revenue/",
        views.DoctorDailyAppointmentsAndRevenueView.as_view(),
        name="daily_appointments_and_revenue",
    ),
    path(
        "yearly-appointments-and-revenue/",
        views.DoctorYearlyAppointmentsAndRevenueView.as_view(),
        name="yearly_appointments_and_revenue",
    ),
]
