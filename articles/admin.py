from django.contrib import admin
from .models import Article
from markdownx.admin import MarkdownxModelAdmin



admin.site.register(Article, MarkdownxModelAdmin)
