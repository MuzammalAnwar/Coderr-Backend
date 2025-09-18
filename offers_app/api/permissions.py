from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsBusinessForWrite(BasePermission):
    """
    Allow everyone to read (GET/HEAD/OPTIONS) if you want,
    but only business users can POST/PUT/PATCH/DELETE.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        return bool(user and user.is_authenticated and getattr(user, "type", None) == "business")
    
class IsOfferOwnerOrReadOnly(BasePermission):
    """
    Only the business users who are the owner of the offer can update and delete it.
    Anyone can read.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        # must be authenticated and the owner of the offer
        return request.user.is_authenticated and obj.business_user_id == request.user.id

