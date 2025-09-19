from rest_framework.permissions import BasePermission


class IsAuthenticatedAndCustomerForCreate(BasePermission):
    """
    GET
    POST requires auth AND user.type == 'customer'.
    """
    message = 'Nur Kunden können Bestellungen erstellen.'

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if request.method == 'POST':
            return getattr(user, 'type', None) == 'customer'
        return True


class IsOrderBusinessUser(BasePermission):
    """
    Allows PATCH only for the business assigned to the order.
    """
    message = 'Nur der zugehörige Geschäftsbenutzer darf den Status dieser Bestellung ändern.'

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            bool(user and user.is_authenticated) and
            getattr(user, 'type', None) == 'business' and
            obj.business_user_id == user.id
        )
