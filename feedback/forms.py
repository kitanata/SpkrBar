#!/usr/bin/env python
from django import forms

from feedback.models import Feedback

class FeedbackForm(forms.ModelForm):
    '''The form shown when giving feedback'''
    class Meta:
        model = Feedback
        #exclude = ('site', 'url')

# vim: et sw=4 sts=4
