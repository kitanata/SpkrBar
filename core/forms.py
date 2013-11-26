from django import forms

from models import SpkrbarUser

class ProfilePhotoForm(forms.Form):
    photo = forms.FileField(required=False)


class SpeakerRegisterForm(forms.Form):
    email = forms.EmailField(max_length=254)
    full_name = forms.CharField()
    about_me = forms.CharField(max_length=1400, required=False,
            widget=forms.Textarea(attrs={'rows':6, 'cols':40}))

    password = forms.CharField(min_length=8, widget=forms.PasswordInput())
    confirm = forms.CharField(min_length=8, widget=forms.PasswordInput())
