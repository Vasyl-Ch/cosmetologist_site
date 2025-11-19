from django.contrib import admin
from django.utils.html import format_html
from django.http import HttpRequest


from .models import Review, Certificate, ContactInfo, HomePageSettings


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("author_name", "created_at", "preview_image")
    search_fields = ("author_name", "text")
    readonly_fields = ("preview_image",)

    def preview_image(self, obj) -> str:
        if obj.image:
            return format_html(
                '<img src="{}" width="{}" height="{}" style="{}" />',
                obj.image.url,
                100,
                100,
                "object-fit: cover;",
            )
        return "Немає фото"

    preview_image.short_description = "Фото"


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ("title", "preview_image")
    search_fields = ("title",)
    readonly_fields = ("preview_image",)

    def preview_image(self, obj) -> str:
        return format_html(
            '<img src="{}" width="{}" height="{}" />',
            obj.image.url,
            100,
            100,
        )

    preview_image.short_description = "Сертифікат"


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ("phone", "address")

    def has_add_permission(self, request: HttpRequest) -> bool:
        return not ContactInfo.objects.exists()


@admin.register(HomePageSettings)
class HomePageSettingsAdmin(admin.ModelAdmin):
    list_display = ("procedures_image", "cosmetics_image")

    def has_add_permission(self, request: HttpRequest) -> bool:
        return not HomePageSettings.objects.exists()
