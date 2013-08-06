from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.forms.util import ErrorList
from django.template import loader, Context
from django.db import IntegrityError

from core.helpers import template, send_html_mail
from core.forms import AttendeeRegisterForm
from core.models import SpkrbarUser, AttendeeProfile, EventProfile

email_template = loader.get_template('mail/register.html')

@template('auth/register_attendee.haml')
def register_attendee(request):
    if request.method == "POST":
        form = AttendeeRegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username'].lower()

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            password = form.cleaned_data['password']
            confirm = form.cleaned_data['confirm']
            email = form.cleaned_data['email']

            if password != confirm:
                errors = form._errors.setdefault("password", ErrorList())
                errors.append("Password does not match confirmation.")

                return {'form': form}

            try:
                user = SpkrbarUser.objects.create_user(username, email, password)
                user.user_type = SpkrbarUser.USER_TYPE_ATTENDEE
                user.save()
            except IntegrityError as e:
                errors = form._errors.setdefault("password", ErrorList())
                errors.append("That username is taken. Try another.")

                return {'form': form}

            profile = AttendeeProfile()
            profile.user = user
            profile.first_name = first_name
            profile.last_name = last_name

            if 'about_me' in form.cleaned_data:
                profile.about_me = form.cleaned_data['about_me']

            profile.save()

            text = """
                Hi there! 
                
                I'm SpkrBot. I want to thank you for joining SpkrBar as a conference attendee. Did you know that with SpkrBar you can:

                <ul>
                    <li>Find and follow your favorite speakers</li>
                    <li>Endorse your favorite talks</li>
                    <li>Rate speakers and talks that you've personally attendes</li>
                    <li>Find all the information about talks in one place</li>
                    <li>Schedule talks that you'd like to attend</li>
                </ul>

                Oh, and before I forget, we are working on making the site better every day, so if you encounter any problems, have questions, or want to give us any feedback please send me an email and I'll automatically send it on to our developers. We read every email we get.

                Thanks again,
                SpkrBot @ Spkrbar.com
                """

            mes = email_template.render(Context({'message': text}))
            send_html_mail("Welcome to SpkrBar", text, mes, [user.email])

            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect(request.user.get_profile().get_absolute_url())
    else:
        form = AttendeeRegisterForm()

    return {'form': form}
