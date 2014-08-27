# -*- coding: utf-8 -*-
"""
Insert forms
"""
from django import forms
from django.utils.translation import ugettext as _

from djangocodemirror.fields import CodeMirrorWidget

from rstview.parser import SourceReporter, map_parsing_errors

from sveedocuments.local_settings import DOCUMENTS_PAGE_RESERVED_SLUGS
from sveedocuments.models import Insert, documents_insert_update_signal
from sveedocuments.forms import CrispyFormMixin
from sveedocuments.forms.page import PageQuickForm

class InsertForm(CrispyFormMixin, forms.ModelForm):
    """
    Insert form
    """
    crispy_form_helper_path = 'sveedocuments.forms.crispies.insert_helper'
    codemirror_config_name = 'sveetchies-documents-add-insert'
    
    def __init__(self, author=None, *args, **kwargs):
        self.author = author
        
        super(InsertForm, self).__init__(*args, **kwargs)
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        
        extra_settings = {}
        if not self.instance.id:
            # Désactive l'option de sauvegarde rapide
            extra_settings = {'quicksave_url': None}
            
        self.fields['content'].widget = CodeMirrorWidget(attrs={'rows': 30}, config_name=self.codemirror_config_name)
    
    def clean_slug(self):
        slug = self.cleaned_data.get("slug")
        if slug:
            if slug in DOCUMENTS_PAGE_RESERVED_SLUGS:
                raise forms.ValidationError(_('This is a reserved keyword'))
        return slug
    
    def clean_content(self):
        """
        Parse le contenu pour vérifier qu'il ne contient par d'erreurs de syntaxe
        """
        content = self.cleaned_data.get("content")
        if content:
            errors = SourceReporter(content)
            if errors:
                raise forms.ValidationError(map(map_parsing_errors, errors))
        return content
    
    def save(self, *args, **kwargs):
        edited = (self.instance and self.instance.id)

        instance = super(InsertForm, self).save(commit=False, *args, **kwargs)
        instance.author = self.author
        instance.save()
        
        # Send a Django signal for page update
        documents_insert_update_signal.send(sender=self, insert_instance=instance, edited=edited)
        
        return instance
    
    class Meta:
        model = Insert
        exclude = ('created', 'author')
        widgets = {
            # Necessary to change "self.fields['content'].widget" in __init__
            'content': CodeMirrorWidget(attrs={'rows': 30}), 
        }


class InsertEditForm(InsertForm):
    crispy_form_helper_path = 'sveedocuments.forms.crispies.insert_edit_helper'
    codemirror_config_name = 'sveetchies-documents-edit-insert'


class InsertQuickForm(PageQuickForm):
    """
    *Insert* quicksave form
    """
    class Meta:
        model = Insert
        fields = ('content',)
