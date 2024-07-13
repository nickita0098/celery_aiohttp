from django.contrib.auth import get_user_model
from django.db import models

from .constants import CODE_MAX_LEN

User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='profile', )
    description = models.TextField(max_length=100, null=True, blank=True)
    is_activated = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'profile'


class ConfirmationCode(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='pin_code', )
    code = models.CharField(max_length=CODE_MAX_LEN, null=True)
    constraints = [
        models.UniqueConstraint(fields=('user', 'code'),
                                name='uniq_user_code')
    ]
