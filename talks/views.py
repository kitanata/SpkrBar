from datetime import datetime
from itertools import groupby

from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.views.generic import ListView
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist

from core.models import Location
from core.forms import LocationForm
from .models import Talk, TalkTag, TalkComment
from .forms import TalkForm

def talk_list(request):

    talks = Talk.objects.filter(date__gt=datetime.now()).order_by('date')[:20]

    talks = [{
        'month_num': k,
        'date': datetime(month=k[0], year=k[1], day=1).strftime("%B %Y"),
        'talks': list(g)} for k, g in groupby(talks, key=lambda x: (x.date.month, x.date.year))]
    talks.sort(key=lambda x: x['month_num'])

    return render_to_response("talk_list.html", {'talks': talks},
            context_instance=RequestContext(request))


def talk_new(request):

    if request.method == 'POST': # If the form has been submitted...
        talk_form = TalkForm(request.POST, request.FILES)
        location_form = None

        if talk_form.is_valid():
            talk = talk_form.save()
            talk.speakers.add(request.user.get_profile())

            if 'photo' in request.FILES:
                photo = request.FILES['photo']

                with open('talk/static/img/photo/' + photo.name, 'wb+') as destination:
                    for chunk in photo.chunks():
                        destination.write(chunk)

                talk.photo = photo.name

            talk.save()

            return redirect('/talk/' + str(talk.id))
    else:
        talk_form = TalkForm()
        location_form = LocationForm()

    return render_to_response('talk_new.html', {
        'talk_form' : talk_form,
        'location_form' : location_form
        }, context_instance=RequestContext(request))

    
def talk_detail(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)

    return render_to_response('talk_detail.html', {'talk': talk},
            context_instance=RequestContext(request))


def talk_edit(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)

    if request.method == 'POST': # If the form has been submitted...
        talk_form = TalkForm(request.POST, instance=talk)
        if talk_form.is_valid():
            talk = talk_form.save()

            return redirect('/talk/' + str(talk.id))
    else:
        talk_form = TalkForm(instance=talk)

    location_form = LocationForm()

    return render_to_response('talk_edit.html', {
        'talk_form': talk_form,
        'location_form': location_form
        }, context_instance=RequestContext(request))


def talk_delete(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)
    talk.delete()

    return redirect('/speaker/' + request.user.username)


def location_new(request):
    if request.method == 'POST': # If the form has been submitted...
        location_form = LocationForm(request.POST)

        if location_form.is_valid():
            location = location_form.save()
            location.save()

    return redirect('/talk/new')


def talk_tag_new(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)

    if request.method == "POST":
        tag = request.POST['tag']

        try:
            tag_obj = TalkTag.objects.get(name=tag)
        except ObjectDoesNotExist as e:
            tag_obj = TalkTag(name=tag)
            tag_obj.save()

        talk.tags.add(tag_obj)

    return redirect('/talk/' + talk_id)


def talk_comment_new(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)

    if request.method == "POST":
        if request.user.get_profile() not in talk.speakers.all():
            comment = TalkComment(
                    talk=talk,
                    reviewer=request.user.get_profile(),
                    comment = request.POST['comment'])

            comment.save()

    return redirect('/talk/' + talk_id)
