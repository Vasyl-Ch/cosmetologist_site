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


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)

    tags = article.tags.all()

    related_articles = (
        Article.objects.filter(tags__in=tags)
        .exclude(id=article.id)
        .distinct()
        .order_by("-created_at")[:3]
    )

    # Fallback only if no related articles at all
    if related_articles.count() == 0:
        other_articles = (
            Article.objects.exclude(id=article.id)
            .order_by("-created_at")[: 3 - related_articles.count()]
        )
        related_articles = list(related_articles) + list(other_articles)

    previous_article = (
        Article.objects.filter(created_at__lt=article.created_at)
        .order_by("-created_at")
        .first()
    )

    next_article = (
        Article.objects.filter(created_at__gt=article.created_at)
        .order_by("-created_at")
        .first()
    )

    context = {
        "article": article,
        "related_articles": related_articles,
        "previous_article": previous_article,
        "next_article": next_article,
    }

    return render(request, "articles/article_detail.html", context)
