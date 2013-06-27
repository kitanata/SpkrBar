from blog.models import BlogPost
from core.helpers import template

@template('blog/blog_list.haml')
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
