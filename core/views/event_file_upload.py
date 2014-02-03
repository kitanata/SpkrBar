import json
from datetime import datetime, timedelta
from itertools import groupby, chain

from django.db.models import Q
from django.http import HttpResponseBadRequest
from django.shortcuts import render_to_response

from engagements.models import Engagement
from core.helpers import template

def event_file_upload(request):
    if request.method != "POST":
        return HttpResponseBadRequest()

    return render_to_response('upload_success.haml')
