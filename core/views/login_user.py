from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponseForbidden

from core.helpers import render_to


def login_user(request):
    if request.method == "GET":
        return render_to(request, 'auth/login.haml')
    else:
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(request.user.get_absolute_url())
            else:
                error = "This account has been disabled."
        else:
            error = "Could not find the email or the password is incorrect."

        return render_to(request, 'auth/login.haml', context={'error': error})
