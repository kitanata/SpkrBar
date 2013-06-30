from django import forms

from models import SpeakerLink

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
