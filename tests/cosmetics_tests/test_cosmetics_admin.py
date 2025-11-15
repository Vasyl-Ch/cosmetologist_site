from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from decimal import Decimal
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image


from cosmetics.models import Brand, Product
from cosmetics.admin import BrandAdmin, ProductAdmin


class CosmeticsAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.brand_admin = BrandAdmin(Brand, self.site)
        self.product_admin = ProductAdmin(Product, self.site)

        self.admin = User.objects.create_superuser("admin", "a@a.com", "pass")
        self.client.login(username="admin", password="pass")

        self.image = self._create_image()

    def _create_image(self):
        file = BytesIO()
        Image.new("RGB", (120, 120), "purple").save(file, 'JPEG')
        file.seek(0)
        return SimpleUploadedFile("admin.jpg", file.read(), "image/jpeg")

    def test_brand_admin_config(self):
        self.assertEqual(self.brand_admin.list_display, ("name", "country", "preview_image"))
        self.assertEqual(self.brand_admin.search_fields, ("name", "country"))
        self.assertEqual(self.brand_admin.prepopulated_fields, {"slug": ("name",)})
        self.assertIn("preview_image", self.brand_admin.readonly_fields)

    def test_brand_preview_image(self):
        brand = Brand.objects.create(name="Test", image=self.image)
        preview = self.brand_admin.preview_image(brand)
        self.assertIn('src="', preview)
        self.assertIn('width="80"', preview)
        self.assertIn('object-fit: cover', preview)

    def test_brand_preview_no_image(self):
        brand = Brand.objects.create(name="NoLogo")
        self.assertEqual(self.brand_admin.preview_image(brand), "Немає логотипа")

    def test_product_admin_config(self):
        self.assertEqual(
            self.product_admin.list_display,
            ("name", "brand", "price_display_admin", "preview_image")
        )
        self.assertEqual(self.product_admin.search_fields, ("name", "brand__name"))
        self.assertIn("brand", self.product_admin.list_filter)
        self.assertEqual(self.product_admin.prepopulated_fields, {"slug": ("name",)})
        self.assertIn("preview_image", self.product_admin.readonly_fields)

    def test_price_display_admin_regular(self):
        brand = Brand.objects.create(name="B", image=self.image)
        product = Product.objects.create(name="P", brand=brand, image=self.image, price=Decimal("400"))
        self.assertEqual(self.product_admin.price_display_admin(product), "400 ₴")

    def test_price_display_admin_discount(self):
        brand = Brand.objects.create(name="B", image=self.image)
        product = Product.objects.create(
            name="P", brand=brand, image=self.image,
            price=Decimal("1000"), discount_price=Decimal("700")
        )
        expected = (
            '<span style=\'text-decoration: line-through; color: #999;\'>1000 ₴</span> '
            '<span style=\'color: #e74c3c; font-weight: bold;\'>700 ₴</span>'
        )
        self.assertHTMLEqual(self.product_admin.price_display_admin(product), expected)

    def test_price_display_admin_no_price(self):
        brand = Brand.objects.create(name="B", image=self.image)
        product = Product.objects.create(name="P", brand=brand, image=self.image)
        expected = '<span style=\'color: #999; font-style: italic;\'>Вартість уточнюйте</span>'
        self.assertHTMLEqual(self.product_admin.price_display_admin(product), expected)

    def test_product_preview_image(self):
        brand = Brand.objects.create(name="B", image=self.image)
        product = Product.objects.create(name="P", brand=brand, image=self.image)
        preview = self.product_admin.preview_image(product)
        self.assertIn('width="80"', preview)
        self.assertIn('object-fit: cover', preview)
