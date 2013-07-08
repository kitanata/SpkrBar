from string import Template as StringTemplate
from django.shortcuts import redirect

from core.helpers import template

@template('auth/invite.haml')
def profile_invite(request):
    if request.method == "POST":
        return redirect('/profile/invite/thanks')
    else:
        template_string = \
        """    I just joined spkrbar.com. Spkrbar is a cool new website for people who attend, plan, and speak at conferences. $other_part
            
            It's free for speakers and attendees!

            You can join me at Spkrbar.com by signing up at http://www.spkrbar.com/register

            I hope to see you on there soon.

            - $user_name
        """

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

        message = """Hi Friend,

        """
        if request.user.is_speaker():
            message += invite_template.substitute(
                    other_part=speaker_message,
                    user_name=request.user.get_full_name())
        elif request.user.is_attendee():
            message += invite_template.substitute(
                    other_part=attendee_message,
                    user_name=request.user.get_full_name())
        elif request.user.is_event_planner():
            message += invite_template.substitute(
                    other_part=planner_message,
                    user_name=request.user.get_full_name())

        return { 'invite_message': message }
