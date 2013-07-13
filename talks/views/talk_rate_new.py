from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound

from guardian.shortcuts import assign

from talks.models import Talk, TalkRating
from talks.forms import TalkRatingForm

@login_required
def talk_rate_new(request, talk_id):
    if request.method == 'POST': # If the form has been submitted...
        rating_form = TalkRatingForm(request.POST)

        if rating_form.is_valid():
            talk = get_object_or_404(Talk, pk=talk_id)

            rating = TalkRating(rater=request.user, talk=talk)
            rating.engagement = rating_form.cleaned_data['engagement']
            rating.knowledge = rating_form.cleaned_data['knowledge']
            rating.professionalism = rating_form.cleaned_data['professionalism']
            rating.resources = rating_form.cleaned_data['resources']
            rating.discussion = rating_form.cleaned_data['discussion']

            rating.save()

            return redirect('/talk/' + str(talk.id))

    return HttpResponseNotFound()
