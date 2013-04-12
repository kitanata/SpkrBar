from datetime import datetime

from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.views.generic import ListView
from django.template import RequestContext

from .models import Talk
from .forms import NewTalkForm

class TalkList(ListView):
    queryset = Talk.objects.filter(date__gt=datetime.now()).order_by('-date')[:20]
    template_name = "talk_list.html"


def talk_new(request):

    if request.method == 'POST': # If the form has been submitted...
        form = NewTalkForm(request.POST)
        if form.is_valid():
            location = Location(
                    name=form.cleaned_data['location_name'],
                    address=form.cleaned_data['location_address'],
                    city=form.cleaned_data['location_city'],
                    state=form.cleaned_data['location_state'])

            location.save()

            talk = Talk(
                    speaker=request.user,
                    name=form.cleaned_data['name'],
                    description=form.cleaned_data['description'],
                    date=form.cleaned_data['date'],
                    location=location)

            talk.save()

            return redirect('/profile/')
    else:
        form = NewTalkForm()

    return render_to_response('talk_new.html', {'form' : form},
            context_instance=RequestContext(request))

    
def talk_detail(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)

    return render_to_response('talk_detail.html', {'talk': talk},
            context_instance=RequestContext(request))
