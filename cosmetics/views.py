from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q


from .models import Brand, Product


def brands_list(request):
    query = request.GET.get("q", "")
    brands = Brand.objects.all().order_by("name")
    if query:
        brands = brands.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    paginator = Paginator(brands, 6)
    page = request.GET.get("page")
    brands_page = paginator.get_page(page)
    return render(
        request,
        "cosmetics/brands_list.html",
        {
            "page_obj": brands_page,
            "query": query,
            "page_title": "Косметика",
        },
    )


def products_by_brand(request, slug):
    brand = get_object_or_404(Brand, slug=slug)
    query = request.GET.get("q", "")
    products = brand.products.all().order_by("-created_at")
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    paginator = Paginator(products, 6)
    page = request.GET.get("page")
    products_page = paginator.get_page(page)

    return render(
        request,
        "cosmetics/products_list.html",
        {
            "brand": brand,
            "page_obj": products_page,
            "query": query,
            "all_brands": Brand.objects.all().order_by("name"),
            "page_title": brand.name,
        },
    )
