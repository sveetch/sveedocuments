# -*- coding: utf-8 -*-
"""
Page forms
"""
from django import forms
from django.utils.translation import ugettext as _

from mptt.forms import TreeNodeChoiceField

from djangocodemirror.fields import CodeMirrorWidget

from rstview.parser import SourceReporter, map_parsing_errors

from sveedocuments.local_settings import DOCUMENTS_PAGE_RESERVED_SLUGS
from sveedocuments.models import Page, documents_page_update_signal
from sveedocuments.forms import CrispyFormMixin

class PageForm(CrispyFormMixin, forms.ModelForm):
    """
    Page form
    """
    crispy_form_helper_path = 'sveedocuments.forms.crispies.page_helper'
    codemirror_config_name = 'sveetchies-documents-add-page'
    
    def __init__(self, author=None, parent=None, *args, **kwargs):
        self.author = author
        self.parent = parent

        self.crispy_form_helper_kwargs = {'parent': self.parent}
        
        super(PageForm, self).__init__(*args, **kwargs)
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        
        # En cas d'édition, limite les choix de parenté à tout ceux qui ne sont pas 
        # descendant de l'instance pour empêcher une exception 
        # sur une erreur de déplacement
        extra_settings = {}
        if self.instance.id:
            parent_queryset = Page.objects.all()
            children = self.instance.get_descendants(include_self=True).values_list('id', flat=True)
            parent_queryset = parent_queryset.exclude(id__in=children)
            self.fields['parent'] = TreeNodeChoiceField(queryset=parent_queryset, empty_label=_(u"-- Root --"), required=False)
        # En cas de création, mode pour ajouter une page directement sous un "parent"
        else:
            if self.parent:
                del self.fields['parent']
            # Désactive l'option de sauvegarde rapide
            extra_settings = {'quicksave_url': None}
            
        # Widget d'édition du contenu
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

        instance = super(PageForm, self).save(commit=False, *args, **kwargs)
        instance.author = self.author
        if self.parent:
            instance.parent = self.parent
        instance.save()
        
        # Send a Django signal for page update
        documents_page_update_signal.send(sender=self, page_instance=instance, edited=edited)
        
        return instance
    
    class Meta:
        model = Page
        exclude = ('created', 'author')
        widgets = {
            'published': forms.SplitDateTimeWidget,
        }


class PageEditForm(PageForm):
    crispy_form_helper_path = 'sveedocuments.forms.crispies.page_edit_helper'
    codemirror_config_name = 'sveetchies-documents-edit-page'


class PageQuickForm(forms.ModelForm):
    """
    *Page* quicksave form
    
    This is only about the instance *content* field
    
    TODO: This should also accepts the associated 'comment' field, but in first the 
          editor must implement to send the "comment" content with the "content" 
          content.
    """
    def __init__(self, author=None, *args, **kwargs):
        self.author = author
        super(PageQuickForm, self).__init__(*args, **kwargs)
    
    def clean_content(self):
        """
        Parse content to check syntax alerts
        """
        content = self.cleaned_data.get("content")
        if content:
            errors = SourceReporter(content)
            if errors:
                raise forms.ValidationError(map(map_parsing_errors, errors))
        return content
    
    def save(self, *args, **kwargs):
        instance = super(PageQuickForm, self).save(commit=True, *args, **kwargs)
        return instance
    
    class Meta:
        model = Page
        fields = ('content',)
