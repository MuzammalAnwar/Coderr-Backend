# orders_app/models.py
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q, F
from django.utils import timezone

User = settings.AUTH_USER_MODEL


class Order(models.Model):
    class OfferType(models.TextChoices):
        BASIC = 'basic', 'basic'
        STANDARD = 'standard', 'standard'
        PREMIUM = 'premium', 'premium'

    class Status(models.TextChoices):
        IN_PROGRESS = 'in_progress', 'in_progress'
        COMPLETED = 'completed', 'completed'
        CANCELLED = 'cancelled', 'cancelled'

    customer_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders_as_customer',
        limit_choices_to={"type": "customer"},
    )

    business_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders_as_business',
        limit_choices_to={"type": "business"},
    )

    title = models.CharField(max_length=255)
    revisions = models.PositiveIntegerField(default=0)
    delivery_time_in_days = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list, blank=True)

    offer_type = models.CharField(
        max_length=20, choices=OfferType.choices, default=OfferType.BASIC
    )

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.IN_PROGRESS
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['offer_type']),
            models.Index(fields=['created_at']),
        ]

    def clean(self):
        errors = {}
        if getattr(self.customer_user, 'type', None) != 'customer':
            errors["customer_user"] = "Selected user is not of type 'customer'."
        if getattr(self.business_user, "type", None) != 'business':
            errors["business_user"] = "Selected user is not of type 'business'."
        if self.customer_user_id and self.customer_user_id == self.business_user_id:
            errors["customer_user"] = "Customer and business cannot be the same user."
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.pk} – {self.title}"
