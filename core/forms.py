from django import forms

from models import SpeakerLink, SpkrbarUser

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



class ProfilePhotoForm(forms.Form):
    photo = forms.FileField(required=False)



class ProfileLinkForm(forms.Form):
    type = forms.ChoiceField(SpeakerLink.LINK_TYPE_CHOICES)
    url = forms.URLField(max_length=140, 
            widget=forms.TextInput(attrs={'placeholder': 'http://'}))



class ProfileTagForm(forms.Form):
    name = forms.CharField(max_length=140,
            widget=forms.TextInput(attrs={'placeholder': 'What are you known for?'}))


class SpeakerRegisterForm(forms.Form):
    username = forms.CharField(max_length=40)
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    about_me = forms.CharField(max_length=1400, widget=forms.Textarea(attrs={'rows':6, 'cols':40}))

    password = forms.CharField(min_length=8, widget=forms.PasswordInput())
    confirm = forms.CharField(min_length=8, widget=forms.PasswordInput())


class EventRegisterForm(forms.Form):
    username = forms.CharField(max_length=40)
    name = forms.CharField()
    description = forms.CharField(max_length=1400, widget=forms.Textarea(attrs={'rows':6, 'cols':40}))
    email = forms.EmailField()

    password = forms.CharField(min_length=8, widget=forms.PasswordInput())
    confirm = forms.CharField(min_length=8, widget=forms.PasswordInput())


class AttendeeRegisterForm(forms.Form):
    username = forms.CharField(max_length=40)
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    password = forms.CharField(min_length=8, widget=forms.PasswordInput())
    confirm = forms.CharField(min_length=8, widget=forms.PasswordInput())
