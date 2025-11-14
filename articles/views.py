from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q


from .models import Article, Tag


def articles_list(request):
    query = request.GET.get("q", "")
    tag_slug = request.GET.get("tag")
    articles = Article.objects.all().order_by("-created_at")

    active_tag = None
    if tag_slug:
        active_tag = get_object_or_404(Tag, slug=tag_slug)
        articles = articles.filter(tags=active_tag)
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
            "page_obj": articles_page,
            "all_tags": Tag.objects.all(),
            "active_tag": active_tag,
            "query": query,
            "page_title": "Статті",
        },
    )
