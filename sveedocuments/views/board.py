# -*- coding: utf-8 -*-
"""
Board views
"""
from django.views import generic

from djangocodemirror.views import SamplePreviewView, EditorSettingsView

from sveedocuments.models import Page, Insert

from braces.views import LoginRequiredMixin

class BoardIndexView(LoginRequiredMixin, generic.TemplateView):
    """
    Documents management board
    """
    template_name = "sveedocuments/board.html"

    def get(self, request, *args, **kwargs):
        context = {
            'page_list' : Page.objects.filter(),
            'insert_list' : Insert.objects.filter().order_by('slug'),
        }
        return self.render_to_response(context)

class PreviewView(LoginRequiredMixin, SamplePreviewView):
    """
    Page preview for a *Page* content
    """
    pass

class BoardEditorSettingsView(LoginRequiredMixin, EditorSettingsView):
    """
    Page form for djangocode-mirror editor settings
    """
    pass
