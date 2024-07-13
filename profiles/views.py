import random

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import mixins, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .constants import CODE_MAX_LEN, DIGS
from .models import ConfirmationCode, UserProfile
from .serializer import ConfCodeSerializer, ProfileSerializer
from .tasks import send_email_to_user

User = get_user_model()


class ProfileViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = (AllowAny,)
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer


class ConfirmationCodeView(viewsets.ViewSet):
    queryset = ConfirmationCode.objects.all()
    serializer_class = ConfCodeSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        users_pin_code = ConfirmationCode.objects.filter(user=user).first()
        if not users_pin_code:
            raise ValidationError('Request the code first')
        if users_pin_code.code == serializer.validated_data['code']:
            user.profile.is_activated = True
            user.profile.save()
            return Response({'message': 'Profile is activated'})
        users_pin_code.delete()
        raise ValidationError('Invalid confirmation code')

    def list(self, request, *args, **kwargs):
        user = request.user
        users_code = ConfirmationCode.objects.filter(user=user).first()
        if users_code:
            users_code.delete()
        users_code = ConfirmationCode.objects.create(
            user=user,
            code=''.join(random.sample(
                DIGS, CODE_MAX_LEN
            ))
        )
        serializer = self.serializer_class(users_code)

        data_for_message = {
            'subject': 'Код подтверждения',
            'message': f'Ваш код подтверждения: {users_code}',
            'from_email': settings.DEFAULT_FROM_EMAIL,
            'recipient_list': [user.email],
        }

        send_email_to_user.delay(data_for_message,)
        return Response(serializer.data, status=status.HTTP_200_OK)
