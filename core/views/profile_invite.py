from string import Template as StringTemplate
from email.utils import parseaddr
from django.shortcuts import redirect
from django.core.mail import send_mass_mail

from core.helpers import template

email_template = ""

with open('mail/invite.html') as email_file:
    email_template = StringTemplate(''.join(email_file.readlines()))

@template('auth/invite.haml')
def profile_invite(request):
    if request.method == "POST":
        contacts = request.POST['contacts']
        message = request.POST['message']

        contacts = contacts.split(',')
        contacts = [parseaddr(x) for x in contacts]

        whole_message = StringTemplate(
            """Hi $name,
            <p>$message</p>
            
            <p>It's free for speakers and attendees!</p>

            <a class="btn" href="http://www.spkrbar.com/register">Signup Here</a>

            <p>I hope to see you on there soon.</p>

            <blockquote>$username</blockquote>""")

        request.user.num_invites += len(contacts)
        request.user.save()

        messages = []
        for contact in contacts:
            if contact[0]:
                mes = whole_message.substitute(
                        name=contact[0], message=message,
                        username=request.user.get_full_name())
            else:
                mes = whole_message.substitute(
                        name="Friend", message=message,
                        username=request.user.get_full_name())

            messages.append(("You've been invited to Spkrbar.com!",
                        email_template.substitute(message=mes),
                        'invite@spkrbar.com', [contact[0]]))

        send_mass_mail(messages, fail_silently=False)
        return redirect('/profile/invite/thanks')
    else:
        template_string =  "I just joined spkrbar.com. Spkrbar is a cool new "\
            "website for people who attend, plan, and speak at " \
            "conferences. $other_part"
            
        speaker_message = "Since I'm a speaker I can upload all the information " \
        "about my talks in one place and if you signup as an attendee you can " \
        "rate them and find other talks like mine you'd find interesting or insightful."

        attendee_message = "Since I'm an attendee I can find and rate talks " \
        "that I've attended or liked. Spkrbar has been a great way for me to " \
        "find interesting talks and events. I love it!"

        planner_message = "Since I'm an event planner I've been able to find " \
        "really awesome speakers for my events using Spkrbar. Speakers that " \
        "signup can upload all the information for their talks in one place and " \
        "promote themsleves while those who come see them speak can rate them " \
        "quickly and easily."

        invite_template = StringTemplate(template_string)

        if request.user.is_speaker():
            message = invite_template.substitute(
                    other_part=speaker_message,
                    user_name=request.user.get_full_name())
        elif request.user.is_attendee():
            message = invite_template.substitute(
                    other_part=attendee_message,
                    user_name=request.user.get_full_name())
        elif request.user.is_event_planner():
            message = invite_template.substitute(
                    other_part=planner_message,
                    user_name=request.user.get_full_name())

        return { 'invite_message': message }
