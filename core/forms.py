from django import forms

from models import UserLink, SpkrbarUser

# 'Field', 'CharField', 'IntegerField',
# 'DateField', 'TimeField', 'DateTimeField', 'TimeField',
# 'RegexField', 'EmailField', 'FileField', 'ImageField', 'URLField',
# 'BooleanField', 'NullBooleanField', 'ChoiceField', 'MultipleChoiceField',
# 'ComboField', 'MultiValueField', 'FloatField', 'DecimalField',
# 'SplitDateTimeField', 'IPAddressField', 'GenericIPAddressField', 'FilePathField',
# 'SlugField', 'TypedChoiceField', 'TypedMultipleChoiceField'

class EditProfileForm(forms.Form):
    name = forms.CharField(max_length=140)
    about_me = forms.CharField(max_length=1400, widget=forms.Textarea(attrs={'rows':6, 'cols':40}))


class EventEditProfileForm(forms.Form):
    name = forms.CharField(max_length=140)
    description = forms.CharField(max_length=1400, widget=forms.Textarea(attrs={'rows':6, 'cols':40}))


class ProfilePhotoForm(forms.Form):
    photo = forms.FileField(required=False)


class ProfileLinkForm(forms.Form):
    type = forms.ChoiceField(UserLink.LINK_TYPE_CHOICES)
    url = forms.CharField(max_length=140, 
            widget=forms.TextInput(attrs={'placeholder': 'URL or Username'}))


class ProfileTagForm(forms.Form):
    name = forms.CharField(max_length=140,
            widget=forms.TextInput(attrs={'placeholder': 'What are you known for?'}))


class SpeakerRegisterForm(forms.Form):
    email = forms.EmailField(max_length=254)
    full_name = forms.CharField()
    about_me = forms.CharField(max_length=1400, required=False,
            widget=forms.Textarea(attrs={'rows':6, 'cols':40}))

    password = forms.CharField(min_length=8, widget=forms.PasswordInput())
    confirm = forms.CharField(min_length=8, widget=forms.PasswordInput())
