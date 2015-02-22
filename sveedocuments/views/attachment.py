# -*- coding: utf-8 -*-
"""
Attachment views
"""
import os

from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views import generic

from sendfile import sendfile

from braces.views import LoginRequiredMixin

from sveedocuments.models import Attachment
from sveedocuments.views.page import PageDetailsMixin

class AttachmentProtectedDownloadView(PageDetailsMixin, LoginRequiredMixin, generic.DetailView):
    """
    View to download protected attachment
    """
    def get_attachment(self):
        return get_object_or_404(Attachment, page=self.object, pk=self.kwargs['attachment_id'])
    
    def get(self, request, **kwargs):
        self.object = self.get_object()
        self.attachment = self.get_attachment()
        
        # If page is not visible, their attachments are not available to download
        if not self.object.visible:
            raise Http404
        
        file_path = os.path.join(settings.PROJECT_PATH, self.attachment.file.path)
        return sendfile(request, file_path, attachment=True, attachment_filename=os.path.basename(file_path))
