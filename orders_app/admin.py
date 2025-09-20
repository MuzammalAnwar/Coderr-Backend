from django.contrib import admin
from django.db import models
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # columns in the list view
    list_display = (
        'id',
        'title',
        'offer_type',
        'status',
        'customer_user',
        'business_user',
        'price',
        'updated_at',
    )
    list_filter = ('status', 'offer_type', 'created_at', 'updated_at')
    search_fields = (
        'title',
        'customer_user__username',
        'business_user__username',
        'offer_detail__id',
    )
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')

    # avoid huge dropdowns; show a lookup widget
    raw_id_fields = ('customer_user', 'business_user', 'offer_detail')

    # reduce queries on list page
    list_select_related = ('customer_user', 'business_user', 'offer_detail')

    # organize the edit form
    fieldsets = (
        ('Parties', {
            'fields': ('customer_user', 'business_user'),
        }),
        ('Offer snapshot', {
            'fields': (
                'offer_detail',
                'title',
                'offer_type',
                'features',
                'revisions',
                'delivery_time_in_days',
                'price',
            ),
        }),
        ('Status & timestamps', {
            'fields': ('status', 'created_at', 'updated_at'),
        }),
    )

    # quick actions for status changes
    actions = ['mark_in_progress', 'mark_completed', 'mark_cancelled']

    def mark_in_progress(self, request, queryset):
        updated = queryset.update(status=Order.Status.IN_PROGRESS)
        self.message_user(request, f'{updated} order(s) set to in_progress.')
    mark_in_progress.short_description = 'Mark as in_progress'

    def mark_completed(self, request, queryset):
        updated = queryset.update(status=Order.Status.COMPLETED)
        self.message_user(request, f'{updated} order(s) set to completed.')
    mark_completed.short_description = 'Mark as completed'

    def mark_cancelled(self, request, queryset):
        updated = queryset.update(status=Order.Status.CANCELLED)
        self.message_user(request, f'{updated} order(s) set to cancelled.')
    mark_cancelled.short_description = 'Mark as cancelled'
