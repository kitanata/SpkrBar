from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseNotFound

@login_required
def talk_video_new(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)

    if not request.user.has_perm('change_talk', talk):
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = TalkVideoForm(request.POST)

        if form.is_valid():
            video = TalkVideo()
            video.talk = talk

            embed = form.cleaned_data['embed']
            embed = embed.split(' ')
            embed = [x.split('=') for x in embed]
            embed = [x for x in embed if len(x) == 2]
            embed = {x[0]: x[1].strip(""" "'""") for x in embed}

            video.source = form.cleaned_data['source']

            if video.source == YOUTUBE or video.source == VIMEO:
                video.data = embed['src']
                w = embed['width']
                h = embed['height']
                video.aspect = int(w) / float(h) if float(h) != 0 else 0
            else:
                return HttpResponseNotFound()

            video.save()

            return redirect(talk)

    return HttpResponseNotFound()
