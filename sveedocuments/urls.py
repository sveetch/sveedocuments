# -*- coding: utf-8 -*-
"""
Root url's map for application
"""
from django.conf.urls import *

from sveedocuments.models import ATTACHMENTS_WITH_SENDFILE
from sveedocuments.views.page import (
    HelpPageView, PageIndexView, PageDetailsView, 
    PageSourceView
)

urlpatterns = patterns('',
    url(r'^$', PageIndexView.as_view(), name='index'),
    
    (r'^board/', include('sveedocuments.urls_board')),
    
    url(r'^help/$', HelpPageView.as_view(), name='help'),
    
    url(r'^(?P<slug>[-\w]+)/$', PageDetailsView.as_view(), name='page-details'),
    url(r'^(?P<slug>[-\w]+)/source/$', PageSourceView.as_view(), name='page-source'),
)

if ATTACHMENTS_WITH_SENDFILE:
    from sveedocuments.views.attachment import AttachmentProtectedDownloadView
    urlpatterns += patterns('',
        url(r'^(?P<slug>[-\w]+)/attachment/(?P<attachment_id>\d+)/$', AttachmentProtectedDownloadView.as_view(), name='page-attachment-download'),
    )
