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

from core.helpers import template
from talkevents.helpers import talk_event_groups
from talkevents.models import TalkEvent

def login_user(request):
    if request.method == "GET":
        return render_to_response('mobile/login.haml', 
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

        return render_to_response('mobile/login.haml', {'error': error},
                context_instance=RequestContext(request))


def logout_user(request):
    logout(request)
    return redirect('/mobile')


def register_user(request):
    if request.method == "GET":
        return render_to_response('mobile/register.haml',
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

        return render_to_response('mobile/register.haml', {
            'error': error
            }, context_instance=RequestContext(request))


@template('mobile/index.haml')
def index(request):
    return {'talk_groups': talk_event_groups()}



def event_detail(request):
    return render_to_response('mobile/event-detail.haml',
            context_instance=RequestContext(request))

def search(request):
    return render_to_response('mobile/search.haml',
            context_instance=RequestContext(request))

@template('mobile/speakers.haml')
def speakers(request):
    speakers = SpeakerProfile.objects.all()
    return {'speakers': speakers}

@template('mobile/profile.haml')
def profile(request):

    profile = request.user.get_profile()

    upcoming = TalkEvent.objects.filter(
            Q(talk__published=True) | 
            Q(talk__speaker__user=request.user),
            Q(date__gte=datetime.today()))

    attending = profile.user.attending.filter(
            date__gte=datetime.today())

    return {'profile': profile,
            'upcoming': upcoming,
            'attending': attending}
