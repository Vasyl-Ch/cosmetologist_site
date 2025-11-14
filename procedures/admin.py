from django.contrib import admin
from django.utils.safestring import mark_safe


from .models import ProcedureType, Procedure


@admin.register(ProcedureType)
class ProcedureTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "preview_image")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("preview_image",)

    def preview_image(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" width="100" height="100" style="object-fit: cover;" />'
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

    def price_display_admin(self, obj):
        return mark_safe(obj.get_price_display())

    price_display_admin.short_description = "Ціна"
    price_display_admin.admin_order_field = "price"

    def preview_image(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" width="80" height="80" style="object-fit: cover;" />'
            )
        return "Немає фото"

    preview_image.short_description = "Фото"

    def get_price_display(self, obj):
        return obj.get_price_display()

    get_price_display.short_description = "Ціна"
