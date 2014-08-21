# -*- coding: utf-8 -*-
"""
Forms
"""
from django import forms
from django.utils.translation import ugettext

from mptt.forms import TreeNodeChoiceField

from crispy_forms.helper import FormHelper
from crispy_forms_foundation.layout import Layout, Fieldset, SplitDateTimeField, RowFluid, Column, ButtonHolder, Submit

from djangocodemirror.fields import CodeMirrorWidget

from rstview.parser import SourceReporter, map_parsing_errors

from sveedocuments.local_settings import DOCUMENTS_PAGE_RESERVED_SLUGS
from sveedocuments.models import Insert, Page, Attachment

class PageForm(forms.ModelForm):
    """
    Page form
    """
    def __init__(self, author=None, parent=None, *args, **kwargs):
        self.author = author
        self.parent = parent
        
        # Put "parent" field in the layout if it is not forced in kwargs
        layout_fields_publish = [
            RowFluid(
                Column(SplitDateTimeField('published'), css_class='six'),
                Column('slug', css_class='six'),
            )
        ]
        if not self.parent:
            layout_fields_publish = ['parent']+layout_fields_publish
        
        self.helper = FormHelper()
        self.helper.form_action = '.'
        self.helper.layout = Layout(
            Fieldset(
                ugettext('Content'),
                'title',
                'content',
            ),
            Fieldset(
                ugettext('Display settings'),
                RowFluid(
                    Column('template', css_class='six'),
                    Column('order', css_class='three'),
                    Column('visible', css_class='three'),
                ),
            ),
            Fieldset(
                ugettext('Publish settings'),
                *layout_fields_publish
            ),
            Fieldset(
                ugettext('History'),
                'comment',
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
        extra_settings = {}
        if self.instance.id:
            parent_queryset = Page.objects.all()
            children = self.instance.get_descendants(include_self=True).values_list('id', flat=True)
            parent_queryset = parent_queryset.exclude(id__in=children)
            self.fields['parent'] = TreeNodeChoiceField(queryset=parent_queryset, empty_label=ugettext(u"-- Root --"), required=False)
        # En cas de création, mode pour ajouter une page directement sous un "parent"
        else:
            if self.parent:
                del self.fields['parent']
            # Désactive l'option de sauvegarde rapide
            extra_settings = {'quicksave_url': None}
            
        # Widget d'édition du contenu
        self.fields['content'].widget = CodeMirrorWidget(attrs={'rows': 30}, config_name='sveetchies-documents-page')
    
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
    Insert form
    """
    def __init__(self, author=None, *args, **kwargs):
        self.author = author
        self.helper = FormHelper()
        self.helper.form_action = '.'
        self.helper.layout = Layout(
            Fieldset(
                ugettext('Content'),
                'title',
                'content',
            ),
            Fieldset(
                ugettext('Display settings'),
                RowFluid(
                    Column('slug', css_class='nine'),
                    Column('visible', css_class='three'),
                ),
            ),
            ButtonHolder(
                Submit('submit_and_continue', ugettext('Save and continue')),
                Submit('submit', ugettext('Save')),
            ),
        )
        
        super(InsertForm, self).__init__(*args, **kwargs)
        
        extra_settings = {}
        if not self.instance.id:
            # Désactive l'option de sauvegarde rapide
            extra_settings = {'quicksave_url': None}
            
        self.fields['content'].widget = CodeMirrorWidget(attrs={'rows': 30}, config_name='sveetchies-documents-insert')
    
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

class InsertQuickForm(PageQuickForm):
    """
    *Insert* quicksave form
    """
    class Meta:
        model = Insert
        fields = ('content',)


class AttachmentForm(forms.ModelForm):
    """
    Attachment form
    """
    def __init__(self, *args, **kwargs):
        self.page = kwargs.pop('page_instance')
        self.author = kwargs.pop('author')
        
        self.helper = FormHelper()
        self.helper.form_action = '.'
        self.helper.layout = Layout(
            RowFluid(
                Column('title', css_class='four'),
                Column('slug', css_class='four'),
                Column('file', css_class='four'),
            ),
            ButtonHolder(
                Submit('submit', ugettext('Save')),
            ),
        )
        super(AttachmentForm, self).__init__(*args, **kwargs)
    
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
