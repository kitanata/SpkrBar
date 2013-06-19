import uuid
import os
from functools import wraps

from config.settings import MEDIA_ROOT

from django.shortcuts import render_to_response
from django.template import RequestContext

def save_photo_with_uuid(photo):
    photo_ext = photo.name.split('.')[-1]
    photo_root_name = str(uuid.uuid4()) + '.' + photo_ext
    photo_name = os.path.join('photo', photo_root_name)
    photo_storage = os.path.join(MEDIA_ROOT, 'photo', photo_root_name)

    with open(photo_storage, 'wb+') as destination:
        for chunk in photo.chunks():
            destination.write(chunk)

    return photo_name


def render_to(request, template, js=None, context=None):

    if js and context:
        context['js'] = js
    elif js:
        context = dict(js=js)

    return render_to_response(template, context, 
            context_instance=RequestContext(request))


def template(template_name):
    def view_wrapper(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            context = view_func(request, *args, **kwargs)

            return render_to_response(template_name, context,
                    context_instance=RequestContext(request))
        return wrapper
    return view_wrapper
    

def generate_datetime():
    year = random.choice([2013, 2014, 2015])
    month = random.choice(range(1, 13))
    day = random.choice(range(1,28))
    hour = random.choice(range(0,24))
    minute = random.choice([0, 15, 30, 45])
    return datetime(year, month, day, hour, minute)
