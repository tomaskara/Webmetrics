from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify


class Article(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, null=False, blank=True)
    perex = models.TextField()
    content = MarkdownxField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    @property
    def formatted_markdown(self):
        return markdownify(self.content)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(Article, self).save(*args, **kwargs)


