# reviewer_app/admin.py
from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'business_user',
        'reviewer',
        'rating',
        'updated_at',
    )
    list_filter = ('rating', 'created_at', 'updated_at')
    search_fields = (
        'description',
        'business_user__username', 'business_user__email',
        'reviewer__username', 'reviewer__email',
    )
    ordering = ('-updated_at',)
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')

    raw_id_fields = ('business_user', 'reviewer')
    list_select_related = ('business_user', 'reviewer')

    fieldsets = (
        ('Bezug', {'fields': ('business_user', 'reviewer')}),
        ('Bewertung', {'fields': ('rating', 'description')}),
        ('Zeitstempel', {'fields': ('created_at', 'updated_at')}),
    )
