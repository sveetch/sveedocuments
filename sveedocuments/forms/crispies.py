"""
Crispy forms layouts
"""
from django import forms
from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper
from crispy_forms_foundation.layout import Layout, Fieldset, SplitDateTimeField, RowFluid, Column, ButtonHolder, Submit

def page_helper(form_tag=True, parent=None, edit_mode=False):
    """
    Page's form layout helper
    """
    helper = FormHelper()
    helper.form_action = '.'
    helper.attrs = {'data_abide': ''}
    helper.form_tag = form_tag
    
    # Put "parent" field in the layout if it is not forced in kwargs
    layout_fields_publish = [
        RowFluid(
            Column(SplitDateTimeField('published'), css_class='small-12 medium-6'),
            Column('slug', css_class='small-12 medium-6'),
        )
    ]
    if not parent:
        layout_fields_publish = ['parent']+layout_fields_publish
    
    helper.layout = Layout(
        Fieldset(
            _('Content'),
            'title',
            'content',
        ),
        Fieldset(
            _('Display settings'),
            RowFluid(
                Column('template', css_class='small-12 medium-6'),
                Column('order', css_class='small-12 medium-3'),
                Column('visible', css_class='small-12 medium-3'),
            ),
        ),
        Fieldset(
            _('Publish settings'),
            *layout_fields_publish
        ),
        Fieldset(
            _('History'),
            'comment',
        ),
        ButtonHolder(
            Submit('submit_and_continue', _('Save and continue')),
            Submit('submit', _('Save')),
        ),
    )
    
    return helper

def page_edit_helper(form_tag=True, parent=None):
    return page_helper(form_tag=form_tag, parent=parent, edit_mode=True)


def insert_helper(form_tag=True, edit_mode=False):
    """
    Insert's form layout helper
    """
    helper = FormHelper()
    helper.form_action = '.'
    helper.attrs = {'data_abide': ''}
    helper.form_tag = form_tag
    
    helper.layout = Layout(
        Fieldset(
            _('Content'),
            'title',
            'content',
        ),
        Fieldset(
            _('Display settings'),
            RowFluid(
                Column('slug', css_class='small-12 medium-9'),
                Column('visible', css_class='small-12 medium-3'),
            ),
        ),
        ButtonHolder(
            Submit('submit_and_continue', _('Save and continue')),
            Submit('submit', _('Save')),
        ),
    )
    
    return helper

def insert_edit_helper(form_tag=True):
    return insert_helper(form_tag=form_tag, edit_mode=True)


def attachment_helper(form_tag=True, edit_mode=False):
    """
    Attachment's form layout helper
    """
    helper = FormHelper()
    helper.form_action = '.'
    helper.attrs = {'data_abide': ''}
    helper.form_tag = form_tag
    
    helper.layout = Layout(
        RowFluid(
            Column('title', css_class='small-12 medium-4'),
            Column('slug', css_class='small-12 medium-4'),
            Column('file', css_class='small-12 medium-4'),
        ),
        ButtonHolder(
            Submit('submit', _('Save')),
        ),
    )
    
    return helper

def attachment_edit_helper(form_tag=True):
    return attachment_helper(form_tag=form_tag, edit_mode=True)
