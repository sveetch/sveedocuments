# -*- coding: utf-8 -*-
"""
Forms
"""
from django import forms
from django.utils.translation import ugettext as _

from sveedocuments.models import Attachment
from sveedocuments.forms import CrispyFormMixin

class AttachmentForm(CrispyFormMixin, forms.ModelForm):
    """
    Attachment form
    """
    crispy_form_helper_path = 'sveedocuments.forms.crispies.attachment_helper'
    
    def __init__(self, *args, **kwargs):
        self.page = kwargs.pop('page_instance')
        self.author = kwargs.pop('author')
        
        super(AttachmentForm, self).__init__(*args, **kwargs)
        super(forms.ModelForm, self).__init__(*args, **kwargs)
    
    def clean_file(self):
        file = self.cleaned_data['file']
        if file:
            self.size = file._size
            self.content_type = file.content_type

        return file
    
    def save(self, *args, **kwargs):
        instance = super(AttachmentForm, self).save(commit=False, *args, **kwargs)
        instance.page = self.page
        instance.author = self.author
        instance.size = self.size
        instance.content_type = self.content_type
        instance.save()
        
        return instance
    
    class Meta:
        model = Attachment
        fields = ('title', 'slug', 'file')
