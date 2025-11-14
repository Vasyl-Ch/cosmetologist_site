from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Brand, Product


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "preview_image")
    search_fields = ("name", "country")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("preview_image",)

    def preview_image(self, obj):
        if obj.image:
            return mark_safe(
                f"<img src='{obj.image.url}' width='80' height='80' style='object-fit: cover;' />"
            )
        return "Нет логотипа"

    preview_image.short_description = "Логотип"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "brand", "price_display_admin", "preview_image")
    search_fields = ("name", "brand__name")
    list_filter = ("brand",)
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("preview_image",)

    def price_display_admin(self, obj):
        return mark_safe(obj.get_price_display())

    price_display_admin.short_description = "Цена"
    price_display_admin.admin_order_field = "price"

    def preview_image(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" width="80" height="80" style="object-fit: cover;" />'
            )
        return "Нет фото"

    preview_image.short_description = "Фото"
