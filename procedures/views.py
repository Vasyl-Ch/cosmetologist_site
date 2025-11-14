from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q


from .models import ProcedureType, Procedure


def procedure_types_list(request):
    query = request.GET.get("q", "")
    types = ProcedureType.objects.all()
    if query:
        types = types.filter(Q(name__icontains=query) | Q(description__icontains=query))
    return render(
        request,
        "procedures/types_list.html",
        {
            "types": types,
            "query": query,
            "all_types": ProcedureType.objects.all(),
            "page_title": "Перелік процедур",
        },
    )


def procedures_by_type(request, slug):
    type_obj = get_object_or_404(ProcedureType, slug=slug)
    query = request.GET.get("q", "")
    procedures = type_obj.procedures.all()
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
            "type": type_obj,
            "procedures": procedures_page,
            "query": query,
            "all_types": ProcedureType.objects.all(),
            "page_title": type_obj.name,
        },
    )
