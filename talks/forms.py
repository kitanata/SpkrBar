from django import forms

# 'Field', 'CharField', 'IntegerField',
# 'DateField', 'TimeField', 'DateTimeField', 'TimeField',
# 'RegexField', 'EmailField', 'FileField', 'ImageField', 'URLField',
# 'BooleanField', 'NullBooleanField', 'ChoiceField', 'MultipleChoiceField',
# 'ComboField', 'MultiValueField', 'FloatField', 'DecimalField',
# 'SplitDateTimeField', 'IPAddressField', 'GenericIPAddressField', 'FilePathField',
# 'SlugField', 'TypedChoiceField', 'TypedMultipleChoiceField'

class NewTalkForm(forms.Form):
    name = forms.CharField(max_length=140)
    description = forms.CharField(widget=forms.Textarea)
    date = forms.DateTimeField()
    location_name = forms.CharField(max_length=140)
    location_address = forms.CharField(max_length=140)
    location_city = forms.CharField(max_length=140)
    location_state = forms.CharField(max_length=40)
