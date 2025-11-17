from django.http import HttpRequest

from .models import ContactInfo


def global_contact_info(request: HttpRequest) -> dict:
    contact = ContactInfo.objects.first()
    return {"contact_info": contact}
