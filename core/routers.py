from rest_framework.routers import SimpleRouter

from accounts.views import UserModelViewSet
from patients.views import PatientModelViewSet
from doctors.views import DoctorModelViewSet
from admins.views import AdminModelViewSet
from core.viewsets import LoginViewSet, RegistrationViewSet, RefreshViewSet
from prescriptions.views import PrescriptionViewSet


routes = SimpleRouter()

# AUTHENTICATION
routes.register(r'auth/login', LoginViewSet, basename='auth-login')
routes.register(r'auth/register', RegistrationViewSet, basename='auth-register')
routes.register(r'auth/refresh', RefreshViewSet, basename='auth-refresh')

# USER
routes.register(r'user', UserModelViewSet, basename='user')

# Patient
routes.register(r'patient', PatientModelViewSet, basename='patient')

# Doctor
routes.register(r'doctor', DoctorModelViewSet, basename='doctor')

# Admin
routes.register(r'admin', AdminModelViewSet, basename='admin')

# Prescriptions
routes.register(r'prescriptions', PrescriptionViewSet, basename='prescriptions')

urlpatterns = [
    *routes.urls
]
