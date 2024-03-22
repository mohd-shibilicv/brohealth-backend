import stripe

from django.shortcuts import redirect
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from appointments.models import Appointment, AppointmentRoom


stripe.api_key = settings.STRIPE_SECRET_KEY


@api_view(["POST"])
def test_payment(request):
    test_payment_intent = stripe.PaymentIntent.create(
        amount=1000,
        currency="inr",
        payment_method_types=["card"],
        receipt_email="test@example.com",
    )
    return Response(status=status.HTTP_200_OK, data=test_payment_intent)


class StripeCheckoutView(APIView):
    def post(self, request):
        appointment_id = request.GET.get('appointmentId', None)
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "price": "price_1Oqd4oSC7P1iNlkRIAh0eezV",
                        "quantity": 1,
                    },
                ],
                payment_method_types=[
                    "card",
                ],
                mode="payment",
                success_url=settings.SITE_URL
                + f"/dashboard/appointments/{appointment_id}/?success=true&session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=settings.SITE_URL + f"/dashboard/appointments/{appointment_id}/?canceled=true",
            )
            return redirect(checkout_session.url)

        except Exception as e:
            return Response(
                {'error': 'Something went wrong when creating stripe checkout session', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UpdateAppointmentPaymentStatusView(APIView):
    def put(self, request, appointment_id):
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            appointment.paid = True
            appointment.save()
            appointment_room_name = f"#{appointment.id} - {appointment.doctor.user.first_name} {appointment.doctor.user.last_name}"
            AppointmentRoom.objects.create(appointment=appointment, name=appointment_room_name)
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        except Appointment.DoesNotExist:
            return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)
