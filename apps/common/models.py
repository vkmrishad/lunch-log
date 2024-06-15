from django.db.models import DateTimeField, Model
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class BaseModel(Model):
    created_at = DateTimeField(
        default=timezone.now, editable=False, help_text=_("Created time"), null=True
    )
    updated_at = DateTimeField(
        auto_now=True, editable=False, help_text=_("Updated time"), null=True
    )

    class Meta:
        abstract = True
