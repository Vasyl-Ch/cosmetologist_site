from django.db import models
from django.utils.text import slugify


class Brand(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="brands/")
    country = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="products/")
    price = models.DecimalField(
        blank=True,
        null=True,
        max_digits=10,
        decimal_places=2,
        help_text="Оставьте пустым, если цена не фиксирована"
    )
    discount_price = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="products")
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_price_display(self):
        if self.price:
            return f"{self.price} ₴"
        return "Вартість уточнюйте."
