from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from django.db import IntegrityError

from core.helpers import render_to

def register_user(request):
    if request.method == "GET":
        return render_to(request, 'register.haml')
    else:
        username = request.POST['username']
        password = request.POST['password']
        confirm = request.POST['confirm']
        email = request.POST['email']

        error = None

        if password != confirm:
            error = "Password does not match confirmation."

        if not error:
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
            except IntegrityError as e:
                error = "That username is taken. Try another."

        if not error:
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/speaker/' + request.user.username)

        return render_to(request, 'auth/register.haml', context={'error': error})
