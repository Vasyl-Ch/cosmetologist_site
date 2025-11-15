from django.db import models


class Review(models.Model):
    author_name = models.CharField(max_length=100)
    text = models.TextField()
    image = models.ImageField(upload_to="reviews/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.author_name


class Certificate(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="certificates/")

    def __str__(self) -> str:
        return self.title or "Certificate"


class ContactInfo(models.Model):
    phone = models.CharField(max_length=20)
    telegram_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    address = models.CharField(max_length=255)
    map_embed_url = models.URLField(blank=True)

    def __str__(self) -> str:
        return self.phone
