from django.contrib import admin
from django.utils.safestring import mark_safe


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
            return mark_safe(f"<img src='{obj.image.url}' width='100' height='100' style='object-fit: cover;' />")
        return "Нет изображения"
    preview_image.short_description = "Превью"
