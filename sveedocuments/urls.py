# -*- coding: utf-8 -*-
"""
Root url's map for application
"""
from django.conf.urls import *

from sveedocuments.views.page import (HelpPageView, PageIndexView, PageDetailsView, 
                                        PageSourceView, PagePDFView)

urlpatterns = patterns('',
    url(r'^$', PageIndexView.as_view(), name='index'),
    
    (r'^board/', include('sveedocuments.urls_board')),
    
    url(r'^sitemap/$', PageIndexView.as_view(), name='index'),
    url(r'^help/$', HelpPageView.as_view(), name='help'),
    
    url(r'^(?P<slug>[-\w]+)/$', PageDetailsView.as_view(), name='page-details'),
    url(r'^(?P<slug>[-\w]+)/source/$', PageSourceView.as_view(), name='page-source'),
)

if not getattr(PagePDFView, 'is_dummy', False):
    urlpatterns += patterns('',
        url(r'^(?P<slug>[-\w]+)/pdf/$', PagePDFView.as_view(), name='page-pdf'),
    )
