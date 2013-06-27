from django.contrib.auth.decorators import login_required

from core.helpers import template

from core.forms import EditProfileForm, ProfilePhotoForm, ProfileLinkForm, ProfileTagForm

@login_required
@template('profile_edit.haml')
def profile_form_view(request):
    profile = request.user
    profile_form = EditProfileForm({
        'name':request.user.get_full_name(),
        'about_me':profile.about_me
    })
    photo_form = ProfilePhotoForm()
    link_form = ProfileLinkForm()
    tag_form = ProfileTagForm()

    return {
        'speaker': request.user,
        'profile_form': profile_form,
        'photo_form': photo_form,
        'tag_form': tag_form,
        'link_form': link_form
        }
