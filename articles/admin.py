from django.contrib import admin
from django.utils.html import format_html


from .models import Tag, Article


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "preview_image")
    search_fields = ("title", "content")
    list_filter = ("tags", "created_at")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)
    readonly_fields = ("preview_image",)

    def preview_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="{}" height="{}" style="{}" />',
                obj.image.url,
                100,
                100,
                "object-fit: cover;",
            )
        return "Нет изображения"

    preview_image.short_description = "Превью"
