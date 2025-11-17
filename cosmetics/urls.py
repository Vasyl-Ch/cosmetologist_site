from django.urls import path
from . import views

urlpatterns = [
    path("", views.brands_list, name="brands_list"),
    path("<slug:slug>/", views.products_by_brand, name="products_by_brand"),
]
