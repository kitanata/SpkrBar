from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.forms.util import ErrorList

from django.db import IntegrityError

from core.helpers import template
from core.forms import AttendeeRegisterForm
from core.models import SpkrbarUser, AttendeeProfile, EventProfile

@template('auth/register_attendee.haml')
def register_attendee(request):
    if request.method == "POST":
        form = AttendeeRegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            about_me = form.cleaned_data['about_me']

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
            profile.about_me = about_me
            profile.save()

            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect(request.user.get_profile().get_absolute_url())

    form = AttendeeRegisterForm()
    return {'form': form}
