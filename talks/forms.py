from django import forms
from .models import *
from config import settings

# 'Field', 'CharField', 'IntegerField',
# 'DateField', 'TimeField', 'DateTimeField', 'TimeField',
# 'RegexField', 'EmailField', 'FileField', 'ImageField', 'URLField',
# 'BooleanField', 'NullBooleanField', 'ChoiceField', 'MultipleChoiceField',
# 'ComboField', 'MultiValueField', 'FloatField', 'DecimalField',
# 'SplitDateTimeField', 'IPAddressField', 'GenericIPAddressField', 'FilePathField',
# 'SlugField', 'TypedChoiceField', 'TypedMultipleChoiceField'

from django.utils.safestring import mark_safe
from django.utils.html import escape, conditional_escape
from django.utils.encoding import force_unicode
from django.forms.widgets import ClearableFileInput, Input, CheckboxInput

from models.choices import *

class CustomClearableFileInput(ClearableFileInput):

    def render(self, name, value, attrs=None):
        substitutions = {
            #uncomment to get 'Currently'
            'input_text': self.input_text,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
            }
        template = """%(input)s"""

        substitutions['input'] = Input.render(self, name, value, attrs)

        if value and hasattr(value, "url"):
            template = """
                <div class="row">
                    <div class="span3">
                        %(input)s
                    </div>
                </div>
            """

            clear_template = """
                Clear: 
                %(clear)s
                """


            substitutions['initial'] = ''

            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                substitutions['clear_checkbox_name'] = conditional_escape(checkbox_name)
                substitutions['clear_checkbox_id'] = conditional_escape(checkbox_id)
                substitutions['clear'] = ''
                substitutions['clear_template'] = ''

        return mark_safe(template % substitutions)


class TalkForm(forms.ModelForm):
    class Meta:
        model = Talk
        widgets = {
            'abstract': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
            'photo': CustomClearableFileInput()
        }
        exclude = ('speaker', 'media', 'published', 'tags', 'attendees', 'endorsements')


class TalkLinkForm(forms.Form):
    name = forms.CharField()
    url = forms.URLField()


class TalkSlideDeckForm(forms.Form):
    source = forms.ChoiceField(choices=SLIDE_TYPE_CHOICES)
    embed = forms.CharField()


class TalkVideoForm(forms.Form):
    source = forms.ChoiceField(choices=VIDEO_TYPE_CHOICES)
    embed = forms.CharField()


class TalkPhotoForm(forms.Form):
    photo = forms.FileField(required=False)
