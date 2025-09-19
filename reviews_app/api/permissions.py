from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAuthenticatedReadOnly(BasePermission):
    """require authentication (even for reads)."""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class IsCustomer(BasePermission):
    """only 'customer' users may create reviews."""
    message = "Nur Kundenprofile dürfen Bewertungen erstellen."
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return getattr(request.user, "type", None) == "customer"


class IsReviewOwner(BasePermission):
    """only the creator may update/delete."""
    message = "Nur der Ersteller der Bewertung darf diese Aktion durchführen."
    def has_object_permission(self, request, view, obj):
        return obj.reviewer_id == getattr(request.user, "id", None)
