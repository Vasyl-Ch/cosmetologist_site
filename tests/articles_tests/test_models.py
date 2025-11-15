from django.test import TestCase
from django.utils.text import slugify
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile


from articles.models import Tag, Article


class TagModelTest(TestCase):
    def test_str(self):
        tag = Tag.objects.create(name="Уход за кожей")
        self.assertEqual(str(tag), "Уход за кожей")

    def test_slug_auto_generation(self):
        tag = Tag.objects.create(name="Тестовый Тег!")
        expected_slug = slugify("Тестовый Тег!")
        self.assertEqual(tag.slug, expected_slug)


class ArticleModelTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="Красота")
        self.image = self._create_test_image()

    def _create_test_image(self):
        file = BytesIO()
        image = Image.new("RGB", (100, 100), color="red")
        image.save(file, 'JPEG')
        file.seek(0)
        return SimpleUploadedFile("test.jpg", file.read(), content_type="image/jpeg")

    def test_str(self):
        article = Article.objects.create(
            title="Мой первый пост",
            content="Содержание",
            image=self.image
        )
        self.assertEqual(str(article), "Мой первый пост")

    def test_slug_auto_generation(self):
        article = Article.objects.create(
            title="Статья с пробелами и знаками!!!",
            content="Текст",
            image=self.image
        )
        self.assertEqual(article.slug, slugify("Статья с пробелами и знаками!!!"))

    def test_tags_relation(self):
        article = Article.objects.create(title="Тест", content="Текст", image=self.image)
        article.tags.add(self.tag)
        self.assertIn(self.tag, article.tags.all())
