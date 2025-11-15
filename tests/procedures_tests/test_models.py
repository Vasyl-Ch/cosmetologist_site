from django.test import TestCase
from django.utils.text import slugify
from decimal import Decimal
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image


from procedures.models import ProcedureType, Procedure


class ProcedureTypeModelTest(TestCase):
    def _create_image(self):
        file = BytesIO()
        Image.new("RGB", (100, 100), "red").save(file, 'JPEG')
        file.seek(0)
        return SimpleUploadedFile("type.jpg", file.read(), "image/jpeg")

    def test_str(self):
        ptype = ProcedureType.objects.create(name="Масаж обличчя", image=self._create_image())
        self.assertEqual(str(ptype), "Масаж обличчя")

    def test_slug_auto_generation(self):
        ptype = ProcedureType.objects.create(name="Чистка з пробелами!", image=self._create_image())
        self.assertEqual(ptype.slug, slugify("Чистка з пробелами!"))


class ProcedureModelTest(TestCase):
    def setUp(self):
        self.image = self._create_image()
        self.ptype = ProcedureType.objects.create(name="Косметологія", image=self.image)

    def _create_image(self):
        file = BytesIO()
        Image.new("RGB", (100, 100), "blue").save(file, 'JPEG')
        file.seek(0)
        return SimpleUploadedFile("proc.jpg", file.read(), "image/jpeg")

    def test_str(self):
        proc = Procedure.objects.create(name="Глибока чистка", type=self.ptype, image=self.image)
        self.assertEqual(str(proc), "Глибока чистка")

    def test_slug_auto_generation(self):
        proc = Procedure.objects.create(name="Процедура з знаками!!!", type=self.ptype, image=self.image)
        self.assertEqual(proc.slug, slugify("Процедура з знаками!!!"))

    def test_get_price_display_regular(self):
        proc = Procedure.objects.create(
            name="Тест", type=self.ptype, image=self.image, price=Decimal("800.00")
        )
        self.assertEqual(proc.get_price_display(), "800.00 ₴")

    def test_get_price_display_with_discount(self):
        proc = Procedure.objects.create(
            name="Тест", type=self.ptype, image=self.image,
            price=Decimal("1200.00"), discount_price=Decimal("900.00")
        )
        expected = (
            "<del style='color: #999;'>1200.00 ₴</del> "
            "<strong style='color: #e74c3c;'>900.00 ₴</strong>"
        )
        self.assertHTMLEqual(proc.get_price_display(), expected)

    def test_get_price_display_no_price(self):
        proc = Procedure.objects.create(name="Тест", type=self.ptype, image=self.image)
        expected = "<em style='color: #999;'>Вартість уточнюйте</em>"
        self.assertHTMLEqual(proc.get_price_display(), expected)
