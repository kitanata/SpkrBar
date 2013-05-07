# Create your views here.
from datetime import datetime
from itertools import groupby
import random

from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from django.db import IntegrityError
from django.db.models import Q

from .models import Location, UserProfile, UserLink, UserTag
from talks.models import Talk
from .forms import EditProfileForm, ProfilePhotoForm, ProfileLinkForm, ProfileTagForm

random.seed(datetime.now())

def load_fixtures(request):
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

    for i in range(0, 200):

        #Every 10 make a new location and user/speaker
        if i % 10 == 0:
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

        talk = Talk()

        year = random.choice([2013, 2014, 2015])
        month = random.choice(range(1, 13))
        day = random.choice(range(1,28))
        hour = random.choice(range(0,24))
        minute = random.choice([0, 15, 30, 45])

        talk.name = random.choice(verbs) + " " + random.choice(things) + ": " + random.choice(long_actions)
        talk.abstract = talk_description
        talk.date = datetime(year, month, day, hour, minute)
        talk.location = location
        talk.photo = str(random.choice(range(1, 21))) + ".jpeg"

        if i % 3 == 0:
            talk.published = False
        
        talk.save()
        talk.speakers.add(speaker)

    return render_to_response('load_fixtures.html', 
            context_instance=RequestContext(request))


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

                with open('core/static/img/photo/' + photo.name, 'wb+') as destination:
                    for chunk in photo.chunks():
                        destination.write(chunk)

                profile.photo = photo.name

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

    return render_to_response('profile_edit.html', {
        'speaker': request.user.get_profile(),
        'profile_form': profile_form,
        'photo_form': photo_form,
        'tag_form': tag_form,
        'link_form': link_form},
        context_instance=RequestContext(request))


def speakers(request):
    if request.user.is_anonymous():
        speakers = UserProfile.objects.filter(Q(published=True))[:20]
    else:
        speakers = UserProfile.objects.filter(Q(published=True) | Q(user=request.user))[:20]

    return render_to_response('speaker_list.html', {
        'speakers': speakers
        }, context_instance=RequestContext(request))


def speaker_detail(request, username):
    speaker = get_object_or_404(User, username=username).get_profile()

    if not request.user.is_anonymous():
        talks = Talk.objects.filter(Q(published=True, speakers__published=True
            ) | Q(speakers__in=[request.user.get_profile()]))
    else:
        talks = Talk.objects

    talks = talks.filter(speakers__in=[speaker])

    upcoming = talks.filter(date__gt=datetime.now()).order_by('date')[:5]
    upcoming = talks_from_queryset(upcoming)

    past = talks.filter(date__lt=datetime.now()).order_by('-date')[:20]
    past = talks_from_queryset(past, reverse=True)

    if request.user.is_anonymous():
        following = speaker.following.filter(published=True)
        followers = speaker.followers.filter(published=True)
        attending = speaker.talks_attending.filter(date__gt=datetime.now()).order_by('date')

        attended = speaker.talks_attending.filter(date__lt=datetime.now()).order_by('-date')
        attended = talks_from_queryset(attended, reverse=True)
    else:
        following = speaker.following.filter(Q(published=True) | Q(user=request.user))
        followers = speaker.followers.filter(Q(published=True) | Q(user=request.user))
        attending = speaker.talks_attending.filter(
                Q(published=True) | Q(speakers__in=[request.user.get_profile()]),
                Q(speakers__published=True),
                date__gt=datetime.now()).order_by('date')

        attended = speaker.talks_attending.filter(
                Q(published=True) | Q(speakers__in=[request.user.get_profile()]),
                Q(speakers__published=True),
                date__lt=datetime.now()).order_by('-date')
        attended = talks_from_queryset(attended, reverse=True)

    return render_to_response('speaker_profile.html', {
        'speaker': speaker,
        'upcoming': upcoming,
        'past': past,
        'attending': attending,
        'attended': attended,
        'following': following,
        'followers': followers,
        'last': '/speaker/' + username
        }, context_instance=RequestContext(request))


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


def talks_from_queryset(queryset, reverse=False):
    queryset = [{
        'month_num': k,
        'date': datetime(month=k[0], year=k[1], day=1).strftime("%B %Y"),
        'talks': list(g)} for k, g in groupby(queryset, key=lambda x: (x.date.month, x.date.year))]
    queryset.sort(key=lambda x: x['month_num'], reverse=reverse)
    return queryset

    
def login_user(request):

    if request.method == "GET":
        return render_to_response('login.html', 
                context_instance=RequestContext(request))
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/speaker/' + request.user.username)
            else:
                error = "This account has been disabled."
        else:
            error = "Username or password is incorrect."

        return render_to_response('login.html', {'error': error},
                context_instance=RequestContext(request))

        
def logout_user(request):
    logout(request)
    return redirect('/')


def register_user(request):

    if request.method == "GET":
        return render_to_response('register.html',
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
            return redirect('/speaker/' + request.user.username)

        return render_to_response('register.html', {'error': error},
                context_instance=RequestContext(request))

        
