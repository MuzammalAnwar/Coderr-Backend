from django.contrib import admin
from .models import Offer, OfferDetail


class OfferDetailInline(admin.TabularInline):
    model = OfferDetail
    extra = 0
    fields = ('offer_type', 'title', 'price', 'revisions', 'delivery_time_in_days', 'features')
    show_change_link = True


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'business_user',
        'created_at',
        'updated_at',
        'details_count',
    )
    list_filter = ('created_at', 'updated_at')
    search_fields = (
        'title',
        'description',
        'business_user__username',
        'business_user__email',
    )
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('business_user',)
    list_select_related = ('business_user',)
    inlines = [OfferDetailInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('details', 'business_user')

    def details_count(self, obj):
        return obj.details.count()
    details_count.short_description = 'details'


@admin.register(OfferDetail)
class OfferDetailAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'offer',
        'offer_type',
        'title',
        'price',
        'revisions',
        'delivery_time_in_days',
    )
    list_filter = ('offer_type', 'delivery_time_in_days', 'price')
    search_fields = (
        'offer__title',
        'title',
        'offer__business_user__username',
        'offer__business_user__email',
    )
    raw_id_fields = ('offer',)
    list_select_related = ('offer', 'offer__business_user')
