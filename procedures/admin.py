from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe


from .models import ProcedureType, Procedure


@admin.register(ProcedureType)
class ProcedureTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "preview_image")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("preview_image",)

    def preview_image(self, obj) -> str:
        if obj.image:
            return format_html(
                "<img src=\"{}\" width=\"{}\" height=\"{}\" style=\"{}\" />",
                obj.image.url,
                100,
                100,
                "object-fit: cover;",
            )
        return "Немає фото"

    preview_image.short_description = "Фото"


@admin.register(Procedure)
class ProcedureAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "type",
        "price_display_admin",
        "duration_minutes",
        "preview_image",
    )
    search_fields = ("name", "type__name")
    list_filter = ("type",)
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("preview_image",)

    def price_display_admin(self, obj) -> str:
        return mark_safe(obj.get_price_display())

    price_display_admin.short_description = "Ціна"
    price_display_admin.admin_order_field = "price"

    def preview_image(self, obj) -> str:
        if obj.image:
            return format_html(
                "<img src=\"{}\" width=\"{}\" height=\"{}\" style=\"{}\" />",
                obj.image.url,
                80,
                80,
                "object-fit: cover;",
            )
        return "Немає фото"

    preview_image.short_description = "Фото"

    def get_price_display(self, obj) -> str:
        return obj.get_price_display()

    get_price_display.short_description = "Ціна"
