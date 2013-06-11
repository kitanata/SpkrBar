# Create your views here.
from django.shortcuts import get_object_or_404

from .models import BlogPost
from core.helpers import render_to

def blog_list(request):
    posts = BlogPost.objects.filter(published=True).order_by('date')

    history = [{
        'month': item.date.strftime("%B"),
        'year': item.date.strftime("%Y"),
        'post': item } for item in posts]

    context = {
        'recent_posts': posts[:5],
        'history': history,
        }

    return render_to(request, "blog_list.haml", context=context)


def blog_details(request, post_id):
    post = get_object_or_404(BlogPost, published=True, pk=post_id)

    posts = BlogPost.objects.filter(published=True).order_by('date')

    history = [{
        'month': item.date.strftime("%B"),
        'year': item.date.strftime("%Y"),
        'post': item } for item in posts]

    context = {
        'post': post,
        'history': history,
        }

    return render_to(request, "blog_details.haml", context=context)
