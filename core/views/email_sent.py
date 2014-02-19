from core.helpers import template

@template('auth/email_sent.haml')
def email_sent(request):
    return {}
