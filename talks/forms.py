from django import forms
from datetimewidget.widgets import DateTimeWidget

from .models import Talk
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
                    <div class="span2">
                        %(initial)s
                    </div>
                    <div class="span3">
                        %(clear_template)s
                        <br />
                        %(input_text)s:
                        %(input)s
                    </div>
                </div>
            """

            print self.template_with_clear

            clear_template = """
                Clear: 
                %(clear)s
                """


            substitutions['initial'] = ('<img src="' + settings.STATIC_URL + 'img/photo/%s" alt="%s"/>'
                                        % (escape(value.url),
                                           escape(force_unicode(value))))
            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                substitutions['clear_checkbox_name'] = conditional_escape(checkbox_name)
                substitutions['clear_checkbox_id'] = conditional_escape(checkbox_id)
                substitutions['clear'] = CheckboxInput().render(checkbox_name, False, attrs={'id': checkbox_id})
                substitutions['clear_template'] = clear_template % substitutions

        return mark_safe(template % substitutions)

class TalkForm(forms.ModelForm):
    class Meta:
        model = Talk
        widgets = {
            'abstract': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
            'date': DateTimeWidget(),
            'photo': CustomClearableFileInput()
        }
        exclude = ('speakers', 'media', 'published', 'tags', 'attendees', 'endorsements')
