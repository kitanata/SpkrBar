# Create your views here.
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from django.views.generic import ListView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from datetime import datetime
import random
from .models import Talk, Location

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

    location_addresses = ["101 5th Ave", "221B Baker Street", "345 E First Street",
            "404 Found Boulevard", "1020 Rodero Drive", "4598 Morse Road", 
            "1108 City Park Ave", "1125 Kinnear Ave", "50 N Warren Ave",
            "200 S Hague Drive", "18559 ZipCode Lane"]

    location_cities = ["Columbus", "South Bend", "Indianapolis", "Chicago", 
            "Los Angeles", "New Bork", "London", "QueensBurg", "Meow City",
            "Volcano", "Deer Park", "La Grange", "Misty Road"]

    location_states = ["Ohio", "Indiana", "New Bork", "Florida", "California",
            "Nebraska", "Washington DC", "Alaska", "Mississippi", "Hawaii",
            "Thailand", "China", "Russia"]

    speaker = User.objects.get(username='raymond')

    for i in range(0, 200):

        if i % 10 == 0:
            location = Location()
            location.name = random.choice(location_names)
            location.address = random.choice(location_addresses)
            location.city = random.choice(location_cities)
            location.state = random.choice(location_states)
            location.save()

        talk = Talk()

        talk.name = random.choice(verbs) + " " + random.choice(things) + ": " + random.choice(long_actions)
        talk.description = "A short description of this talk should go here"
        talk.date = datetime.now()
        talk.location = location
        talk.speaker = speaker
        
        talk.save()

    return render_to_response('load_fixtures.html', 
            context_instance=RequestContext(request))

class TalkList(ListView):
    model = Talk
    template_name = "talk_list.html"


def profile(request):
    talks = Talk.objects.filter(speaker=request.user)[:5]

    return render_to_response('profile.html', {'talks': talks},
            context_instance=RequestContext(request))


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
                return redirect('/profile/')
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
    return render_to_response('register.html',
            context_instance=RequestContext(request))
