import random
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden

from guardian.shortcuts import assign_perm

from core.models import SpkrbarUser, UserTag

from locations.models import Location
from events.models import Event
from talks.models import Talk, TalkTag
from blog.models import BlogPost

random.seed(datetime.now())


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

profile_tags = ["Game Design", "Python", "Ruby", "JavaScript", 
        "Entreprenuership", "Education", "Business Strategy", "Marketing",
        "Social Web", "Public Relations", "Human Resources", 
        "Corporate Culture", "Graphic Design", "User Experience", 
        "Interactive Design", "Industrial Design", "C++", ".NET", "C#",
        "Java", "Delphi", "Oracle", "SQL", "MongoDB", "Django", "Rails",
        "Foreign Languages"]

user_description = "Zombie ipsum reversus ab viral inferno, nam rick grimes malum cerebro. De carne lumbering animata corpora quaeritis. Summus brains sit morbo vel maleficia? De apocalypsi gorger omero undead survivor dictum mauris. Hi mindless mortuis soulless creaturas, imo evil stalking monstra adventus resi dentevil vultus comedat cerebella viventium. Qui animated corpse, cricket bat max brucks terribilem incessu zomby. The voodoo sacerdos flesh eater, suscitat mortuos comedere carnem virus."
talk_description = user_description


def generate_datetime():
    year = random.choice([2013, 2014, 2015])
    month = random.choice(range(1, 13))
    day = random.choice(range(1,28))
    hour = random.choice(range(0,24))
    minute = random.choice([0, 15, 30, 45])
    return datetime(year, month, day, hour, minute)


def generate_profile_tags():
    for tag in profile_tags:
        new_tag = UserTag()
        new_tag.name = tag
        new_tag.save()


def generate_talk_tags():
    for tag in profile_tags:
        new_tag = TalkTag()
        new_tag.name = tag
        new_tag.save()


def generate_speaker(username):
    user = SpkrbarUser.objects.create_user(
            username,
            'test@spkrbar.com',
            'abcd1234')

    first_name = random.choice(user_first_names)
    last_name = random.choice(user_last_names)

    user.first_name = first_name
    user.last_name = last_name
    user.about_me = user_description
    user.save()

    build_tags_on_profile(user)

    return user


def build_tags_on_profile(profile):
    for i in range(0, random.choice(range(2,7))):
        tag = UserTag.objects.get(name=random.choice(profile_tags))

        if tag not in profile.tags.all():
            profile.tags.add(tag)

    profile.save()


def generate_talk(speaker):
    talk = Talk()
    talk.name = random.choice(verbs) + " " + random.choice(things) + ": " + random.choice(long_actions)
    talk.abstract = talk_description

    if random.choice(range(0,10)) % 2 == 0:
        talk.published = False

    talk.speaker = speaker
    talk.save()

    for i in range(0, random.choice(range(2,7))):
        tag = TalkTag.objects.get(name=random.choice(profile_tags))

        if tag not in talk.tags.all():
            talk.tags.add(tag)

    assign_perm('change_talk', speaker, talk)
    assign_perm('delete_talk', speaker, talk)

    return talk


def generate_event(location):
    event = Event()
    event.name = random.choice(event_names)
    event.year = random.choice(range(1985, 2014))
    event.location = location
    event.save()

    return event


def generate_admin_user():
    user = SpkrbarUser.objects.create_superuser(
            'raymond',
            'raymondchandleriii@gmail.com',
            'abcd1234')

    user.first_name = "Raymond"
    user.last_name = "Chandler III"
    user.about_me = "I'm a little teapot, short and stout!"
    user.save()

    return user


def generate_blog_post():
    post = BlogPost()
    post.name = random.choice(long_actions)
    post.content = user_description
    post.date = generate_datetime()
    post.published = True
    post.save()


def generate_location():
    location = Location()
    location.name = random.choice(location_names)
    addr = random.choice(location_addrs)
    location.address = addr[0]
    location.city = addr[1]
    location.state = addr[2]
    location.zip_code = addr[3]
    location.save()

    return location


class Command(BaseCommand):
    args = ''
    help = 'Generates the test data for the application.'

    def handle(self, *args, **options):
        speaker = generate_admin_user()

        anon_profile = SpkrbarUser.objects.get(username="AnonymousUser")
        anon_profile.published = False
        anon_profile.save()

        print "Generating Speaker Tags"
        generate_profile_tags()
        generate_talk_tags()

        for i in range(0, 200):
            #every 20 make a new blog POST
            if i % 19 == 0 or i == 0:
                print "Generating Blog Post"
                generate_blog_post()

            #Every 10 make a new location and user/speaker
            if i % 11 == 0 or i == 0:
                un = "speaker" + str(i / 10)
                print "Generating Location"
                location = generate_location()

                print "Generating Speaker " + un
                speaker = generate_speaker(un)

            if i % 17 == 0 or i == 0:
                un = "event" + str(i / 10)
                print "Generating Event " + un
                event = generate_event(location)

            print "Generating Talk"
            talk = generate_talk(speaker)

            #print "Generating Talk Event"
            #talk_event = generate_talk_event(talk, event)

        print "Generating Followers For Users"
        users = SpkrbarUser.objects.all()

        for user in users:
            for i in range(0, random.choice(range(5,17))):
                follower = random.choice(users)

                if follower not in user.followers.all():
                    user.followers.add(follower)

        self.stdout.write('Successfully loaded test data.')
