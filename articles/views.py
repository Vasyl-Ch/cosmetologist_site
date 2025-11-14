from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q


from .models import Article, Tag


def articles_list(request):
    query = request.GET.get("q", "")
    tag_slug = request.GET.get("tag")
    articles = Article.objects.all().order_by("-created_at")

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        articles = articles.filter(tags=tag)
    if query:
        articles = articles.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    paginator = Paginator(articles, 6)
    page = request.GET.get("page")
    articles_page = paginator.get_page(page)

    return render(
        request,
        "articles/articles_list.html",
        {
            "articles": articles_page,
            "tags": Tag.objects.all(),
            "selected_tag": tag_slug,
            "query": query,
            "page_title": "Статьи",
        },
    )
