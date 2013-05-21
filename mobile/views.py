# Create your views here.
from datetime import datetime

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.db import IntegrityError
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from core.models import UserProfile

from events.models import Event
from events.helpers import group_events_by_date

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
    if request.user.is_anonymous():
        events = Event.published_events()
    else:
        events = Event.published_events(user_profile=request.user.get_profile())

    events = events.filter(date__gt=datetime.today()).order_by('date')[:20]

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
        speakers = UserProfile.objects.filter(Q(published=True))[:20]
    else:
        speakers = UserProfile.objects.filter(Q(published=True) | Q(user=request.user))[:20]

    return render_to_response('mobile/speakers.html', {
        'speakers': speakers
        }, context_instance=RequestContext(request))

def profile(request):
    return render_to_response('mobile/profile.html',
            context_instance=RequestContext(request))
