# -*- coding: utf-8 -*-
"""
Board views
"""
import json

from django.views import generic
from django.core.urlresolvers import reverse

from mptt.templatetags.mptt_tags import cache_tree_children

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

    #def get(self, request, *args, **kwargs):
        #context = {
            #'page_list' : Page.objects.filter(),
        #}
        #return self.render_to_response(context)
    
    def get(self, request, *args, **kwargs):
        # We can't force queryset evaluation here else it will mess the tree 
        # resolution from mptt
        page_list = Page.objects.all()
        
        context = {
            'page_list': page_list,
            'json_tree': [],
        }
        
        # Fill the JSON tree if there is at least one entry
        if page_list.count()>0:
            context['json_tree'] = json.dumps(self.get_recursed_tree( cache_tree_children(page_list) ))
            
        return self.render_to_response(context)
    
    def get_recursed_tree(self, root_nodes):
        """
        Get the recursed tree from the queryset
        """
        nodes = []
        for n in root_nodes:
            nodes.append({
                "id": n.pk,
                "label": n.title,
                "slug": n.slug,
                "visible": n.visible,
                "view_url": reverse('sveedocuments:page-details', args=[n.slug]),
                "edit_url": reverse('sveedocuments:page-edit', args=[n.slug]),
                "add_child_url": reverse('sveedocuments:page-add-child', args=[n.slug]),
                "delete_url": reverse('sveedocuments:page-delete', args=[n.slug]),
                "children": self.get_recursed_tree(n.get_children())
            })
        return nodes


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
