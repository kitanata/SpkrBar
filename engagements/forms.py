from django import forms

from models import Rating

# 'Field', 'CharField', 'IntegerField',
# 'DateField', 'TimeField', 'DateTimeField', 'TimeField',
# 'RegexField', 'EmailField', 'FileField', 'ImageField', 'URLField',
# 'BooleanField', 'NullBooleanField', 'ChoiceField', 'MultipleChoiceField',
# 'ComboField', 'MultiValueField', 'FloatField', 'DecimalField',
# 'SplitDateTimeField', 'IPAddressField', 'GenericIPAddressField', 'FilePathField',
# 'SlugField', 'TypedChoiceField', 'TypedMultipleChoiceField'

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating

        widgets = {
                'engagement': forms.RadioSelect(),
                'knowledge': forms.RadioSelect(),
                'professionalism': forms.RadioSelect(),
                'resources': forms.RadioSelect(),
                'discussion': forms.RadioSelect()
                }

        exclude = ('talk', 'rater', 'datetime')
