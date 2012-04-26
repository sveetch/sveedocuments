# -*- coding: utf-8 -*-
"""
Forms
"""
from django import forms
from django.utils.translation import ugettext

from mptt.forms import TreeNodeChoiceField

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, MultiField, Div, ButtonHolder, Submit, HTML

from djangocodemirror.settings_local import CODEMIRROR_SETTINGS
from djangocodemirror.fields import CodeMirrorWidget

from sveedocuments.settings_local import DOCUMENTS_PAGE_RESERVED_SLUGS
from sveedocuments.models import Insert, Page
from sveedocuments.parser import SourceReporter, map_parsing_errors

class PageForm(forms.ModelForm):
    """
    *Page* form
    """
    def __init__(self, author=None, parent=None, *args, **kwargs):
        self.author = author
        self.parent = parent
        
        empty_label = u"-- {0} --".format(ugettext("Root"))
        layout_parameters_fields = ['order', 'visible', 'published', 'template', 'slug']
        if not self.parent:
            layout_parameters_fields = ['parent']+layout_parameters_fields
        
        self.helper = FormHelper()
        self.helper.form_action = '.'
        self.helper.form_style = 'inline'
        self.helper.layout = Layout(
            Div(
                Fieldset(
                    ugettext('Content'),
                    'title',
                    'content',
                ),
                Fieldset(
                    ugettext('Settings'), *layout_parameters_fields),
                css_class = 'combined-multiple-fieldsets'
            ),
            ButtonHolder(
                Submit('submit_and_continue', ugettext('Save and continue')),
                Submit('submit', ugettext('Save')),
            ),
        )
        
        super(PageForm, self).__init__(*args, **kwargs)
        
        # En cas d'édition, limite les choix de parenté à tout ceux qui ne sont pas 
        # descendant de l'instance pour empêcher une exception 
        # sur une erreur de déplacement
        if self.instance.id:
            parent_queryset = Page.objects.all()
            children = self.instance.get_descendants(include_self=True).values_list('id', flat=True)
            parent_queryset = parent_queryset.exclude(id__in=children)
            self.fields['parent'] = TreeNodeChoiceField(queryset=parent_queryset, empty_label=ugettext(u"-- Root --"), required=False)
            # Options par défaut pour le widget d'édition
            content_widget_settings = CODEMIRROR_SETTINGS['sveetchies-documents-page']
        # En cas de création, mode pour ajouter une page directement sous un "parent"
        else:
            if self.parent:
                del self.fields['parent']
            # Options par défaut pour le widget d'édition moins l'option de sauvegarde 
            # rapide
            content_widget_settings = CODEMIRROR_SETTINGS['sveetchies-documents-page'].copy()
            del content_widget_settings['quicksave_url']
            
        # Widget d'édition du contenu
        self.fields['content'].widget = CodeMirrorWidget(attrs={'rows': 30}, codemirror_attrs=content_widget_settings)
    
    def clean_slug(self):
        slug = self.cleaned_data.get("slug")
        if slug:
            if slug in DOCUMENTS_PAGE_RESERVED_SLUGS:
                raise forms.ValidationError(ugettext('This is a reserved keyword'))
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
        instance = super(PageForm, self).save(commit=False, *args, **kwargs)
        instance.author = self.author
        if self.parent:
            instance.parent = self.parent
        instance.save()
        
        return instance
    
    class Meta:
        model = Page
        exclude = ('created', 'author')
        widgets = {
            'published': forms.SplitDateTimeWidget,
        }

class InsertForm(forms.ModelForm):
    """
    *Insert* form
    """
    def __init__(self, author=None, *args, **kwargs):
        self.author = author
        self.helper = FormHelper()
        self.helper.form_action = '.'
        self.helper.form_style = 'inline'
        self.helper.add_input(Submit('submit_and_continue', ugettext('Save and continue')))
        self.helper.add_input(Submit('submit', ugettext('Save')))
        
        super(InsertForm, self).__init__(*args, **kwargs)
        
        if self.instance.id:
            # Options par défaut pour le widget d'édition
            content_widget_settings = CODEMIRROR_SETTINGS['sveetchies-documents-insert']
        else:
            # Options par défaut pour le widget d'édition moins l'option de sauvegarde 
            # rapide
            content_widget_settings = CODEMIRROR_SETTINGS['sveetchies-documents-insert'].copy()
            del content_widget_settings['quicksave_url']
            
        self.fields['content'].widget = CodeMirrorWidget(attrs={'rows': 30}, codemirror_attrs=content_widget_settings)
    
    def clean_slug(self):
        slug = self.cleaned_data.get("slug")
        if slug:
            if slug in DOCUMENTS_PAGE_RESERVED_SLUGS:
                raise forms.ValidationError(ugettext('This is a reserved keyword'))
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
        instance = super(InsertForm, self).save(commit=False, *args, **kwargs)
        instance.author = self.author
        instance.save()
        
        return instance
    
    class Meta:
        model = Insert
        exclude = ('created', 'author')
        widgets = {
            # Necessary to change "self.fields['content'].widget" in __init__
            'content': CodeMirrorWidget(attrs={'rows': 30}), 
        }

class PageQuickForm(forms.ModelForm):
    """
    *Page* quicksave form
    
    This is only about the instance *content* field
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

class InsertQuickForm(PageQuickForm):
    """
    *Insert* quicksave form
    """
    class Meta:
        model = Insert
        fields = ('content',)
