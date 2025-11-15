from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Brand, Product


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "preview_image")
    search_fields = ("name", "country")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("preview_image",)

    def preview_image(self, obj) -> str:
        if obj.image:
            return format_html(
                '<img src="{}" width="{}" height="{}" style="{}" />',
                obj.image.url,
                80,
                80,
                "object-fit: cover;",
            )
        return "Немає логотипа"

    preview_image.short_description = "Логотип"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "brand", "price_display_admin", "preview_image")
    search_fields = ("name", "brand__name")
    list_filter = ("brand",)
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("preview_image",)

    def price_display_admin(self, obj) -> str:
        return mark_safe(obj.get_price_display())

    price_display_admin.short_description = "Ціна"
    price_display_admin.admin_order_field = "price"

    def preview_image(self, obj) -> str:
        if obj.image:
            return format_html(
                '<img src="{}" width="{}" height="{}" style="{}" />',
                obj.image.url,
                80,
                80,
                "object-fit: cover;",
            )
        return "Немає фото"

    preview_image.short_description = "Фото"
