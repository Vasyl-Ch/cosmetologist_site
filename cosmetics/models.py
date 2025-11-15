from django.db import models
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from decimal import Decimal, ROUND_HALF_UP


class Brand(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="brands/")
    country = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="products/")
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
        help_text="Акційна ціна (менша за звичайну)",
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name="products",
    )
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_price_display(self):
        def _fmt(amount):
            if amount is None:
                return ""
            if not isinstance(amount, Decimal):
                amount = Decimal(str(amount))
            return format(amount.quantize(Decimal(0), rounding=ROUND_HALF_UP), ".0f")

        if (
            self.discount_price
            and self.discount_price < (self.price or float("inf"))
        ):
            return format_html(
                (
                    "<span style='text-decoration: line-through; "
                    "color: #999;'>" "{} ₴</span> "
                    "<span style='color: #e74c3c; "
                    "font-weight: bold;'>{} ₴</span>"
                ),
                _fmt(self.price),
                _fmt(self.discount_price),
            )
        if self.price:
            return f"{_fmt(self.price)} ₴"
        return mark_safe(
            (
                "<span style='color: #999; font-style: italic;'>"
                "Вартість уточнюйте</span>"
            )
        )
