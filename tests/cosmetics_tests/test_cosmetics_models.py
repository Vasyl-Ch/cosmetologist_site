from django.test import TestCase
from django.utils.text import slugify
from decimal import Decimal
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image


from cosmetics.models import Brand, Product


class BrandModelTest(TestCase):
    def _create_image(self):
        file = BytesIO()
        Image.new("RGB", (100, 100), "red").save(file, 'JPEG')
        file.seek(0)
        return SimpleUploadedFile("brand.jpg", file.read(), "image/jpeg")

    def test_str(self):
        brand = Brand.objects.create(name="L'Oréal", image=self._create_image())
        self.assertEqual(str(brand), "L'Oréal")


class ProductModelTest(TestCase):
    def setUp(self):
        self.image = self._create_image()
        self.brand = Brand.objects.create(name="TestBrand", image=self.image)

    def _create_image(self):
        file = BytesIO()
        Image.new("RGB", (100, 100), "blue").save(file, 'JPEG')
        file.seek(0)
        return SimpleUploadedFile("product.jpg", file.read(), "image/jpeg")

    def test_str(self):
        product = Product.objects.create(name="Крем для лица", brand=self.brand, image=self.image)
        self.assertEqual(str(product), "Крем для лица")

    def test_slug_auto_generation(self):
        product = Product.objects.create(name="Продукт с пробелами!", brand=self.brand, image=self.image)
        self.assertEqual(product.slug, slugify("Продукт с пробелами!"))

    def test_get_price_display_regular_price(self):
        product = Product.objects.create(
            name="Тест", brand=self.brand, image=self.image, price=Decimal("500.00")
        )
        self.assertEqual(product.get_price_display(), "500\u00a0₴")

    def test_get_price_display_with_discount(self):
        product = Product.objects.create(
            name="Тест", brand=self.brand, image=self.image,
            price=Decimal("1000.00"), discount_price=Decimal("750.00")
        )
        expected = (
            '<span style=\'text-decoration: line-through; color: #999;\'>1\u202f000\u00a0₴</span> '
            '<span style=\'color: #e74c3c; font-weight: bold;\'>750\u00a0₴</span>'
        )
        self.assertHTMLEqual(product.get_price_display(), expected)

    def test_get_price_display_no_price(self):
        product = Product.objects.create(name="Тест", brand=self.brand, image=self.image)
        expected = '<span style=\'color: #999; font-style: italic;\'>Вартість уточнюйте</span>'
        self.assertHTMLEqual(product.get_price_display(), expected)
