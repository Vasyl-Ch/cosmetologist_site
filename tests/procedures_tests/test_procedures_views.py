from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image


from procedures.models import ProcedureType, Procedure


class ProceduresViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.image = self._create_image()
        self.type1 = ProcedureType.objects.create(name="Тип A", image=self.image)
        self.type2 = ProcedureType.objects.create(name="Тип B", image=self.image)
        self.proc1 = Procedure.objects.create(
            name="Процедура 1", type=self.type1, image=self.image, price=500
        )
        self.proc2 = Procedure.objects.create(
            name="Процедура 2", type=self.type1, image=self.image
        )

    def _create_image(self):
        file = BytesIO()
        Image.new("RGB", (100, 100), "green").save(file, 'JPEG')
        file.seek(0)
        return SimpleUploadedFile("img.jpg", file.read(), "image/jpeg")

    def test_procedure_types_list_status_and_template(self):
        response = self.client.get(reverse("procedure_types_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "procedures/types_list.html")

    def test_procedure_types_list_search(self):
        response = self.client.get(reverse("procedure_types_list"), {"q": "Тип A"})
        self.assertContains(response, "Тип A")
        self.assertNotContains(response, "Тип B")

    def test_procedure_types_list_context(self):
        response = self.client.get(reverse("procedure_types_list"), {"q": "test"})
        self.assertIn("procedure_types", response.context)
        self.assertEqual(response.context["query"], "test")
        self.assertEqual(response.context["page_title"], "Перелік процедур")

    def test_procedures_by_type_200_and_template(self):
        response = self.client.get(reverse("procedures_by_type", args=[self.type1.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "procedures/procedures_list.html")

    def test_procedures_by_type_404(self):
        response = self.client.get(reverse("procedures_by_type", args=["non-existent"]))
        self.assertEqual(response.status_code, 404)

    def test_procedures_by_type_search(self):
        response = self.client.get(
            reverse("procedures_by_type", args=[self.type1.slug]), {"q": "Процедура 1"}
        )
        self.assertContains(response, "Процедура 1")
        self.assertNotContains(response, "Процедура 2")

    def test_procedures_by_type_context(self):
        response = self.client.get(reverse("procedures_by_type", args=[self.type1.slug]))
        self.assertEqual(response.context["procedure_type"], self.type1)
        self.assertIn("page_obj", response.context)
        self.assertIn("all_procedure_types", response.context)
        self.assertEqual(response.context["current_type_slug"], self.type1.slug)
        self.assertEqual(response.context["page_title"], self.type1.name)
