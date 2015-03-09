# -*- coding: utf-8 -*-
"""
Page document views
"""
import json, os

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.views import generic

from mptt.templatetags.mptt_tags import cache_tree_children

from braces.views import LoginRequiredMixin

from rstview.parser import SourceParser

from sveedocuments import models
from sveedocuments.utils.braces_addons import DownloadMixin

class PageIndexMixin(object):
    """
    Pages sitemap
    """
    template_name = "sveedocuments/index.html"
    
    def get(self, request, *args, **kwargs):
        # We can't force queryset evaluation here else it will mess the tree 
        # resolution from mptt
        page_list = models.Page.objects.filter(visible=True)
        
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
                "view_url": reverse('sveedocuments:page-details', args=[n.slug]),
                "children": self.get_recursed_tree(n.get_children())
            })
        return nodes

class HelpPageMixin(object):
    """
    Help document
    """
    template_name = "sveedocuments/help.html"
    
    def get(self, request, *args, **kwargs):
        path_root = os.path.abspath(os.path.dirname(models.__file__))
        f = open(os.path.join(path_root, "HELP.rst"))
        content = f.read()
        f.close()
        
        context = {'content' : SourceParser(content, silent=False)}
        return self.render_to_response(context)


class PageDetailsMixin(object):
    """
    Page view
    """
    model = models.Page
    context_object_name = "page_instance"
    template_name = "sveedocuments/page_details/page_default.html"
    
    def get_object(self, *args, **kwargs):
        """
        Memorize object to avoid multiple database access when using ``get_object()`` 
        method
        """
        cache_key = "_cache_get_object"
        if not hasattr(self, cache_key):
            setattr(self, cache_key, super(PageDetailsMixin, self).get_object(*args, **kwargs))
        return getattr(self, cache_key)
    
    def get_attachments(self):
        return self.object.attachment.all()
        
    def get_context_data(self, **kwargs):
        context = super(PageDetailsMixin, self).get_context_data(**kwargs)
        context.update({
            'attachments': self.get_attachments(),
            'ATTACHMENTS_WITH_SENDFILE': models.ATTACHMENTS_WITH_SENDFILE,
        })
        return context
    
    def get(self, request, **kwargs):
        # Check if the object is ``visible``
        if not self.get_object().visible:
            raise Http404
        return super(PageDetailsMixin, self).get(request, **kwargs)
    
    def get_template_names(self):
        return [self.object.get_template()]


# Bind views from restricted mode
if settings.DOCUMENTS_PAGE_RESTRICTED:
    class PageIndexView(PageIndexMixin, LoginRequiredMixin, generic.TemplateView):
        pass
    class PageDetailsView(PageDetailsMixin, LoginRequiredMixin, generic.DetailView):
        pass
    class HelpPageView(HelpPageMixin, LoginRequiredMixin, generic.TemplateView):
        pass
else:
    class PageIndexView(PageIndexMixin, generic.TemplateView):
        pass
    class PageDetailsView(PageDetailsMixin, generic.DetailView):
        pass
    class HelpPageView(HelpPageMixin, generic.TemplateView):
        pass


class PageSourceView(PageDetailsView):
    """
    Raw content Page view
    """
    def get(self, request, *args, **kwargs):
        # Check if the object is ``visible``
        if not self.get_object().visible:
            raise Http404
        return HttpResponse(self.get_object().content, content_type="text/plain; charset=utf-8")
