from string import Template as StringTemplate
from email.utils import parseaddr
from django.shortcuts import redirect
from django.template import loader, Context

from core.helpers import template, send_mass_html_mail
from config.settings import DEFAULT_FROM_EMAIL

email_template = loader.get_template('mail/invite.html')

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
            
            <p>It's absolutely free!</p>

            <a class="btn" href="http://www.spkrbar.com/register">Signup Here</a>

            <p>I hope to see you on there soon.</p>

            <blockquote>$username</blockquote>""")

        messages = []
        for contact in contacts:
            email = contact[1]
            try:
                SpkrbarUser.objects.get(email=email)
            except:
                if contact[0]:
                    mes = whole_message.substitute(
                            name=contact[0], message=message,
                            username=request.user.get_full_name())
                else:
                    mes = whole_message.substitute(
                            name="Friend", message=message,
                            username=request.user.get_full_name())

                c = Context({"message": mes})

                messages.append(("You've been invited to Spkrbar.com!",
                    mes, email_template.render(c), request.user.email, [email]))

        send_mass_html_mail(messages, fail_silently=False)
        return redirect('/profile/invite/thanks')
    else:
        template_string =  "I just joined spkrbar.com. Spkrbar is a cool new "\
            "website for people who speaker at conferences. SpkrBar give speakers "\
            "to upload all the information about their talks in one place, get "\
            "feedback and ratings on speaking engagements and promote themselves "\
            "online. SpkrBar helps speakers understand themselves and get better "\
            "at speaking"

        invite_template = StringTemplate(template_string)

        message = invite_template.substitute(
                other_part=speaker_message,
                user_name=request.user.get_full_name())

        return { 'invite_message': message }
