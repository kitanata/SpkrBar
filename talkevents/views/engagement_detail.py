import dateutil.parser
from datetime import datetime
from talkevents.models import TalkEvent
from talkevents.serializers import EngagementSerializer
from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import action

from core.models import Notification
from talks.models import Talk
from events.models import Event

class EngagementDetail(viewsets.ModelViewSet):
    queryset = TalkEvent.objects.all()
    serializer_class = EngagementSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def create(self, request):
        talk_id = request.DATA['talk']
        event_id = request.DATA['event']
        from_speaker = request.DATA['from_speaker']
        date = dateutil.parser.parse(request.DATA['date']).replace(tzinfo=None)

        talk = Talk.objects.get(pk=talk_id)
        event = Event.objects.get(pk=event_id)

        if from_speaker:
            print date
            print datetime.now()
            if date < datetime.now():
                message = "%s says that they spoke at %s. Is this true? <a href='/confirm'>Yes</a> <a href='/decline'>No</a>"
            else:
                message = "%s would like to speak at %s. Is that okay? <a href='/confirm'>Yes</a> <a href='/decline'>No</a>"

            message = message % (talk.speaker.user.get_full_name(), str(event))

            new_note = Notification()
            new_note.title = "Engagement Request"
            new_note.date = datetime.now()
            new_note.user = event.owner.user
            new_note.message = message
            new_note.save()
        else:
            if date < datetime.now():
                message = "%s says that you spoke at their event. Is this true? <a href='/confirm'>Yes</a> <a href='/decline'>No</a>"
            else:
                message = "%s would like you to speak at their event. Is that okay? <a href='/confirm'>Yes</a> <a href='/decline'>No</a>"

            message = message % (str(event), )

            new_note = Notification()
            new_note.title = "Engagement Request"
            new_note.date = datetime.now()
            new_note.user = talk.speaker.user
            new_note.message = message
            new_note.save()

        return super(EngagementDetail, self).create(request)
