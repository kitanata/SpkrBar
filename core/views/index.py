from core.helpers import template
from django.shortcuts import redirect

@template('index.haml')
def index(request):
    if not request.user.is_anonymous():
        if request.user.is_event_manager:
            return redirect('/manager')
        else:
            return redirect(request.user.get_absolute_url())
    return {}
