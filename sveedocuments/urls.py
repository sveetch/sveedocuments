# -*- coding: utf-8 -*-
"""
Root url's map for application
"""
from django.conf.urls import *

from sveedocuments.views.page import (HelpPageView, PageIndexView, PageDetailsView, 
                                        PageSourceView, PagePDFView)

urlpatterns = patterns('',
    url(r'^$', PageIndexView.as_view(), name='documents-index'),
    
    (r'^board/', include('sveedocuments.urls_board')),
    
    url(r'^sitemap/$', PageIndexView.as_view(), name='documents-index'),
    url(r'^documents-help/$', HelpPageView.as_view(), name='documents-help'),
    
    url(r'^(?P<slug>[-\w]+)/$', PageDetailsView.as_view(), name='documents-page-details'),
    url(r'^(?P<slug>[-\w]+)/source/$', PageSourceView.as_view(), name='documents-page-source'),
)

if not getattr(PagePDFView, 'is_dummy', False):
    urlpatterns += patterns('',
        url(r'^(?P<slug>[-\w]+)/pdf/$', PagePDFView.as_view(), name='documents-page-pdf'),
    )
