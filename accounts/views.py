import os
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import datetime, timedelta
from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import filters
from rest_framework import status
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.exceptions import ValidationError

from accounts.models import User, PasswordReset
from accounts.serializers import UserSerializer, ResetPasswordRequestSerializer, ResetPasswordSerializer


class UserModelViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['role']
    ordering = ['-role']

    def get_queryset(self):
        return User.objects.all()

    def get_object(self):
        lookup_field_value = self.kwargs[self.lookup_field]
        obj = User.objects.get(id=lookup_field_value)
        self.check_object_permissions(self.request, obj)
        return obj


class LogoutView(APIView):
    def get(self, request):
        # Get the refresh token from the cookies
        refresh_token = request.COOKIES.get('refresh_token')

        # Blacklist the refresh token
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception as e:
                # Handle the exception if the token is invalid or malformed
                print(f"Error blacklisting token: {e}")

        # Delete the JWT tokens from the client's cookies
        response = Response(status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        return response


class RequestPasswordReset(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data['email']
        user = User.objects.filter(email__iexact=email).first()

        if user:
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)  
            reset = PasswordReset(email=email, token=token)
            reset.save()

            frontend_base_url = os.getenv('FRONTEND_BASE_URL')
            password_reset_route = os.getenv('PASSWORD_RESET_ROUTE')
            reset_url = f"{frontend_base_url}/{password_reset_route}?token={token}"

            # Render the email message
            html_message = render_to_string('password_reset_email.html', {
                'user': user,
                'reset_url': reset_url
            })

            # Create the email message
            email_message = EmailMultiAlternatives(
                "Password Reset Request",
                "Please use the link below to reset your password.",
                settings.EMAIL_HOST_USER,
                [user.email],
            )

            # Send the email
            email_message.attach_alternative(html_message, "text/html")
            email_message.send()

            return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User with credentials not found"}, status=status.HTTP_404_NOT_FOUND)


class ResetPassword(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = []

    def post(self, request, token):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data

        new_password = data['new_password']
        confirm_password = data['confirm_password']

        if new_password != confirm_password:
            return Response({"error": "Passwords do not match"}, status=status.HTTP_417_EXPECTATION_FAILED)
        
        reset_obj = PasswordReset.objects.filter(token=token).first()

        if not reset_obj:
            return Response({'error':'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        
        if timezone.now() > reset_obj.created_at + timedelta(hours=24):
            return Response({'message': 'Reset password link has expired!'}, status=status.HTTP_400_BAD_REQUEST);
        
        user = User.objects.filter(email=reset_obj.email).first()

        if user:
            user.set_password(request.data['new_password'])
            user.save()
            
            reset_obj.delete()
            
            return Response({'success':'Password updated'})
        else: 
            return Response({'error':'No user found'}, status=status.HTTP_404_NOT_FOUND)


class DeactivateAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=request.user.pk)
        user.is_active = False
        user.save()
        return Response({"message": "Account deactivated successfully."}, status=status.HTTP_200_OK)

