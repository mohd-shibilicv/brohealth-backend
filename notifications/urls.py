from django.urls import path
from .views import (
    DoctorNotificationList,
    DoctorNotificationDetail,
    PatientNotificationList,
    PatientNotificationDetail,
    AdminNotificationList,
    AdminNotificationDetail
)


app_name = 'notifications'
urlpatterns = [
    path('patient-notifications/', PatientNotificationList.as_view(), name='patient-notification-list'),
    path('patient-notifications/<int:pk>/', PatientNotificationDetail.as_view(), name='patient-notification-detail'),
    path('doctor-notifications/', DoctorNotificationList.as_view(), name='doctor-notification-list'),
    path('doctor-notifications/<int:pk>/', DoctorNotificationDetail.as_view(), name='doctor-notification-detail'),
    path('admin-notifications/', AdminNotificationList.as_view(), name='admin-notification-list'),
    path('admin-notifications/<int:pk>/', AdminNotificationDetail.as_view(), name='admin-notification-detail'),
]
