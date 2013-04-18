from django import forms
from datetimewidget.widgets import DateTimeWidget

from .models import Talk

# 'Field', 'CharField', 'IntegerField',
# 'DateField', 'TimeField', 'DateTimeField', 'TimeField',
# 'RegexField', 'EmailField', 'FileField', 'ImageField', 'URLField',
# 'BooleanField', 'NullBooleanField', 'ChoiceField', 'MultipleChoiceField',
# 'ComboField', 'MultiValueField', 'FloatField', 'DecimalField',
# 'SplitDateTimeField', 'IPAddressField', 'GenericIPAddressField', 'FilePathField',
# 'SlugField', 'TypedChoiceField', 'TypedMultipleChoiceField'

class TalkForm(forms.ModelForm):
    class Meta:
        model = Talk
        widgets = {
            'abstract': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
            'date': DateTimeWidget()
        }
        exclude = ('speakers', 'media', 'tags')
