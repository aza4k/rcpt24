from django.contrib import admin
from .models import Medicine, Pharmacy, Inventory, News

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "short_description", "has_image")
    search_fields = ("name", "analogs")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)

    def short_description(self, obj):
        return (obj.description[:60] + "...") if obj.description and len(obj.description) > 60 else obj.description
    short_description.short_description = "Tavsif"

    def has_image(self, obj):
        return bool(obj.image)
    has_image.boolean = True
    has_image.short_description = "Rasm bor"

@admin.register(Pharmacy)
class PharmacyAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "phone", "lat", "lng", "working_hours")
    search_fields = ("name", "address", "phone")
    list_filter = ("working_hours",)
    ordering = ("name",)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ("medicine", "pharmacy", "quantity", "price", "updated_at")
    list_filter = ("pharmacy", "medicine")
    search_fields = ("medicine__name", "pharmacy__name")
    autocomplete_fields = ("medicine", "pharmacy")
    ordering = ("medicine",)

    def updated_at(self, obj):
        return obj.pk and obj.__dict__.get("updated_at") or None
