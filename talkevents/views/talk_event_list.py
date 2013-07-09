from core.helpers import template
from talkevents.helpers import talk_event_groups

@template("talkevents/talkevent_list.haml")
def talk_event_list(request):
    return {'talk_groups': talk_event_groups(10),
            'last': '/talks' }
