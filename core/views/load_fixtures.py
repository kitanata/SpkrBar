from datetime import datetime, timedelta
import random

from django.contrib.auth.models import User
from django.http import HttpResponseForbidden

from guardian.shortcuts import assign

from core.helpers import generate_datetime, template

from core.models import Location, UserProfile
from events.models import Event
from talkevents.models import TalkEvent
from blog.models import BlogPost

random.seed(datetime.now())

@template('load_fixtures.haml')
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

    return {}
