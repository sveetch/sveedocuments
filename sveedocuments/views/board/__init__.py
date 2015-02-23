# -*- coding: utf-8 -*-
"""
Board views
"""
from django.views import generic

from djangocodemirror.views import SamplePreviewView, EditorSettingsView

from sveedocuments.models import Page, Insert
from sveedocuments.forms.page import DjangoCodeMirrorSettingsForm

from braces.views import LoginRequiredMixin, PermissionRequiredMixin

class BoardIndexView(LoginRequiredMixin, generic.TemplateView):
    """
    Documents management board
    """
    template_name = "sveedocuments/board/index.html"

    def get(self, request, *args, **kwargs):
        context = {
            'page_count' : Page.objects.count(),
            'page_hidden_count' : Page.objects.filter(visible=False).count(),
            'page_last_revised': Page.objects.all().order_by('-modified')[0:5],
            'insert_count' : Insert.objects.count(),
            'insert_hidden_count' : Insert.objects.filter(visible=False).count(),
        }
        return self.render_to_response(context)

class BoardPagesIndexView(LoginRequiredMixin, generic.TemplateView):
    """
    Board pages index
    """
    template_name = "sveedocuments/board/page_index.html"

    def get(self, request, *args, **kwargs):
        context = {
            'page_list' : Page.objects.filter(),
        }
        return self.render_to_response(context)

class BoardInsertsIndexView(LoginRequiredMixin, generic.TemplateView):
    """
    Board inserts index
    """
    template_name = "sveedocuments/board/insert_index.html"

    def get(self, request, *args, **kwargs):
        context = {
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
    form_class = DjangoCodeMirrorSettingsForm
