from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Review(models.Model):
    business_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_reviews"
    )
    reviewer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="written_reviews"
    )

    rating = models.PositiveSmallIntegerField()  # 1..5
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["business_user", "reviewer"],
                name="unique_reviewer_business_review",
            )
        ]
        ordering = ["-updated_at"]

    def __str__(self):
        return f"Review #{self.pk} by {self.reviewer_id} for {self.business_user_id}"
