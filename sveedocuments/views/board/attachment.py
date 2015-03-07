# -*- coding: utf-8 -*-
"""
Page's attachments management views
"""
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views import generic
from django.contrib import messages
from django.utils.translation import ugettext as _

from braces.views import PermissionRequiredMixin

from sveedocuments.models import ATTACHMENTS_WITH_SENDFILE, Page, Attachment
from sveedocuments.forms.attachment import AttachmentForm
from sveedocuments.views.board.page import PageTabsContentMixin
from sveedocuments.utils.braces_addons import DetailListAppendView, DirectDeleteView

class PageAttachmentsView(PermissionRequiredMixin, PageTabsContentMixin, DetailListAppendView):
    """
    Form view to add file attachments to a Page
    """
    model = Attachment
    form_class = AttachmentForm
    template_name = "sveedocuments/board/page_attachments.html"
    permission_required = 'sveedocuments.change_page'
    raise_exception = True
    context_parent_object_name = 'page_instance'
    
    def get_page_object(self):
        return self.get_parent_object()
    
    def get_parent_object(self):
        return get_object_or_404(Page, slug=self.kwargs['slug'])
    
    def get_queryset(self):
        return self.parent_object.attachment.all()
    
    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, _('Attachment has been added successfully'), fail_silently=True)
        return super(PageAttachmentsView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(PageAttachmentsView, self).get_form_kwargs()
        kwargs.update({'author': self.request.user})
        return kwargs
        
    def get_context_data(self, **kwargs):
        context = super(PageAttachmentsView, self).get_context_data(**kwargs)
        context.update({
            'ATTACHMENTS_WITH_SENDFILE': ATTACHMENTS_WITH_SENDFILE,
        })
        return context

    def get_success_url(self):
        return reverse('sveedocuments:page-attachments', args=[self.parent_object.slug])


class PageAttachmentDeleteView(PermissionRequiredMixin, DirectDeleteView):
    """
    View to delete a *Page* document
    """
    model = Attachment
    permission_required = 'sveedocuments.change_page'
    raise_exception = True
    memoize_old_object = True
    _memoized_attr = ['id', 'slug', 'title', 'page']
    
    def get_page_object(self):
        return get_object_or_404(Page, slug=self.kwargs['slug'])
    
    def get_success_url(self):
        messages.add_message(self.request, messages.WARNING, _('Attachment has been deleted successfully'), fail_silently=True)
        return reverse('sveedocuments:page-attachments', args=[self.old_object['page'].slug])
