from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from api_moneypit.core.models import BulkOrder
from api_moneypit.core.models import Order
from api_moneypit.core.models import Ticker


class TickerResource(resources.ModelResource):
    class Meta:
        model = Ticker
        fields = ("symbol", "name", "price")
        export_order = ("symbol", "name", "price")


@admin.register(Ticker)
class TickerAdmin(ImportExportModelAdmin):
    list_display = ["symbol", "name", "price"]
    search_fields = ["symbol", "name"]
    list_filter = ["symbol", "name"]

    resource_class = TickerResource


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["ticker", "type", "qty"]
    search_fields = ["ticker", "user"]
    list_filter = ["ticker", "user", "type"]


@admin.register(BulkOrder)
class BulkOrderAdmin(admin.ModelAdmin):
    list_display = ["user", "is_processed"]
    search_fields = ["user"]
    list_filter = ["is_processed"]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["file"]
        return []

    def has_add_permission(self, request):
        return False
