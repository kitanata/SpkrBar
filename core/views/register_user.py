from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.forms.util import ErrorList

from django.db import IntegrityError

from core.helpers import template

@template('auth/register.haml')
def register_user(request):
    pass
