from rest_framework import serializers
from django.core.validators import MinLengthValidator, RegexValidator
from django.conf import settings

from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    A Serilaizer for User Model
    """
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'role',
            'first_name',
            'last_name',
            'age',
            'gender',
            'address',
            'mobile_number',
            'profile_picture',
            'is_active',
        ]
        read_only_fields = ['is_active']


class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[
            MinLengthValidator(8),
            RegexValidator(
                regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$',
                message='Password must contain at least eight characters, at least one uppercase letter , one number and one special character'
            ),
        ],
        error_messages={
            'blank': 'Password cannot be blank.',
            'required': 'Password is required.'
        }
    )
    confirm_password = serializers.CharField(write_only=True, required=True)
