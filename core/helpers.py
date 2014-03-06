import uuid
import os
from datetime import datetime
from functools import wraps
from itertools import groupby

from config.settings import MEDIA_ROOT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, DEFAULT_FROM_EMAIL

from django.contrib.auth.models import Permission
from django.core.mail import get_connection, EmailMultiAlternatives
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.utils.html_parser import HTMLParser, HTMLParseError
from django.utils.encoding import force_unicode

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


def assign_basic_permissions(user):

    user.user_permissions.add(
        Permission.objects.get(codename='add_talk'),
        Permission.objects.get(codename='change_talk'),
        Permission.objects.get(codename='delete_talk'),

        Permission.objects.get(codename='add_talkcomment'),
        Permission.objects.get(codename='change_talkcomment'),
        Permission.objects.get(codename='delete_talkcomment'),

        Permission.objects.get(codename='add_engagement'),
        Permission.objects.get(codename='change_engagement'),
        Permission.objects.get(codename='delete_engagement'),

        Permission.objects.get(codename='add_usertag'),
        Permission.objects.get(codename='add_talktag'),
        Permission.objects.get(codename='add_location'),

        Permission.objects.get(codename='add_userlink'),
        Permission.objects.get(codename='change_userlink'),
        Permission.objects.get(codename='delete_userlink'),

        Permission.objects.get(codename='add_talklink'),
        Permission.objects.get(codename='change_talklink'),
        Permission.objects.get(codename='delete_talklink'),

        Permission.objects.get(codename='add_talkslidedeck'),
        Permission.objects.get(codename='change_talkslidedeck'),
        Permission.objects.get(codename='delete_talkslidedeck'),

        Permission.objects.get(codename='add_talkvideo'),
        Permission.objects.get(codename='change_talkvideo'),
        Permission.objects.get(codename='delete_talkvideo'),

        Permission.objects.get(codename='add_talkendorsement'),
        Permission.objects.get(codename='delete_talkendorsement'),

        Permission.objects.get(codename='add_userfollowing'),
        Permission.objects.get(codename='delete_userfollowing'),

        Permission.objects.get(codename='change_spkrbaruser'),
        Permission.objects.get(codename='add_feedback'),
    )

class MLStripper(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def handle_entityref(self, name):
        self.fed.append('&%s;' % name)
    def handle_charref(self, name):
        self.fed.append('&#%s;' % name)
    def get_data(self):
        return u''.join([force_unicode(s) for s in self.fed])

def strip_tags(value):
    """Returns the given HTML with all tags stripped."""
    s = MLStripper()
    try:
        s.feed(value)
        s.close()
    except HTMLParseError:
        return value
    else:
        return s.get_data()
        
def rank_engagement(engagement):
    points = 0
    if engagement.speaker.photo:
        points += 250
    points += engagement.speaker.tags.count() * 10
    points += engagement.speaker.links.count() * 25
    points += engagement.talk.tags.count() * 20
    points += engagement.talk.links.count() * 30

    return points
