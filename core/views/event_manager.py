from core.helpers import template
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
@template('event_manager.haml')
def event_manager(request):
    return {}
