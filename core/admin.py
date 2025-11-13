from django.contrib import admin
from django.utils.safestring import mark_safe


from .models import Review, Certificate, ContactInfo


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("author_name", "created_at", "preview_image")
    search_fields = ("author_name", "text")
    readonly_fields = ("preview_image",)

    def preview_image(self, obj):
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width='100' height='100' style='object-fit: cover;' />")
        return "Нет фото"
    preview_image.short_description = "Фото"


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ("title", "preview_image")
    search_fields = ("title",)
    readonly_fields = ("preview_image",)

    def preview_image(self, obj):
        return mark_safe(f"<img src='{obj.image.url}' width='100' height='100' />")
    preview_image.short_description = "Сертификат"


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ("phone", "address")
    def has_add_permission(self, request):
        # Разрешаем только одну запись
        return not ContactInfo.objects.exists()
