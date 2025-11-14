from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q


from .models import Brand, Product


def brands_list(request):
    query = request.GET.get("q", "")
    brands = Brand.objects.all()
    if query:
        brands = brands.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    return render(
        request,
        "cosmetics/brands_list.html",
        {
            "brands": brands,
            "query": query,
            "all_brands": Brand.objects.all(),
            "page_title": "Косметика",
        },
    )


def products_by_brand(request, slug):
    brand = get_object_or_404(Brand, slug=slug)
    query = request.GET.get("q", "")
    products = brand.products.all()
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
            "products": products_page,
            "query": query,
            "all_brands": Brand.objects.all(),
            "page_title": brand.name,
        },
    )
