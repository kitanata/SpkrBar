import json
from datetime import datetime, timedelta
from itertools import groupby, chain

from django.db.models import Q

from engagements.models import Engagement
from core.helpers import template

@template('events/event_base.haml')
def event_detail(request, slug):
    slugs = slug.split('-')
    name = ' '.join(map(lambda x: x.capitalize(), slugs))
    engagements = Engagement.objects.filter(
        reduce(lambda x, y: x & y, [Q(event_name__icontains=x) for x in slugs]),
        )

    engagements = sorted(list(engagements), key=lambda x: x.date.year)
    #talks = {k: list(v) for k, v in groupby(engagements, key=lambda x: x.date.year)}

    speakers = set([e.talk.speaker for e in engagements])

    tags = list(reduce(lambda x, y : x | y, map(lambda z: z.talk.tags.all(), engagements)))
    tags = sorted([(tags.count(x), x.name) for x in set(tags)], key=lambda x: -x[0])
    tag_vals = [t[0] for t in tags]
    tag_median = tag_vals[max(len(tag_vals) / 2 - 1, 0)]
    tags = [t for t in tags if t[0] >= tag_median]

    return {
        'name': name,
        'num_engagements': len(engagements),
        'num_speakers': len(speakers),
        'speakers': json.dumps([x.id for x in speakers]),
        'tags': json.dumps(tags),
        'talks': json.dumps([x.id for x in engagements]),
    }
