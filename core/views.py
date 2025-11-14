from django.shortcuts import render


from .models import Review, Certificate, ContactInfo
from procedures.models import ProcedureType
from cosmetics.models import Brand
from articles.models import Article


def home(request):
    reviews = Review.objects.all()[:6]
    certificates = Certificate.objects.all()
    contact = ContactInfo.objects.first()

    context = {
        "reviews": reviews,
        "certificates": certificates,
        "contact_info": contact,
        "procedure_types": ProcedureType.objects.all()[:3],
        "brands": Brand.objects.all()[:3],
        "recent_articles": Article.objects.all()[:3],
        "page_title": "Головна",
    }
    return render(request, "core/home.html", context)


def contacts(request):
    contact = ContactInfo.objects.first()
    return render(
        request,
        "core/contacts.html",
        {
            "contact_info": contact,
            "page_title": "Контакти",
        },
    )
