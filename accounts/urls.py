from django.urls import path, include

from accounts import views
from core.viewsets import VerifyAccountView


app_name = 'accounts'

urlpatterns = [
    path('api/auth/activate/<slug:uidb64>/<slug:token>/', VerifyAccountView.as_view({'get': 'retrieve'}), name='activate'),
    path('api/auth/reset-password/', views.RequestPasswordReset.as_view(), name='reset_password'),
    path('api/auth/reset-password-confirm/<slug:token>/', views.ResetPassword.as_view(), name='reset_password_confirm'),
    path('api/deactivate-account/', views.DeactivateAccountView.as_view(), name='deactivate-account'),
]
