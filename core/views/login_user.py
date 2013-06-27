from django.shortcuts import redirect
from django.contrib.auth import authenticate, login

from core.helpers import render_to

def login_user(request):
    if request.method == "GET":
        return render_to(request, 'auth/login.haml')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(request.user.get_profile())
            else:
                error = "This account has been disabled."
        else:
            error = "Username or password is incorrect."

        return render_to(request, 'auth/login.haml', context={'error': error})
