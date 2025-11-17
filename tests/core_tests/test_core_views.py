from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image


from core.models import Review, Certificate, ContactInfo
from procedures.models import ProcedureType
from cosmetics.models import Brand
from articles.models import Article


class CoreViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.image = self._create_image()
        self.contact = ContactInfo.objects.create(
            phone="+373 000 111 222",
            address="ул. Пушкина, 10",
            telegram_url="https://t.me/test"
        )

    def _create_image(self):
        file = BytesIO()
        Image.new("RGB", (100, 100), "green").save(file, 'JPEG')
        file.seek(0)
        return SimpleUploadedFile("test.jpg", file.read(), "image/jpeg")

    def test_home_status_and_template(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/home.html")

    def test_home_context_data(self):
        # Создаём минимальные данные
        Review.objects.create(author_name="А", text="...", image=self.image)
        Certificate.objects.create(title="Серт", image=self.image)
        ProcedureType.objects.create(name="Тип", image=self.image)
        Brand.objects.create(name="Бренд", image=self.image)
        Article.objects.create(title="Статья", content="...", image=self.image)

        response = self.client.get(reverse("home"))

        self.assertIn("reviews", response.context)
        self.assertIn("certificates", response.context)
        self.assertEqual(response.context["contact_info"], self.contact)
        self.assertEqual(response.context["page_title"], "Головна")
        self.assertEqual(response.context["procedure_types"].count(), 1)
        self.assertEqual(response.context["brands"].count(), 1)
        self.assertEqual(response.context["recent_articles"].count(), 1)

    def test_contacts_status_and_template(self):
        response = self.client.get(reverse("contacts"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/contacts.html")

    def test_contacts_context(self):
        response = self.client.get(reverse("contacts"))
        self.assertEqual(response.context["contact_info"], self.contact)
        self.assertEqual(response.context["page_title"], "Контакти")

    def test_context_processor(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.context["contact_info"], self.contact)
