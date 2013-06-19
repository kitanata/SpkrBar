from django.shortcuts import get_object_or_404

from models import BlogPost
from core.helpers import template

@template('blog/blog_details.haml')
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
