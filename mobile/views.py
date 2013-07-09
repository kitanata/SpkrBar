# Create your views here.
from datetime import datetime
from itertools import groupby

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.db import IntegrityError
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from core.models import SpeakerProfile

from events.models import Event

def group_events_by_date(talks, reverse=False):
    talks = [{
        'month_num': k,
        'date': datetime(month=k[1], year=k[0], day=1).strftime("%B %Y"),
        'events': list(g)} 
        for k, g in groupby(talks, key=lambda x: (x.start_date.year, x.start_date.month))]

    talks.sort(key=lambda x: x['month_num'], reverse=reverse)
    return talks

def login_user(request):
    if request.method == "GET":
        return render_to_response('mobile/login.html', 
                context_instance=RequestContext(request))
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/mobile')
            else:
                error = "This account has been disabled."
        else:
            error = "Username or password is incorrect."

        return render_to_response('mobile/login.html', {'error': error},
                context_instance=RequestContext(request))


def logout_user(request):
    logout(request)
    return redirect('/mobile')


def register_user(request):
    if request.method == "GET":
        return render_to_response('mobile/register.html',
                context_instance=RequestContext(request))
    else:
        username = request.POST['username']
        password = request.POST['password']
        confirm = request.POST['confirm']
        email = request.POST['email']

        error = None

        if password != confirm:
            error = "Password does not match confirmation."

        if not error:
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
            except IntegrityError as e:
                error = "That username is taken. Try another."

        if not error:
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/mobile/profile')

        return render_to_response('mobile/register.html', {
            'error': error
            }, context_instance=RequestContext(request))


def index(request):
    events = Event.objects.all()

    events = events.filter(start_date__gte=datetime.today()).order_by('start_date')[:20]

    event_groups = group_events_by_date(events)

    return render_to_response('mobile/index.html', {
        'event_groups': event_groups
        }, context_instance=RequestContext(request))



def event_detail(request):
    return render_to_response('mobile/event-detail.html',
            context_instance=RequestContext(request))

def search(request):
    return render_to_response('mobile/search.html',
            context_instance=RequestContext(request))

def speakers(request):
    if request.user.is_anonymous():
        speakers = SpeakerProfile.objects.filter(Q(published=True))[:20]
    else:
        speakers = SpeakerProfile.objects.filter(Q(published=True) | Q(user=request.user))[:20]

    return render_to_response('mobile/speakers.html', {
        'speakers': speakers
        }, context_instance=RequestContext(request))

def profile(request):
    return render_to_response('mobile/profile.html',
            context_instance=RequestContext(request))
