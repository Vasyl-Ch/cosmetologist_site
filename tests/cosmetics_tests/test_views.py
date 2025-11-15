from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image


from cosmetics.models import Brand, Product


class CosmeticsViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.image = self._create_image()
        self.brand1 = Brand.objects.create(name="BrandA", image=self.image, country="FR")
        self.brand2 = Brand.objects.create(name="BrandB", image=self.image)
        self.product1 = Product.objects.create(
            name="Крем", brand=self.brand1, image=self.image, price=300
        )
        self.product2 = Product.objects.create(
            name="Маска", brand=self.brand1, image=self.image
        )

    def _create_image(self):
        file = BytesIO()
        Image.new("RGB", (100, 100), "green").save(file, 'JPEG')
        file.seek(0)
        return SimpleUploadedFile("img.jpg", file.read(), "image/jpeg")

    def test_brands_list_status_and_template(self):
        response = self.client.get(reverse("brands_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cosmetics/brands_list.html")

    def test_brands_list_search(self):
        response = self.client.get(reverse("brands_list"), {"q": "BrandA"})
        self.assertContains(response, "BrandA")
        self.assertNotContains(response, "BrandB")

    def test_brands_list_context(self):
        response = self.client.get(reverse("brands_list"), {"q": "test"})
        self.assertIn("page_obj", response.context)
        self.assertEqual(response.context["query"], "test")
        self.assertEqual(response.context["page_title"], "Косметика")

    def test_products_by_brand_200_and_template(self):
        response = self.client.get(reverse("products_by_brand", args=[self.brand1.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cosmetics/products_list.html")

    def test_products_by_brand_404(self):
        response = self.client.get(reverse("products_by_brand", args=["non-existent"]))
        self.assertEqual(response.status_code, 404)

    def test_products_by_brand_search(self):
        response = self.client.get(
            reverse("products_by_brand", args=[self.brand1.slug]), {"q": "Крем"}
        )
        self.assertContains(response, "Крем")
        self.assertNotContains(response, "Маска")

    def test_products_by_brand_context(self):
        response = self.client.get(reverse("products_by_brand", args=[self.brand1.slug]))
        self.assertEqual(response.context["brand"], self.brand1)
        self.assertIn("page_obj", response.context)
        self.assertIn("all_brands", response.context)
        self.assertEqual(response.context["page_title"], self.brand1.name)
