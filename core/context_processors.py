from .models import ContactInfo


def global_contact_info(request):
    contact = ContactInfo.objects.first()
    return {"contact_info": contact}
