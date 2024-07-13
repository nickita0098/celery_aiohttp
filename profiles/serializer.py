from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import UserProfile
from .constants import CODE_MAX_LEN
from .validators import validate_confirmation_code

User = get_user_model()


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username')


class ProfileSerializer(serializers.ModelSerializer):
    user = UserShortSerializer()

    class Meta:
        model = UserProfile
        fields = '__all__'


class ConfCodeSerializer(serializers.Serializer):
    code = serializers.CharField(
        required=True,
        max_length=CODE_MAX_LEN,
        min_length=CODE_MAX_LEN,
        validators=(validate_confirmation_code,)
    )
