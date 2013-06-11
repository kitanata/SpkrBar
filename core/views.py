# Create your views here.
from datetime import datetime, timedelta
from itertools import groupby
from collections import namedtuple
import random

from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden

from django.db import IntegrityError
from django.db.models import Q

from guardian.shortcuts import assign

from .helpers import save_photo_with_uuid, render_to

from .models import Location, UserProfile, UserLink, UserTag, TalkEvent
from talks.models import Talk

from events.models import Event
from events.helpers import group_events_by_date

from blog.models import BlogPost

from .forms import EditProfileForm, ProfilePhotoForm, ProfileLinkForm, ProfileTagForm

from security import speaker_restricted

random.seed(datetime.now())

def generate_datetime():
    year = random.choice([2013, 2014, 2015])
    month = random.choice(range(1, 13))
    day = random.choice(range(1,28))
    hour = random.choice(range(0,24))
    minute = random.choice([0, 15, 30, 45])
    return datetime(year, month, day, hour, minute)

def load_fixtures(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    verbs = ['Hacking', 'Saving', 'Hunting', 'Exploiting', 
            'Looking Past', 'Lessons Learned from', 'Staring Down']
    things = ['Robots', 'Money', 'Communication', 'The Hiring Process', 
            'The Homeless', 'Bad Bosses', 'Startups', 'Social Policies',
            'Smart Grids', 'Local Government', 'The Court System',
            'Board Games', 'The MAFIAA', 'Hackers']
    long_actions = [
            "What's Next?",
            "or... How divination is for suckers...",
            "A small bag of tricks.",
            "After the digital age.",
            "What I learned on Cherry Blossom Ave.",
            "Cities of the future.",
            "Perpetual machines CAN work. I swear!",
            "or... What I learned from Battlestar Galactica",
            "Why you suck.",
            "Why you don't suck.",
            "The sky is falling, or so they say."]

    location_names = ["Tech Columbus", "Linux User Group", "Java User Group",
            "Anime Kids United", "Soccer Club", "Bar 451", "Chains on 10th",
            "15 Smiling Kids", "Central Community Center", "InTech Central Office",
            "Baboon Fun Park", "The Wilde Syde: Animal Safari", "Anonymous",
            "The Clap Trap", "Game Design Group", "Board Gamers R' US"]

    event_names = ["Rubycon", "PyOhio", "PyCon", "GenCon", "CodeMash", "BingCon", 
            "MarCon", "MegaCon", "CloudDevelop", "Origins Game Fair", "Essen",
            "Columbus Code Camp", "Girl Develop It", "Iron Ruby", "Emerald Fair"]

    location_addrs = [
            ("1275 Kinnear Road", "Columbus", "Ohio", "43204"),
            ("7003 Post Road", "Dublin", "Ohio", "43016"),
            ("200 Georgesville Road", "Columbus", "Ohio", "43228"),
            ("1100 Rock and Roll Boulevard", "Cleveland", "Ohio", "44114"),
            ("1268 Missouri Street", "San Francisco", "California", "94107"),
            ("326 N Main Street", "Crestview", "Florida", "32536"),
            ("3900 Chagrin Drive", "Columbus", "Ohio", "43219"),
            ("1400 E Angela Blvd", "South Bend", "Indiana", "46617")]

    user_first_names = ['Kenneth', 'Bill', 'John', 'Mike', 'Susan', 'Junell',
            'Dharma', 'Shaniquha', 'Damien', 'Dominic', 'Tyler', 'Edward',
            'Jameson', 'Jim', 'Ron', 'Dharani', 'Priya', 'Venkat']

    user_last_names = ["O'Neil", 'Brown', 'Smith', 'Jackson', 'Ramachandra',
            'Rajeshwer', 'Howard', 'Wooten', 'Berry', 'Frauenfelder',
            'Bender', 'Fry', 'Hogue']

    user_description = "Zombie ipsum reversus ab viral inferno, nam rick grimes malum cerebro. De carne lumbering animata corpora quaeritis. Summus brains sit morbo vel maleficia? De apocalypsi gorger omero undead survivor dictum mauris. Hi mindless mortuis soulless creaturas, imo evil stalking monstra adventus resi dentevil vultus comedat cerebella viventium. Qui animated corpse, cricket bat max brucks terribilem incessu zomby. The voodoo sacerdos flesh eater, suscitat mortuos comedere carnem virus."
    talk_description = user_description

    user = User.objects.get(username='raymond')
    user.first_name = "Raymond"
    user.last_name = "Chandler III"
    user.email = "raymondchandleriii@gmail.com"
    user.save()

    speaker = user.get_profile()
    speaker.about_me = "I'm a little teapot, short and stout!"
    speaker.save()

    anon_profile = UserProfile.objects.get(user__username="AnonymousUser")
    anon_profile.published = False
    anon_profile.save()

    for i in range(0, 200):
        #every 20 make a new blog POST
        if i % 19 == 0 or i == 0:
            post = BlogPost()
            post.name = random.choice(long_actions)
            post.content = user_description
            post.date = generate_datetime()
            post.save()

        #Every 10 make a new location and user/speaker
        if i % 11 == 0 or i == 0:
            location = Location()
            location.name = random.choice(location_names)
            addr = random.choice(location_addrs)
            location.address = addr[0]
            location.city = addr[1]
            location.state = addr[2]
            location.zip_code = addr[3]
            location.save()

            first_name = random.choice(user_first_names)
            last_name = random.choice(user_last_names)
            un = "test" + str(i / 10)
            new_user = User.objects.create_user(un, 'test@spkrbar.com', 'abcd1234')
            new_user.first_name = first_name
            new_user.last_name = last_name
            new_user.save()

            speaker = new_user.get_profile()
            speaker.about_me = user_description
            speaker.save()

        if i % 17 == 0 or i == 0:
            event = Event()
            event.name = random.choice(event_names)
            event.description = user_description
            event.owner = speaker
            event.location = location
            event.published = True
            event.accept_submissions = (i % 2 == 0)

            event.start_date = generate_datetime()
            event.end_date = event.start_date + timedelta(days=3)
            event.save()

        talk = Talk()
        talk.name = random.choice(verbs) + " " + random.choice(things) + ": " + random.choice(long_actions)
        talk.abstract = talk_description

        if i % 7 == 0:
            talk.published = False
       
        talk.speaker = speaker
        talk.save()

        talk_event = TalkEvent()
        talk_event.talk = talk
        talk_event.event = event
        delta = timedelta(days=random.choice([1,2]), hours=random.choice(range(1, 10)))
        talk_event.date = event.start_date + delta
        talk_event.save()

        assign('change_talk', speaker.user, talk)
        assign('delete_talk', speaker.user, talk)

    return render_to(request, 'load_fixtures.haml')


def index(request):
    talk_events = TalkEvent.objects.filter(
            event__published=True, event__owner__published=True,
            talk__published=True, talk__speaker__published=True)

    start_date = datetime.today() - timedelta(days=1)
    upcoming = talk_events.filter(event__start_date__gt=start_date
            ).order_by('date')[:20]

    if len(upcoming) > 4:
        upcoming = random.sample(upcoming, 4)

    context = {'upcoming': upcoming }

    return render_to(request, "index.haml", context=context)


def talk_list(request):
    group_defs = [ 
            ('-', 14, "In the past couple weeks"), 
            ('+', 7, "Upcoming this week"), 
            ('+', 30, "In the next 30 days"),
            ('+', 90, "In the next 3 months"), 
            ('+', 90, "In the next 6 months"), 
            ('+', 180, "In the next year") ]

    talk_events = TalkEvent.objects.filter(
            event__published=True, event__owner__published=True,
            talk__published=True, talk__speaker__published=True)

    groups = []
    end_date = datetime.today()
    for group in group_defs:
        if group[0] == '-':
            start_date = datetime.today() - timedelta(days=group[1])
            end_date = datetime.today()
        else:
            start_date = end_date
            end_date = start_date + timedelta(days=group[1])

        result = talk_events.filter(event__start_date__gt=start_date,
                event__start_date__lt=end_date)

        if len(result) > 9:
            result = random.sample(result, 8)

        result = list(result)
        result.sort(key=lambda x: x.date)

        groups.append((group[2], result))

    context = {'talk_groups': groups }

    return render_to(request, "talk_list.haml", context=context)


@login_required()
def talk_event_attendee_new(request, talk_event_id):
    talk_event = get_object_or_404(TalkEvent, pk=talk_event_id)

    if request.user.get_profile() in talk_event.attendees.all():
        talk_event.attendees.remove(request.user.get_profile())
        talk_event.save()
    else:
        talk_event.attendees.add(request.user.get_profile())
        talk_event.save()

    if request.GET['last']:
        return redirect(request.GET['last'])
    else:
        return redirect(request.user.get_profile())

@login_required()
def profile_edit(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST)

        if form.is_valid():
            user = request.user

            names = form.cleaned_data['name'].split(' ')
            first_name = names[0]
            last_name = ' '.join(names[1:])

            user.first_name = first_name
            user.last_name = last_name
            user.save()

            profile = user.get_profile()
            profile.about_me = form.cleaned_data['about_me']
            profile.save()

            return redirect('/profile/edit/')

    else:
        return profile_form_view(request)


@login_required()
def profile_publish(request):
    profile = request.user.get_profile()
    profile.published=True
    profile.save()

    return redirect('/speaker/' + request.user.username)


@login_required()
def profile_archive(request):
    profile = request.user.get_profile()
    profile.published=False
    profile.save()

    return redirect('/speaker/' + request.user.username)


@login_required()
def profile_edit_photo(request):
    if request.method == "POST":
        form = ProfilePhotoForm(request.FILES)

        if form.is_valid():
            profile = request.user.get_profile()

            if 'photo' in request.FILES:
                photo = request.FILES['photo']
                profile.photo = save_photo_with_uuid(photo)

            profile.save()

            return redirect('/profile/edit/')
    return profile_form_view(request)



@login_required
def profile_link_new(request):
    if request.method == "POST":
        form = ProfileLinkForm(request.POST)

        if form.is_valid():
            profile = request.user.get_profile()

            link_model = UserLink()

            link_model.type_name = form.cleaned_data['type']
            link_model.url_target = form.cleaned_data['url']
            link_model.profile = profile

            link_model.save()

            return redirect('/profile/edit/')
    return profile_form_view(request)



@login_required
def profile_tag_new(request):
    if request.method == "POST":
        form = ProfileTagForm(request.POST)

        if form.is_valid():
            profile = request.user.get_profile()

            tag_name = form.cleaned_data['name']

            try:
                tag_model = UserTag.objects.get(name=tag_name)
            except ObjectDoesNotExist as e:
                tag_model = UserTag(name=tag_name)
                tag_model.save()

            profile.tags.add(tag_model)
            profile.save()

            return redirect('/profile/edit/')
    return profile_form_view(request)



@login_required
def profile_form_view(request):
    profile = request.user.get_profile()
    profile_form = EditProfileForm({
        'name':request.user.get_full_name(),
        'about_me':profile.about_me
    })
    photo_form = ProfilePhotoForm()
    link_form = ProfileLinkForm()
    tag_form = ProfileTagForm()

    context = {
        'speaker': request.user.get_profile(),
        'profile_form': profile_form,
        'photo_form': photo_form,
        'tag_form': tag_form,
        'link_form': link_form
        }

    return render_to(request, 'profile_edit.haml', context=context)


@login_required
def speaker_follow(request, username):
    speaker = get_object_or_404(User, username=username).get_profile()
    user_profile = request.user.get_profile()

    speaker.followers.add(user_profile)
    speaker.save()

    user_profile.following.add(speaker)
    user_profile.save()

    if request.GET['last']:
        return redirect(request.GET['last'])
    else:
        return redirect('/')


def login_user(request):
    if request.method == "GET":
        return render_to(request, 'login.haml')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(request.user.get_profile())
            else:
                error = "This account has been disabled."
        else:
            error = "Username or password is incorrect."

        return render_to(request, 'login.haml', context={'error': error})

        
def logout_user(request):
    logout(request)
    return redirect('/')


def register_user(request):
    if request.method == "GET":
        return render_to(request, 'register.haml')
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
            return redirect('/speaker/' + request.user.username)

        return render_to(request, 'register.haml', context={'error': error})

        
def speakers(request):
    if request.user.is_anonymous():
        speakers = UserProfile.objects.filter(Q(published=True))[:20]
    else:
        speakers = UserProfile.objects.filter(Q(published=True) | Q(user=request.user))[:20]

    return render_to(request, 'speaker_list.haml', context={'speakers': speakers })


def speaker_detail(request, username):
    speaker = get_object_or_404(User, username=username).get_profile()

    talks = Talk.objects.filter(speaker=speaker)
    events = Event.objects.filter(owner=speaker)

    if speaker.user != request.user:
        talks = talks.filter(published=True, speaker__published=True)
        events = events.filter(published=True, owner__published=True)

    talk_events = TalkEvent.objects.filter(talk__speaker=speaker,
            event__published=True, talk__published=True,
            event__owner__published=True, talk__speaker__published=True)

    current = talk_events.filter(
            event__start_date__lt=datetime.today(),
            event__end_date__gt=datetime.today())

    upcoming = talk_events.filter(event__start_date__gt=datetime.today())
    past = talk_events.filter(event__end_date__lt=datetime.today())

    if request.user.is_anonymous():
        following = speaker.following.filter(published=True)
        followers = speaker.followers.filter(published=True)
        attending = None
        attended = None
    else:
        following = speaker.following.filter(Q(published=True) | Q(user=request.user))
        followers = speaker.followers.filter(Q(published=True) | Q(user=request.user))

        attendance = speaker.talkevent_set
        attending = attendance.filter(date__gt=datetime.today()).order_by('date')
        attended = attendance.filter(date__lt=datetime.today()).order_by('-date')

    template = 'speaker_profile.haml'

    if request.user == speaker.user:
        template = 'user_profile.haml'

    context = {
        'speaker': speaker,
        'current': current,
        'upcoming': upcoming,
        'past': past,
        'talks': talks,
        'events': events,
        'attending': attending,
        'attended': attended,
        'following': following,
        'followers': followers,
        'last': '/speaker/' + username
        }

    return render_to(request, template, context=context)
