from django.urls import path

from patients import views
from accounts.views import LogoutView


app_name = 'patients'

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    path('protected/', views.ProtectedView.as_view(), name='protected'),
]
