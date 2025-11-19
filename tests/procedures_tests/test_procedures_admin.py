from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from procedures.models import ProcedureType, Procedure
from procedures.admin import ProcedureTypeAdmin, ProcedureAdmin
from decimal import Decimal
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image


class ProceduresAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.type_admin = ProcedureTypeAdmin(ProcedureType, self.site)
        self.proc_admin = ProcedureAdmin(Procedure, self.site)

        self.admin = User.objects.create_superuser("admin", "a@a.com", "pass")
        self.client.login(username="admin", password="pass")

        self.image = self._create_image()

    def _create_image(self):
        file = BytesIO()
        Image.new("RGB", (120, 120), "purple").save(file, 'JPEG')
        file.seek(0)
        return SimpleUploadedFile("admin.jpg", file.read(), "image/jpeg")

    def test_type_admin_config(self):
        self.assertEqual(self.type_admin.list_display, ("name", "preview_image"))
        self.assertEqual(self.type_admin.search_fields, ("name",))
        self.assertEqual(self.type_admin.prepopulated_fields, {"slug": ("name",)})
        self.assertIn("preview_image", self.type_admin.readonly_fields)

    def test_type_preview_image(self):
        ptype = ProcedureType.objects.create(name="Тест", image=self.image)
        preview = self.type_admin.preview_image(ptype)
        self.assertIn('src="', preview)
        self.assertIn('width="100"', preview)
        self.assertIn('object-fit: cover', preview)

    def test_type_preview_no_image(self):
        ptype = ProcedureType.objects.create(name="Без фото")
        self.assertEqual(self.type_admin.preview_image(ptype), "Немає фото")

    def test_procedure_admin_config(self):
        self.assertEqual(
            self.proc_admin.list_display,
            ("name", "type", "price_display_admin", "duration_minutes", "preview_image")
        )
        self.assertEqual(self.proc_admin.search_fields, ("name", "type__name"))
        self.assertIn("type", self.proc_admin.list_filter)
        self.assertEqual(self.proc_admin.prepopulated_fields, {"slug": ("name",)})
        self.assertIn("preview_image", self.proc_admin.readonly_fields)

    def test_price_display_admin_regular(self):
        ptype = ProcedureType.objects.create(name="T", image=self.image)
        proc = Procedure.objects.create(name="P", type=ptype, image=self.image, price=Decimal("600"))
        self.assertEqual(self.proc_admin.price_display_admin(proc), "600\u00a0₴")

    def test_price_display_admin_discount(self):
        ptype = ProcedureType.objects.create(name="T", image=self.image)
        proc = Procedure.objects.create(
            name="P", type=ptype, image=self.image,
            price=Decimal("1500"), discount_price=Decimal("1100")
        )
        expected = (
            "<del style='color: #999;'>1\u202f500\u00a0₴</del> "
            "<strong style='color: #e74c3c;'>1\u202f100\u00a0₴</strong>"
        )
        self.assertHTMLEqual(self.proc_admin.price_display_admin(proc), expected)

    def test_price_display_admin_no_price(self):
        ptype = ProcedureType.objects.create(name="T", image=self.image)
        proc = Procedure.objects.create(name="P", type=ptype, image=self.image)
        expected = "<em style='color: #999;'>Вартість уточнюйте</em>"
        self.assertHTMLEqual(self.proc_admin.price_display_admin(proc), expected)

    def test_procedure_preview_image(self):
        ptype = ProcedureType.objects.create(name="T", image=self.image)
        proc = Procedure.objects.create(name="P", type=ptype, image=self.image)
        preview = self.proc_admin.preview_image(proc)
        self.assertIn('width="80"', preview)
        self.assertIn('object-fit: cover', preview)
