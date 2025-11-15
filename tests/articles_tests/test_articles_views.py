from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image


from articles.models import Article, Tag


class ArticlesListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.tag = Tag.objects.create(name="Уход")
        self.image = self._create_image()
        self.article1 = Article.objects.create(
            title="Первая статья", content="Текст", image=self.image, slug="pervaya-statia"
        )
        self.article1.tags.add(self.tag)
        self.article2 = Article.objects.create(
            title="Вторая статья", content="Другой текст", image=self.image, slug="vtoraya-statia"
        )

    def _create_image(self):
        file = BytesIO()
        Image.new("RGB", (100, 100), "blue").save(file, 'JPEG')
        file.seek(0)
        return SimpleUploadedFile("img.jpg", file.read(), "image/jpeg")

    def test_list_status_and_template(self):
        response = self.client.get(reverse("articles_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "articles/articles_list.html")

    def test_search_filter(self):
        response = self.client.get(reverse("articles_list"), {"q": "Первая"})
        self.assertContains(response, "Первая статья")
        self.assertNotContains(response, "Вторая статья")

    def test_tag_filter(self):
        response = self.client.get(reverse("articles_list"), {"tag": self.tag.slug})
        self.assertContains(response, "Первая статья")
        self.assertNotContains(response, "Вторая статья")

    def test_context_tags_and_query(self):
        response = self.client.get(reverse("articles_list"), {"q": "статья", "tag": self.tag.slug})
        self.assertIn("all_tags", response.context)
        self.assertEqual(response.context["query"], "статья")
        self.assertEqual(response.context["active_tag"], self.tag)


class ArticleDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.image = self._create_image()
        self.tag1 = Tag.objects.create(name="Кожа")
        self.tag2 = Tag.objects.create(name="Волосы")

        self.article = Article.objects.create(
            title="Основная статья", content="Текст", image=self.image, slug="osnovnaya"
        )
        self.article.tags.add(self.tag1, self.tag2)

        self.related = Article.objects.create(
            title="Похожая", content="...", image=self.image, slug="pohozhaya"
        )
        self.related.tags.add(self.tag1)

        self.unrelated = Article.objects.create(
            title="Несвязанная", content="...", image=self.image, slug="nesvyazannaya"
        )

    def _create_image(self):
        file = BytesIO()
        Image.new("RGB", (100, 100), "green").save(file, 'JPEG')
        file.seek(0)
        return SimpleUploadedFile("test.jpg", file.read(), "image/jpeg")

    def test_detail_200_and_template(self):
        response = self.client.get(reverse("article_detail", args=[self.article.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "articles/article_detail.html")

    def test_404_for_nonexistent(self):
        response = self.client.get(reverse("article_detail", args=["non-existent-slug"]))
        self.assertEqual(response.status_code, 404)

    def test_related_articles_by_tags(self):
        response = self.client.get(reverse("article_detail", args=[self.article.slug]))
        self.assertIn(self.related, response.context["related_articles"])
        self.assertNotIn(self.unrelated, response.context["related_articles"])

    def test_fallback_to_recent_if_not_enough_related(self):
        # Удалим общие теги у related
        self.related.tags.clear()
        Article.objects.create(title="Доп1", content="...", image=self.image, slug="dop1")
        Article.objects.create(title="Доп2", content="...", image=self.image, slug="dop2")

        response = self.client.get(reverse("article_detail", args=[self.article.slug]))
        related = response.context["related_articles"]
        self.assertEqual(len(related), 3)
        self.assertIn("Доп", related[0].title or related[1].title or related[2].title)

    def test_prev_next_navigation(self):
        older = Article.objects.create(title="Старее", content="...", image=self.image, slug="old")
        older.created_at = self.article.created_at.replace(year=self.article.created_at.year - 1)
        older.save()

        newer = Article.objects.create(title="Новее", content="...", image=self.image, slug="new")
        newer.created_at = self.article.created_at.replace(year=self.article.created_at.year + 1)
        newer.save()

        response = self.client.get(reverse("article_detail", args=[self.article.slug]))
        self.assertEqual(response.context["previous_article"], older)
        self.assertEqual(response.context["next_article"], newer)
