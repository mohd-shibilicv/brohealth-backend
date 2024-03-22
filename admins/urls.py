from django.urls import path

from admins import views


app_name = "admins"
urlpatterns = [
    path(
        "doctor-account-verification/<int:verification_id>/approve/",
        views.approve_doctor_verification,
        name="approve-doctor-verification",
    ),
    path(
        "doctor-account-verification/<int:verification_id>/reject/",
        views.reject_doctor_verification,
        name="reject-doctor-verification",
    ),
    path(
        "doctor-account-verification/<int:verification_id>/delete/",
        views.delete_doctor_verification,
        name="delete-doctor-verification",
    ),
    path("user-role-counts/", views.user_role_counts, name="user_role_counts"),
    path(
        "monthly-appointments-and-revenue/",
        views.MonthlyAppointmentsAndRevenueView.as_view(),
        name="monthly_appointments_and_revenue",
    ),
    path(
        "daily-appointments-and-revenue/",
        views.DailyAppointmentsAndRevenueView.as_view(),
        name="daily_appointments_and_revenue",
    ),
    path(
        "yearly-appointments-and-revenue/",
        views.YearlyAppointmentsAndRevenueView.as_view(),
        name="yearly_appointments_and_revenue",
    ),
]
