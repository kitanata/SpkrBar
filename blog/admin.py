from django.contrib import admin
from django_markdown.admin import MarkdownModelAdmin
from .models import BlogPost

admin.site.register(BlogPost, MarkdownModelAdmin)
