# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from .models import BlogPost

def blog_list(request):
    posts = BlogPost.objects.filter(published=True).order_by('date')

    history = [{
        'month': item.date.strftime("%B"),
        'year': item.date.strftime("%Y"),
        'post': item } for item in posts]

    return render_to_response("blog_list.haml", {
        'recent_posts': posts[:5],
        'history': history,
        }, context_instance=RequestContext(request))

def blog_details(request, post_id):
    post = get_object_or_404(BlogPost, published=True, pk=post_id)

    posts = BlogPost.objects.filter(published=True).order_by('date')

    history = [{
        'month': item.date.strftime("%B"),
        'year': item.date.strftime("%Y"),
        'post': item } for item in posts]

    return render_to_response("blog_details.haml", {
        'post': post,
        'history': history,
        }, context_instance=RequestContext(request))
