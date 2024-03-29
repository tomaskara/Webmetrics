from django.shortcuts import render, get_object_or_404
from .models import Article


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    return render(request, "articles/article_detail.html", {"article": article})


def article_list(request):
    articles = Article.objects.filter(active=True).order_by("-last_modified")
    return render(request, "articles/articles.html", {"articles": articles})
