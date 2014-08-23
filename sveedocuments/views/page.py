# -*- coding: utf-8 -*-
"""
Page document views
"""
import json, os
from datetime import datetime
from cStringIO import StringIO

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views import generic
from django.views.generic.detail import SingleObjectMixin

from braces.views import LoginRequiredMixin, PermissionRequiredMixin

from djangocodemirror.views import SampleQuicksaveMixin

from rstview.parser import SourceParser

from sveedocuments import local_settings
from sveedocuments.models import Page, Attachment
from sveedocuments.forms.page import PageForm, PageEditForm, PageQuickForm
from sveedocuments.forms.attachment import AttachmentForm
from sveedocuments.utils.objects import get_instance_children
from sveedocuments.utils.braces_addons import DetailListAppendView, DirectDeleteView, DownloadMixin

class PageIndexView(generic.TemplateView):
    """
    Pages index
    """
    template_name = "sveedocuments/index.html"
    
    def get(self, request, *args, **kwargs):
        context = {'page_list' : Page.objects.filter(visible=True)}
        return self.render_to_response(context)

class HelpPageView(generic.TemplateView):
    """
    Help document
    """
    template_name = "sveedocuments/help.html"
    
    def get(self, request, *args, **kwargs):
        path_root = os.path.abspath(os.path.dirname(local_settings.__file__))
        f = open(os.path.join(path_root, "HELP.rst"))
        content = f.read()
        f.close()
        
        context = {'content' : SourceParser(content, silent=False)}
        return self.render_to_response(context)

class PageDetailsView(generic.DetailView):
    """
    *Page* view
    """
    model = Page
    context_object_name = "page_instance"
    template_name = "sveedocuments/page_details/page_default.html"
    
    def get_object(self, *args, **kwargs):
        """
        Memorize object to avoid multiple database access when using ``get_object()`` 
        method
        """
        cache_key = "_cache_get_object"
        if not hasattr(self, cache_key):
            setattr(self, cache_key, super(PageDetailsView, self).get_object(*args, **kwargs))
        return getattr(self, cache_key)
    
    def get(self, request, **kwargs):
        # Check if the object is ``visible``
        if not self.get_object().visible:
            raise Http404
        return super(PageDetailsView, self).get(request, **kwargs)
    
    def get_template_names(self):
        return [self.object.get_template()]

class PageSourceView(PageDetailsView):
    """
    Raw content *Page* view
    """
    def get(self, request, *args, **kwargs):
        # Check if the object is ``visible``
        if not self.get_object().visible:
            raise Http404
        return HttpResponse(self.get_object().content, content_type="text/plain; charset=utf-8")

class PageCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    """
    Form view to create a *Page* document
    """
    model = Page
    context_object_name = "page_instance"
    template_name = "sveedocuments/board/page_form.html"
    form_class = PageForm
    permission_required = "sveedocuments.add_page"
    raise_exception = True
    _redirect_to_self = False

    def get(self, request, *args, **kwargs):
        self.parent_page_instance = self._get_parent(**kwargs)
        return super(PageCreateView, self).get(request, *args, **kwargs)
        
    def post(self, request, *args, **kwargs):
        self.parent_page_instance = self._get_parent(**kwargs)
        # Mark to go back to the form page after save, triggered by special submit
        if request.POST:
            if request.POST.get('submit_and_continue', False):
                self._redirect_to_self = True
        return super(PageCreateView, self).post(request, *args, **kwargs)
        
    def get_success_url(self):
        if self._redirect_to_self:
            return reverse('sveedocuments:page-edit', args=[self.object.slug])
        return reverse('sveedocuments:page-index')

    def _get_parent(self, **kwargs):
        if 'slug' in kwargs:
            return get_object_or_404(Page, slug=kwargs['slug'])
        return None
        
    def get_context_data(self, **kwargs):
        context = super(PageCreateView, self).get_context_data(**kwargs)
        context.update({
            'parent_page_instance': self.parent_page_instance,
        })
        return context
    
    def get_form_kwargs(self):
        kwargs = super(PageCreateView, self).get_form_kwargs()
        kwargs.update({
            'author': self.request.user,
            'parent': self.parent_page_instance,
            'initial': {'published': datetime.today()},
        })
        return kwargs

class PageTabsContentMixin(object):
    def get_context_data(self, **kwargs):
        context = super(PageTabsContentMixin, self).get_context_data(**kwargs)
        # Little trick to work with SingleObjectMixin and DetailListAppendView
        if hasattr(self, 'parent_object'):
            obj = self.parent_object
        else:
            obj = self.object
        
        context.update({
            'revisions_count': obj.revision.all().count()+1,
            'files_count': obj.attachment.all().count(),
        })
        return context

class PageEditView(LoginRequiredMixin, PermissionRequiredMixin, PageTabsContentMixin, generic.UpdateView):
    """
    Form view to edit a *Page* document
    """
    model = Page
    context_object_name = "page_instance"
    template_name = "sveedocuments/board/page_form.html"
    form_class = PageEditForm
    permission_required = "sveedocuments.change_page"
    raise_exception = True
    _redirect_to_self = False
        
    def post(self, request, *args, **kwargs):
        # Mark to go back to the form page after save, triggered by special submit
        if request.POST:
            if request.POST.get('submit_and_continue', False):
                self._redirect_to_self = True
        return super(PageEditView, self).post(request, *args, **kwargs)
    
    def get_object(self, *args, **kwargs):
        """
        Forcing a new empty comment field in edit mode
        """
        obj = super(PageEditView, self).get_object(*args, **kwargs)
        obj.comment = ''
        return obj

    def get_success_url(self):
        if self._redirect_to_self:
            return reverse('sveedocuments:page-edit', args=[self.object.slug])
        return reverse('sveedocuments:page-index')

    def get_form_kwargs(self):
        kwargs = super(PageEditView, self).get_form_kwargs()
        kwargs.update({'author': self.request.user})
        return kwargs


