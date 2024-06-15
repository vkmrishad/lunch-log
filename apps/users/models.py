from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db.models import (
    EmailField,
    ManyToManyField,
)
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel


class AppUser(BaseModel, AbstractUser):
    email = EmailField(_("email address"), unique=True)

    groups = ManyToManyField(
        Group,
        verbose_name=_("groups"),
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="app_user_set",
        related_query_name="user",
    )
    user_permissions = ManyToManyField(
        Permission,
        verbose_name=_("user permissions"),
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="app_user_set",
        related_query_name="user",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "User"
        verbose_name_plural = "Users"
