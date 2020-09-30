import sys

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as DefaultUserManager
from django.db import models
from django.http import HttpRequest
from django.template.context import RequestContext
from django.utils.translation import ugettext_lazy as _


"""
Current request
"""


def get_current_request():
    """
    Get the current request using introspection.

    Be careful when getting request.user because you can get a recursion
    if this code will be used in User manager. You need override ModelBackend.get_user:
        def get_user(self, user_id):
            user = UserModel.custom_manager.get(pk=user_id)

    custom_manager - manager without calling get_current_request()
    """
    request = None
    frame = sys._getframe(1)  # sys._getframe(0).f_back

    while frame:
        # check the instance of each funtion argument
        for arg in frame.f_code.co_varnames[:frame.f_code.co_argcount]:
            request = frame.f_locals[arg]

            if isinstance(request, HttpRequest):
                break

            # from template tag
            if isinstance(request, RequestContext):
                request = request.request
                break
        else:
            frame = frame.f_back
            continue

        break

    return request if isinstance(request, HttpRequest) else None


def get_current_user():
    """
    Get current user from request.

    Don't forget to check if you want to get an authorized user:
        if user and user.is_authenticated:
            ...
    """
    request = get_current_request()
    return getattr(request, 'user', None)


def get_current_user_id():
    """Get current user id."""
    user = get_current_user()
    return user.pk if user and user.is_authenticated else None


class UserManager(DefaultUserManager):

    def get_queryset(self):
        qs = super(UserManager, self).get_queryset()

        return qs


class User(AbstractUser):
    """Override base class."""

    REQUIRED_FIELDS = ['first_name']

    username = models.CharField(
        _('login'),
        unique=True,
        error_messages={
            'unique': _("A user with that login already exists."),
        },
        max_length=255
    )
    email = models.EmailField(
        _('email'),
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )

    first_name = models.CharField(_('first name'),
                                  max_length=255, null=True)
    last_name = models.CharField(_('last name'),
                                 max_length=255, blank=True, null=True)
    middle_name = models.CharField(_('middle name'),
                                   max_length=255, blank=True, null=True)

    objects = UserManager()
