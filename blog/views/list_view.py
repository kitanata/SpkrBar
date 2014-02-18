from blog.models import BlogPost
from core.helpers import template

@template('blog/blog_list.haml')
def blog_list(request):
    posts = BlogPost.objects.filter(published=True).order_by('-date')

    history = [{
        'month': item.date.strftime("%B"),
        'year': item.date.strftime("%Y"),
        'post': item,
        'content': item.markup_content() 
        } for item in posts]

    recent = [{'post': p, 'content': p.markup_content()} for p in posts[:5]]

    return {
        'recent_posts': recent,
        'history': history,
        }
