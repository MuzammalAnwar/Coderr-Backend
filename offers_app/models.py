from django.conf import settings
from django.db import models
from django.utils import timezone

User = settings.AUTH_USER_MODEL


class Offer(models.Model):
    business_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="offers",
        limit_choices_to={"type": "business"},  # admin/forms convenience
    )
    title = models.CharField(max_length=255)
    image = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"Offer #{self.pk} – {self.title}"


class OfferDetail(models.Model):
    class OfferType(models.TextChoices):
        BASIC = "basic", "basic"
        STANDARD = "standard", "standard"
        PREMIUM = "premium", "premium"

    offer = models.ForeignKey(
        Offer, on_delete=models.CASCADE, related_name="details"
    )
    title = models.CharField(max_length=255)
    revisions = models.PositiveIntegerField(default=0)
    delivery_time_in_days = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # ["Logo", "Visitenkarte"]
    features = models.JSONField(default=list, blank=True)
    offer_type = models.CharField(
        max_length=20, choices=OfferType.choices
    )

    class Meta:
        # Don’t allow duplicate types for the same offer
        unique_together = ("offer", "offer_type")
        indexes = [
            models.Index(fields=["offer_type"]),
            models.Index(fields=["price"]),
        ]

    def __str__(self):
        return f"{self.offer} • {self.offer_type}"
