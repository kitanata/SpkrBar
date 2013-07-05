# Create your views here.
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from core.models import SpkrbarUser

@login_required
def user_follow(request, username):
    to_follow = get_object_or_404(SpkrbarUser, username=username)

    if request.user in to_follow.followers.all():
        to_follow.followers.remove(request.user)
        to_follow.save()

        request.user.following.remove(to_follow)
        request.user.save()
    else:
        to_follow.followers.add(request.user)
        to_follow.save()

        request.user.following.add(to_follow)
        request.user.save()

    if request.GET['last']:
        return redirect(request.GET['last'])
    else:
        return redirect('/')
