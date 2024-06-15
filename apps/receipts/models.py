from django.contrib.auth import get_user_model
from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    DecimalField,
    ForeignKey,
    ImageField,
)
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel
from apps.receipts.helpers import receipt_image_upload_path

User = get_user_model()


class Receipt(BaseModel):
    user = ForeignKey(
        User, on_delete=CASCADE, related_name="receipts", verbose_name=_("user")
    )
    restaurant_name = CharField(_("restaurant name"), max_length=255)
    dated = DateTimeField(_("date and time"))
    price = DecimalField(_("price"), max_digits=10, decimal_places=2)
    image = ImageField(upload_to=receipt_image_upload_path)
    street = CharField(_("street"), max_length=100)
    city = CharField(_("city"), max_length=100)
    state = CharField(_("state"), max_length=100, blank=True, null=True)
    country = CharField(_("country"), max_length=100)
    postal_code = CharField(_("postal code"), max_length=20)

    def __str__(self):
        return self.restaurant_name

    class Meta:
        ordering = ["-id"]
        verbose_name = _("receipt")
        verbose_name_plural = _("receipts")
