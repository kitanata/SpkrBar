from core.helpers import template

@template('base.haml')
def index(request):
    return {}