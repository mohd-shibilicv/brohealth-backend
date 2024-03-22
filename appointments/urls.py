from django.urls import path

from prescriptions.views import CreatePrescriptionView
from appointments.views import (
    AppointmentListCreateView,
    AppointmentDetailView,
    AppointmentCancelView,
    AppointmentRescheduleView,
    GenerateRoomAccessToken,
    send_session_email,
    AppointmentRoomList,
    AppointmentRoomCreate,
    AppointmentChatList,
    AppointmentChatCreate
)


app_name = "appointments"
urlpatterns = [
    path("", AppointmentListCreateView.as_view(), name="appointment-list-create"),
    path("<int:pk>/", AppointmentDetailView.as_view(), name="appointment-detail"),
    path("create-prescription/", CreatePrescriptionView.as_view(), name="create-prescription"),
    path(
        "<int:pk>/cancel/", AppointmentCancelView.as_view(), name="appointment-cancel"
    ),
    path(
        "<int:pk>/reschedule/",
        AppointmentRescheduleView.as_view(),
        name="appointment-reschedule",
    ),
    path('room_access_token', GenerateRoomAccessToken.as_view(), name='room-access-token'),
    path('send_session_email', send_session_email, name='send-session-email'),
    path('appointment-rooms/', AppointmentRoomList.as_view(), name='appointment-room-list'),
    path('appointment-rooms/create/', AppointmentRoomCreate.as_view(), name='appointment-room-create'),
    path('appointment-rooms/<int:room_id>/chats/', AppointmentChatList.as_view(), name='appointment-chat-list'),
    path('appointment-rooms/<int:room_id>/chats/create/', AppointmentChatCreate.as_view(), name='appointment-chat-create'),
]
