# -*- coding: utf-8 -*-
"""
Root url's map for application
"""
from django.conf.urls.defaults import *

from sveedocuments.views.page import HelpPage, PageIndex, PageDetails, PageSource

urlpatterns = patterns('',
    url(r'^$', PageIndex.as_view(), name='documents-index'),
    
    (r'^board/', include('sveedocuments.urls_board')),
    
    url(r'^sitemap/$', PageIndex.as_view(), name='documents-index'),
    url(r'^documents-help/$', HelpPage.as_view(), name='documents-help'),
    
    url(r'^(?P<slug>[-\w]+)/$', PageDetails.as_view(), name='documents-page-details'),
    url(r'^(?P<slug>[-\w]+)/source/$', PageSource.as_view(), name='documents-page-source'),
)
