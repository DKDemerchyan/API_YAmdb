from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    ROLES = (
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Administrator'),
    )
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    role = models.CharField(max_length=256, choices=ROLES, default=ROLES[0][0])
    email = models.EmailField(
        _('email address'), blank=False, unique=True, max_length=254
    )
    bio = models.TextField(_('biography'), blank=True,)
    confirmation_code = models.IntegerField(
        _('confirmation code'), blank=True, null=True
    )

    def __str__(self):
        return self.username
