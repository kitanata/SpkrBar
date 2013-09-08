import dateutil.parser
from datetime import datetime
from string import Template

from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import action

from engagements.models import Engagement
from engagements.serializers import EngagementSerializer

from core.models import Notification
from talks.models import Talk
from events.models import Event

class EngagementDetail(viewsets.ModelViewSet):
    queryset = Engagement.objects.all()
    serializer_class = EngagementSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def create(self, request):
        talk_id = request.DATA['talk']
        event_id = request.DATA['event']
        from_speaker = request.DATA['from_speaker']
        date = dateutil.parser.parse(request.DATA['date']).replace(tzinfo=None)

        talk = Talk.objects.get(pk=talk_id)
        event = Event.objects.get(pk=event_id)

        newEngagement = super(EngagementDetail, self).create(request)
        my_id = newEngagement.data['id']

        from_speaker_past = Template("""
            $speaker says that they spoke about $talk at $event.
            Is this true? 
            <div class="btn-group"> <a id="confirm-engagement" class="btn btn-warning" data-id="$id">Yes</a> <a id="decline-engagement" class="btn btn-warning" data-id="$id">No</a> </div>
        """)

        from_speaker_future = Template("""
            $speaker would like to speak about $talk at $event.
            Is that okay?
            <div class="btn-group"> <a id="confirm-engagement" class="btn btn-warning" data-id="$id">Yes</a> <a id="decline-engagement" class="btn btn-warning" data-id="$id">No</a> </div>
        """)

        from_event_past = Template("""
            $event says that you spoke about $talk at their event.
            Is this true? 
            <div class="btn-group"> <a id="confirm-engagement" class="btn btn-warning" data-id="$id">Yes</a> <a id="decline-engagement" class="btn btn-warning" data-id="$id">No</a> </div>
        """)

        from_event_future = Template("""
            $event would like to speak about $talk at their event.
            Is that okay?
            <div class="btn-group"> <a id="confirm-engagement" class="btn btn-warning" data-id="$id">Yes</a> <a id="decline-engagement" class="btn btn-warning" data-id="$id">No</a> </div>
        """)

        if from_speaker:
            if date < datetime.now():
                message = from_speaker_past.substitute(
                        id=my_id,
                        speaker=talk.speaker.user.get_full_name(),
                        talk=talk.name,
                        event=str(event))
            else:
                message = from_speaker_future.substitute(
                        id=my_id,
                        speaker=talk.speaker.user.get_full_name(),
                        talk=talk.name,
                        event=str(event))

            new_note = Notification()
            new_note.title = "Engagement Request"
            new_note.date = datetime.now()
            new_note.user = event.owner.user
            new_note.message = message
            new_note.save()
        else:
            if date < datetime.now():
                message = from_speaker_past.substitute(
                        id=my_id,
                        talk=talk.name,
                        event=str(event))
            else:
                message = from_speaker_future.substitute(
                        id=my_id,
                        talk=talk.name,
                        event=str(event))

            new_note = Notification()
            new_note.title = "Engagement Request"
            new_note.date = datetime.now()
            new_note.user = talk.speaker.user
            new_note.message = message
            new_note.save()

        return newEngagement
