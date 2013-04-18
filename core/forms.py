from django import forms

from models import UserLink, Location

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
    type = forms.ChoiceField(UserLink.LINK_TYPE_CHOICES)
    name = forms.CharField(max_length=200)
    url = forms.URLField(max_length=140)

class ProfileTagForm(forms.Form):
    name = forms.CharField(max_length=140)

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
