from django.urls import path
from . import views


urlpatterns = [
    path("", views.procedure_types_list, name="procedure_types_list"),
    path("<slug:slug>/", views.procedures_by_type, name="procedures_by_type"),
]
