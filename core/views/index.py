from core.helpers import template
from django.shortcuts import redirect

@template('index.haml')
def index(request):
    if not request.user.is_anonymous():
        return redirect(request.user.get_absolute_url())
    return {}