class PageHistoryView(LoginRequiredMixin, PermissionRequiredMixin, PageTabsContentMixin, generic.DetailView):
    """
    *Page* history
    """
    model = Page
    context_object_name = "page_instance"
    template_name = "sveedocuments/board/page_history.html"
    permission_required = "sveedocuments.change_page"
    raise_exception = True
    
    def get_object(self, *args, **kwargs):
        """
        Memorize object to avoid multiple database access when using ``get_object()`` 
        method
        """
        cache_key = "_cache_get_object"
        if not hasattr(self, cache_key):
            setattr(self, cache_key, super(PageHistoryView, self).get_object(*args, **kwargs))
        return getattr(self, cache_key)
        
    def get_context_data(self, **kwargs):
        context = super(PageHistoryView, self).get_context_data(**kwargs)
        context.update({
            'last_revisions': self.object.revision.all().order_by('-created'),
        })
        return context


class PageAttachmentsView(LoginRequiredMixin, PermissionRequiredMixin, PageTabsContentMixin, DetailListAppendView):
    """
    Form view to add file attachments to a Page
    """
    model = Attachment
    form_class = AttachmentForm
    template_name = "sveedocuments/board/page_attachments.html"
    permission_required = "sveedocuments.change_page"
    raise_exception = True
    context_parent_object_name = 'page_instance'
    
    def get_parent_object(self):
        return get_object_or_404(Page, slug=self.kwargs['slug'])
    
    def get_queryset(self):
        return self.parent_object.attachment.all()

    def get_success_url(self):
        return reverse('sveedocuments:page-attachments', args=[self.parent_object.slug])

    def get_form_kwargs(self):
        kwargs = super(PageAttachmentsView, self).get_form_kwargs()
        kwargs.update({'author': self.request.user})
        return kwargs


class PageAttachmentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DirectDeleteView):
    """
    View to delete a *Page* document
    """
    model = Attachment
    permission_required = "sveedocuments.delete_attachment"
    raise_exception = True
    memoize_old_object = True
    _memoized_attr = ['id', 'slug', 'title', 'page']

    def get_success_url(self):
        return reverse('sveedocuments:page-attachments', args=[self.old_object['page'].slug])

class PageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    """
    Form view to delete a *Page* document
    
    This display a tree of relations to confirm the object and relations deletion
    """
    model = Page
    context_object_name = "page_instance"
    template_name = "sveedocuments/board/page_delete.html"
    permission_required = "sveedocuments.delete_page"
    raise_exception = True

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context.update({'relations': get_instance_children(self.object)})
        return self.render_to_response(context)

    def get_success_url(self):
        # On success, force mptt tree rebuild to avoid which seems a bug that will cause 
        # recursetree templatetag to raise an exception
        Page.tree.rebuild()
        # DEPRECATED: Implicit manager Page.tree will be removed in django-mptt 0.6.
        # Explicitly define a TreeManager() on your model to remove this warning.
        
        # Then redirect
        return reverse('sveedocuments:page-index')

class PageQuicksaveView(SampleQuicksaveMixin, PageEditView):
    """
    Quicksave view for a *Page* content
    """
    form_class = PageQuickForm
    
    def get_object(self, queryset=None):
        if self.request.POST.get('slug', False):
            self.kwargs['slug'] = self.request.POST['slug']
        return super(PageQuicksaveView, self).get_object(queryset=queryset)

# Optional view for PDF export need RstToPdf
try:
    from rst2pdf.createpdf import RstToPdf
except ImportError:
    class PagePDFView(object):
        """Dummy object"""
        is_dummy = True
else:
    class PagePDFView(SingleObjectMixin, DownloadMixin, generic.View):
        """
        Export a Page as a PDF file
        """
        model = Page
        content_type = 'application/pdf'
        filename_format = "{slug}_{timestamp}.pdf"
        
        def get_context_data(self, **kwargs):
            context = super(PagePDFView, self).get_context_data(**kwargs)
            context.update({
                'slug': self.object.slug,
                'timestamp': self.get_filename_timestamp(),
            })
            return context
        
        def get_filename(self, context):
            return self.filename_format.format(**context)
        
        def get_content(self, context):
            """
            Build the PDF from the page content with RstToPdf
            """
            # Add the optional preface and then the page content
            content = ''
            if getattr(local_settings, 'DOCUMENTS_EXPORT_PDF_PREFACE', None) is not None:
                content += local_settings.DOCUMENTS_EXPORT_PDF_PREFACE.format(page=self.object)
            content += self.object.content
            
            buffer_response = StringIO()
            # TODO: Can't we simply pass a dict kwargs to "RstToPdf" so all available 
            #       options could be setted from the settings ?
            RstToPdf(language=settings.LANGUAGE_CODE, breakside='any', header=local_settings.DOCUMENTS_EXPORT_PDF_HEADER, footer=local_settings.DOCUMENTS_EXPORT_PDF_FOOTER).createPdf(text=content, output=buffer_response)
            pdf = buffer_response.getvalue()
            buffer_response.close()
            
            return pdf

        def get(self, request, *args, **kwargs):
            self.object = self.get_object()
            context = self.get_context_data(**kwargs)
            return super(PagePDFView, self).render_to_response(context)
