from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from django.contrib import admin as django_admin
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image


from articles.models import Tag, Article
from articles.admin import TagAdmin, ArticleAdmin


class AdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.tag_admin = TagAdmin(Tag, self.site)
        self.article_admin = ArticleAdmin(Article, self.site)

        self.superuser = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="pass"
        )
        self.client.login(username="admin", password="pass")

        self.image = self._create_image()

    def _create_image(self):
        file = BytesIO()
        Image.new("RGB", (200, 200), "purple").save(file, 'JPEG')
        file.seek(0)
        return SimpleUploadedFile("admin_test.jpg", file.read(), "image/jpeg")

    def test_tag_admin_registered_and_fields(self):
        self.assertIn(Tag, django_admin.site._registry)
        self.assertEqual(self.tag_admin.list_display, ("name", "slug"))
        self.assertEqual(self.tag_admin.search_fields, ("name",))
        self.assertEqual(self.tag_admin.prepopulated_fields, {"slug": ("name",)})

    def test_article_admin_registered_and_fields(self):
        self.assertIn(Article, django_admin.site._registry)
        self.assertEqual(self.article_admin.list_display, ("title", "created_at", "preview_image"))
        self.assertEqual(self.article_admin.search_fields, ("title", "content"))
        self.assertIn("tags", self.article_admin.list_filter)
        self.assertEqual(self.article_admin.prepopulated_fields, {"slug": ("title",)})
        self.assertEqual(self.article_admin.filter_horizontal, ("tags",))
        self.assertIn("preview_image", self.article_admin.readonly_fields)

    def test_preview_image_output(self):
        article = Article.objects.create(title="Тест", content="...", image=self.image)
        preview = self.article_admin.preview_image(article)
        self.assertIn('src="', preview)
        self.assertIn('width="100"', preview)
        self.assertIn('object-fit: cover', preview)

    def test_preview_image_no_image(self):
        article = Article(title="Без фото", content="...")
        preview = self.article_admin.preview_image(article)
        self.assertEqual(preview, "Нет изображения")
