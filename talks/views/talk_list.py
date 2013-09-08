from core.helpers import template
from talks.models import Talk

@template("talks/talk_list.haml")
def talk_list(request):
    talks = Talk.objects.filter(published=True)

    recently_created = talks.order_by('created_at')[:10]
    recently_updated = talks.order_by('updated_at')[:10]

    return {
        'recently_created': recently_created,
        'recently_updated': recently_updated,
        'last': '/talks' }
