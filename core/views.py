from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


from .models import Review, Certificate, ContactInfo, HomePageSettings
from procedures.models import ProcedureType
from cosmetics.models import Brand
from articles.models import Article


def home(request: HttpRequest) -> HttpResponse:
    reviews = Review.objects.all()[:6]
    certificates = Certificate.objects.all()
    contact = ContactInfo.objects.first()
    home_settings = HomePageSettings.objects.first()

    context = {
        "reviews": reviews,
        "certificates": certificates,
        "contact_info": contact,
        "home_settings": home_settings,
        "procedure_types": ProcedureType.objects.all()[:3],
        "brands": Brand.objects.all()[:3],
        "recent_articles": Article.objects.all()[:3],
        "page_title": "Головна",
    }
    return render(request, "core/home.html", context)


def contacts(request: HttpRequest) -> HttpResponse:
    contact = ContactInfo.objects.first()
    return render(
        request,
        "core/contacts.html",
        {
            "contact_info": contact,
            "page_title": "Контакти",
        },
    )
