from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound

from core.models import UserTag

from core.forms import ProfileTagForm

@login_required
def profile_tag_new(request):
    if request.method == "POST":
        form = ProfileTagForm(request.POST)

        if form.is_valid():
            tag_name = form.cleaned_data['name']

            try:
                tag_model = UserTag.objects.get(name=tag_name)
            except ObjectDoesNotExist as e:
                tag_model = UserTag(name=tag_name)
                tag_model.save()

            request.user.tags.add(tag_model)
            request.user.save()

            return redirect(request.user.get_absolute_url())
    else:
        return HttpResponseNotFound()
