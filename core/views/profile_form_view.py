from django.contrib.auth.decorators import login_required

from core.helpers import template

from core.forms import EditProfileForm, ProfilePhotoForm

@login_required
@template('profile/profile_edit.haml')
def profile_form_view(request):
    profile = request.user.get_profile()
    profile_form = EditProfileForm({
        'name':request.user.get_full_name(),
        'about_me':profile.about_me
    })
    photo_form = ProfilePhotoForm()

    return {
        'speaker': request.user.get_profile(),
        'profile_form': profile_form,
        'photo_form': photo_form,
        }
