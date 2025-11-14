from django.db import models
from django.utils.safestring import mark_safe
from django.utils.text import slugify


class ProcedureType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="procedure_types/")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Procedure(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="procedures/")
    duration_minutes = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(
        blank=True,
        null=True,
        max_digits=10,
        decimal_places=2,
        help_text="Залиште порожнім, якщо ціна не фіксована",
    )
    discount_price = models.DecimalField(
        blank=True,
        null=True,
        max_digits=10,
        decimal_places=2,
        help_text="Акційна ціна",
    )
    slug = models.SlugField(unique=True)
    type = models.ForeignKey(
        ProcedureType, on_delete=models.CASCADE, related_name="procedures"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_price_display(self):
        if self.discount_price and self.discount_price < (self.price or float("inf")):
            return mark_safe(
                f"<del style='color: #999;'>{self.price} ₴</del> "
                f"<strong style='color: #e74c3c;'>{self.discount_price} ₴</strong>"
            )
        elif self.price:
            return f"{self.price} ₴"
        else:
            return mark_safe("<em style='color: #999;'>Вартість уточнюйте</em>")
