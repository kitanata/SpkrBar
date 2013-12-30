from django.shortcuts import redirect
from django.contrib.auth.models import User, Permission
from django.contrib.auth import authenticate, login
from django.forms.util import ErrorList
from django.template import loader, Context
from django.db import IntegrityError

from core.helpers import template, send_html_mail
from core.forms import SpeakerRegisterForm
from core.models import SpkrbarUser

email_template = loader.get_template('mail/register.html')

@template('auth/register_user.haml')
def register_user(request):
    if request.method == "POST":
        form = SpeakerRegisterForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email'].lower()
            full_name = form.cleaned_data['full_name']

            password = form.cleaned_data['password']
            confirm = form.cleaned_data['confirm']

            if password != confirm:
                errors = form._errors.setdefault("password", ErrorList())
                errors.append("Password does not match confirmation.")

                return {'form': form}

            try:
                user = SpkrbarUser.objects.create_user(email, password)
                user.save()
            except IntegrityError as e:
                print e
                errors = form._errors.setdefault("password", ErrorList())
                errors.append("That email is already being used. Try another.")

                return {'form': form}

            user.full_name = full_name

            if 'about_me' in form.cleaned_data:
                user.about_me = form.cleaned_data['about_me']

            user.user_permissions.add(
                Permission.objects.get(codename='add_talk'),
                Permission.objects.get(codename='change_talk'),
                Permission.objects.get(codename='delete_talk'),

                Permission.objects.get(codename='add_talkcomment'),
                Permission.objects.get(codename='change_talkcomment'),
                Permission.objects.get(codename='delete_talkcomment'),

                Permission.objects.get(codename='add_engagement'),
                Permission.objects.get(codename='change_engagement'),
                Permission.objects.get(codename='delete_engagement'),

                Permission.objects.get(codename='add_usertag'),
                Permission.objects.get(codename='add_talktag'),
                Permission.objects.get(codename='add_location'),

                Permission.objects.get(codename='add_userlink'),
                Permission.objects.get(codename='change_userlink'),
                Permission.objects.get(codename='delete_userlink'),

                Permission.objects.get(codename='add_talklink'),
                Permission.objects.get(codename='change_talklink'),
                Permission.objects.get(codename='delete_talklink'),

                Permission.objects.get(codename='add_talkslidedeck'),
                Permission.objects.get(codename='change_talkslidedeck'),
                Permission.objects.get(codename='delete_talkslidedeck'),

                Permission.objects.get(codename='add_talkvideo'),
                Permission.objects.get(codename='change_talkvideo'),
                Permission.objects.get(codename='delete_talkvideo'),

                Permission.objects.get(codename='add_talkendorsement'),
                Permission.objects.get(codename='delete_talkendorsement'),

                Permission.objects.get(codename='add_userfollowing'),
                Permission.objects.get(codename='delete_userfollowing'),

                Permission.objects.get(codename='change_spkrbaruser'),
            )

            user.save()

            text = """
                Hi there! 
                
                I'm SpkrBot. I want to thank you for joining SpkrBar as a speaker. Did you know that with SpkrBar you can:

                <ul>
                    <li>Host all the information about your talks in one place</li>
                    <li>Find events you'd like to speak at and submit proposals to them</li>
                    <li>Get great feedback on your talks by the people who attend them</li>
                    <li>Find other talks like yours and learn from them</li>
                </ul>

                Oh, and before I forget, we are working on making the site better every day, so if you encounter any problems, have questions, or want to give us any feedback please send me an email and I'll automatically send it on to our developers. We read every email we get.

                Thanks again,
                SpkrBot @ Spkrbar.com
                """

            mes = email_template.render(Context({'message': text}))
            send_html_mail("Welcome to SpkrBar", text, mes, [user.email])

            user = authenticate(email=email, password=password)
            login(request, user)

            return redirect(request.user.get_absolute_url())
    else:
        form = SpeakerRegisterForm()

    return {'form': form}
