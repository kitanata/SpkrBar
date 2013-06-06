# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext

def blog_list(request):
    return render_to_response("blog_list.haml", {
        }, context_instance=RequestContext(request))

def blog_details(request, post_id):
    return render_to_response("blog_details.haml", {
        }, context_instance=RequestContext(request))
