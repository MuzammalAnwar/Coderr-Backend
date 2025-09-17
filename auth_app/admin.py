# auth_app/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "type")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            "username", "email", "first_name", "last_name",
            "tel", "location", "description", "working_hours", "type",
            "is_active", "is_staff", "is_superuser", "groups", "user_permissions"
        )


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """
    Admin for custom User.
    - Nice list view with filters, search, and bulk actions
    """
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    # LIST VIEW
    list_display = (
        "id", "username", "full_name", "email", "type",
        "is_active", "is_staff", "date_joined", "last_login"
    )
    list_filter = ("type", "is_active", "is_staff",
                   "is_superuser", "date_joined")
    search_fields = ("id", "username", "first_name", "last_name", "email")
    ordering = ("-date_joined",)
    list_per_page = 50

    # READONLY & LAYOUT
    readonly_fields = ("date_joined", "last_login")
    fieldsets = (
        (_("Account"), {"fields": ("username", "password")}),
        (_("Personal info"), {
            "fields": (
                "first_name", "last_name", "email", "tel",
                "location", "description", "working_hours", "type"
            )
        }),
        (_("Permissions"), {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")
        }),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "type", "password1", "password2",
                       "is_active", "is_staff", "is_superuser", "groups"),
        }),
    )

    # BULK ACTIONS
    actions = ("activate_users", "deactivate_users",
               "make_customer", "make_business")

    def full_name(self, obj):
        name = f"{obj.first_name} {obj.last_name}".strip()
        return name or "—"
    full_name.short_description = "Name"

    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"Activated {updated} user(s).")
    activate_users.short_description = "Activate selected users"

    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"Deactivated {updated} user(s).")
    deactivate_users.short_description = "Deactivate selected users"

    def make_customer(self, request, queryset):
        updated = queryset.update(type=User.Usertype.CUSTOMER)
        self.message_user(request, f"Set type=customer for {updated} user(s).")
    make_customer.short_description = "Set type → customer"

    def make_business(self, request, queryset):
        updated = queryset.update(type=User.Usertype.BUSINESS)
        self.message_user(request, f"Set type=business for {updated} user(s).")
    make_business.short_description = "Set type → business"
