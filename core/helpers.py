import uuid
import os
import random
from datetime import datetime
from functools import wraps

from config.settings import MEDIA_ROOT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, DEFAULT_FROM_EMAIL

from django.core.mail import get_connection, EmailMultiAlternatives
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect

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

            if isinstance(context, HttpResponseRedirect):
                return context

            return render_to_response(template_name, context,
                    context_instance=RequestContext(request))
        return wrapper
    return view_wrapper


def send_mass_html_mail(datatuple, fail_silently=False, user=None, password=None, 
                        connection=None):
    if not connection:
        if user and password:
            connection = connection or get_connection(
                username=user, password=password, fail_silently=fail_silently
            )
        else:
            connection = connection or get_connection(
                username=EMAIL_HOST_USER, password=EMAIL_HOST_PASSWORD, 
                fail_silently=fail_silently
            )

    messages = []
    for subject, text, html, from_email, recipient in datatuple:
        message = EmailMultiAlternatives(subject, text, from_email, recipient)
        message.attach_alternative(html, 'text/html')
        messages.append(message)

    return connection.send_messages(messages)


def send_html_mail(subject, text, html, recipient, from_email=None):
    if not from_email:
        from_email = DEFAULT_FROM_EMAIL

    message = EmailMultiAlternatives(subject, text, from_email, recipient)
    message.attach_alternative(html, 'text/html')
    message.send()
