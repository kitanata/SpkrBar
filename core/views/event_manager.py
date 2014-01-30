from core.helpers import template
from django.shortcuts import redirect

@template('event_manager.haml')
def event_manager(request):
    return {}
