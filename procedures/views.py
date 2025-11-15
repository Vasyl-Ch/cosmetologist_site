from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import HttpRequest, HttpResponse


from .models import ProcedureType, Procedure


def procedure_types_list(request: HttpRequest) -> HttpResponse:
    query = request.GET.get("q", "")
    types = ProcedureType.objects.all().order_by("name")
    if query:
        types = types.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    return render(
        request,
        "procedures/types_list.html",
        {
            "procedure_types": types,
            "query": query,
            "page_title": "Перелік процедур",
        },
    )


def procedures_by_type(request: HttpRequest, slug: str) -> HttpResponse:
    type_obj = get_object_or_404(ProcedureType, slug=slug)
    query = request.GET.get("q", "")
    procedures = type_obj.procedures.all().order_by("-created_at")
    if query:
        procedures = procedures.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    paginator = Paginator(procedures, 6)
    page = request.GET.get("page")
    procedures_page = paginator.get_page(page)

    return render(
        request,
        "procedures/procedures_list.html",
        {
            "procedure_type": type_obj,
            "page_obj": procedures_page,
            "query": query,
            "all_procedure_types": ProcedureType.objects.all().order_by(
                "name"
            ),
            "current_type_slug": type_obj.slug,
            "page_title": type_obj.name,
        },
    )
