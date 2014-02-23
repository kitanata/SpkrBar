import json
from datetime import datetime, timedelta
from itertools import groupby, chain

from django.db.models import Q, Count

from engagements.models import Engagement
from core.helpers import template
from core.models import SpkrbarUser

def rank_engagement(engagement):
    points = 0
    if engagement.speaker.photo:
        points += 250
    points += engagement.speaker.tags.count() * 10
    points += engagement.speaker.links.count() * 25
    points += engagement.talk.tags.count() * 20
    points += engagement.talk.links.count() * 30

    return points

@template('events/event_base.haml')
def event_detail(request, slug):
    slugs = slug.split('-')
    name = ' '.join(map(lambda x: x.capitalize(), slugs))
    engagements = Engagement.objects.filter(
        reduce(lambda x, y: x & y, [Q(event_name__icontains=x) for x in slugs]),
        )

    engagements = sorted(list(engagements), key=rank_engagement, reverse=True)
    #talks = {k: list(v) for k, v in groupby(engagements, key=lambda x: x.date.year)}

    talk_ids = set([e.talk.pk for e in engagements])
    speakers = SpkrbarUser.objects.filter(talks__pk__in=talk_ids).annotate(
            num_tags=Count('tags'),
            num_links=Count('links')).order_by(
                    '-photo', '-about_me', '-num_tags', '-num_links')

    tags = []
    if engagements:
        tags = list(reduce(lambda x, y : x | y, map(lambda z: z.talk.tags.all(), engagements)))
        tags = sorted([(tags.count(x), x.name) for x in set(tags)], key=lambda x: -x[0])
        
    tag_vals = [t[0] for t in tags]

    if tag_vals:
        tag_median = tag_vals[max(len(tag_vals) / 2 - 1, 0)]
        tags = [t for t in tags if t[0] >= tag_median]
    else:
        tag_median = 0
        tags = []

    return {
        'name': name,
        'speakers': json.dumps([x.id for x in speakers]),
        'tags': json.dumps(tags),
        'talks': json.dumps([x.id for x in engagements]),
    }
