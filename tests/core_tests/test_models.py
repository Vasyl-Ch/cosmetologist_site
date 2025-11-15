from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image


from core.models import Review, Certificate, ContactInfo


class ReviewModelTest(TestCase):
    def _create_image(self):
        file = BytesIO()
        Image.new("RGB", (100, 100), "red").save(file, 'JPEG')
        file.seek(0)
        return SimpleUploadedFile("review.jpg", file.read(), "image/jpeg")

    def test_str(self):
        review = Review.objects.create(author_name="Анна", text="Отлично!")
        self.assertEqual(str(review), "Анна")

    def test_with_image(self):
        image = self._create_image()
        review = Review.objects.create(author_name="Мария", text="...", image=image)
        self.assertTrue(review.image)

    def test_without_image(self):
        review = Review.objects.create(author_name="Ольга", text="...")
        self.assertFalse(review.image)


class CertificateModelTest(TestCase):
    def _create_image(self):
        file = BytesIO()
        Image.new("RGB", (200, 150), "blue").save(file, 'JPEG')
        file.seek(0)
        return SimpleUploadedFile("cert.jpg", file.read(), "image/jpeg")

    def test_str_with_title(self):
        cert = Certificate.objects.create(title="Диплом косметолога", image=self._create_image())
        self.assertEqual(str(cert), "Диплом косметолога")

    def test_str_without_title(self):
        cert = Certificate.objects.create(image=self._create_image())
        self.assertEqual(str(cert), "Certificate")


class ContactInfoModelTest(TestCase):
    def test_str(self):
        contact = ContactInfo.objects.create(phone="+373 123 456 789", address="Кишинёв")
        self.assertEqual(str(contact), "+373 123 456 789")
