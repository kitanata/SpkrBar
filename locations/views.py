# Create your views here.
from datetime import datetime

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from models import Location
from forms import LocationForm

@login_required
def location_new(request):
    if request.method == 'POST': # If the form has been submitted...
        location_form = LocationForm(request.POST)

        if location_form.is_valid():
            location = location_form.save()
            location.save()

    if 'next' in request.GET:
        return redirect(request.GET['next'])
    else:
        return redirect('/talk/new')
