from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image


from core.models import Review, Certificate, ContactInfo
from core.admin import ReviewAdmin, CertificateAdmin, ContactInfoAdmin


class CoreAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.review_admin = ReviewAdmin(Review, self.site)
        self.cert_admin = CertificateAdmin(Certificate, self.site)
        self.contact_admin = ContactInfoAdmin(ContactInfo, self.site)

        self.admin_user = User.objects.create_superuser(
            username="admin", email="a@a.com", password="pass"
        )
        self.client.login(username="admin", password="pass")

        self.image = self._create_image()

    def _create_image(self):
        file = BytesIO()
        Image.new("RGB", (150, 150), "purple").save(file, 'JPEG')
        file.seek(0)
        return SimpleUploadedFile("admin.jpg", file.read(), "image/jpeg")

    def test_review_admin_config(self):
        self.assertEqual(self.review_admin.list_display, ("author_name", "created_at", "preview_image"))
        self.assertEqual(self.review_admin.search_fields, ("author_name", "text"))
        self.assertIn("preview_image", self.review_admin.readonly_fields)

    def test_review_preview_image(self):
        review = Review.objects.create(author_name="Тест", text="...", image=self.image)
        preview = self.review_admin.preview_image(review)
        self.assertIn('src="', preview)
        self.assertIn('width="100"', preview)
        self.assertIn('object-fit: cover', preview)

    def test_review_preview_no_image(self):
        review = Review.objects.create(author_name="Без фото", text="...")
        self.assertEqual(self.review_admin.preview_image(review), "Немає фото")

    def test_certificate_admin_config(self):
        self.assertEqual(self.cert_admin.list_display, ("title", "preview_image"))
        self.assertEqual(self.cert_admin.search_fields, ("title",))
        self.assertIn("preview_image", self.cert_admin.readonly_fields)

    def test_certificate_preview_image(self):
        cert = Certificate.objects.create(title="Серт", image=self.image)
        preview = self.cert_admin.preview_image(cert)
        self.assertIn('src="', preview)
        self.assertIn('width="100"', preview)
        self.assertIn('height="100"', preview)

    def test_contact_admin_config(self):
        self.assertEqual(self.contact_admin.list_display, ("phone", "address"))

    def test_contact_has_add_permission(self):
        # Нет записей — можно добавлять
        self.assertTrue(self.contact_admin.has_add_permission(None))

        ContactInfo.objects.create(phone="+373 123", address="Test")
        # Есть запись — нельзя добавлять
        self.assertFalse(self.contact_admin.has_add_permission(None))
