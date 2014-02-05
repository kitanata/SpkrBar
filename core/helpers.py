import uuid
import os
from datetime import datetime
from functools import wraps
from itertools import groupby

from config.settings import MEDIA_ROOT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, DEFAULT_FROM_EMAIL

from django.core.mail import get_connection, EmailMultiAlternatives
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

def save_photo_with_uuid(photo):
    return save_data_with_uuid(photo, 'photo')

def save_file_with_uuid(file_item):
    return save_data_with_uuid(file_item, 'files')

def save_data_with_uuid(item, folder_name):
    file_ext = item.name.split('.')[-1]
    file_root_name = str(uuid.uuid4()) + '.' + file_ext
    file_name = os.path.join(folder_name, file_root_name)
    file_storage = os.path.join(MEDIA_ROOT, folder_name, file_root_name)

    with open(file_storage, 'wb+') as destination:
        for chunk in item.chunks():
            destination.write(chunk)

    return file_name

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


def events_from_engagements(queryset):
    engagements = queryset.order_by('event_name')

    events = list()
    for name, engs in groupby(engagements, key=lambda x: x.event_name):
        engs = list(engs)
        earliest_eng = min(map(lambda x: datetime.combine(x.date, x.time), engs))
        latest_eng = max(map(lambda x: datetime.combine(x.date, x.time), engs))
        tags = list(reduce(lambda x, y : x | y, map(lambda z: z.talk.tags.all(), engs)))
        tags = sorted([(tags.count(x), x.name) for x in set(tags)], key=lambda x: -x[0])
        events.append({
            'name': name,
            'numtalks': len(engs),
            'earliest_date': earliest_eng.date().isoformat(),
            'earliest_time': earliest_eng.time().isoformat(),
            'latest_date': latest_eng.date().isoformat(),
            'latest_time': latest_eng.time().isoformat(),
            'tags': tags,
        })

    events.sort(key=lambda x: -x['numtalks'])

    return events
