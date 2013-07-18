from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.forms.util import ErrorList
from django.template import loader, Context
from django.db import IntegrityError
from django.core.mail import send_mail

from core.helpers import template
from core.forms import EventRegisterForm
from core.models import SpkrbarUser, SpeakerProfile, EventProfile

email_template = loader.get_template('mail/register_event.html')

@template('auth/register_event.haml')
def register_event(request):
    if request.method == "POST":
        form = EventRegisterForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            username = form.cleaned_data['username'].lower()
            password = form.cleaned_data['password']
            confirm = form.cleaned_data['confirm']
            email = form.cleaned_data['email']

            if password != confirm:
                errors = form._errors.setdefault("password", ErrorList())
                errors.append("Password does not match confirmation.")

                return {'form': form}

            try:
                user = SpkrbarUser.objects.create_user(username, email, password)
                user.user_type = SpkrbarUser.USER_TYPE_EVENT
                user.save()
            except IntegrityError as e:
                errors = form._errors.setdefault("password", ErrorList())
                errors.append("That username is taken. Try another.")

                return {'form': form}

            profile = EventProfile()
            profile.user = user
            profile.name = name
            profile.description = description
            profile.save()

            mes = email_template.render(Context())
            send_mail("Welcome to SpkrBar", mes, "no-reply@spkrbar.com",
                    [user.email], fail_silently=False)

            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect(request.user.get_profile().get_absolute_url())

    form = EventRegisterForm()
    return {'form': form}
