# -*- coding: utf-8 -*-
"""
Url's map for documents board
"""
from django.conf.urls.defaults import *

from sveedocuments.views.board import BoardIndexView, PreviewView, BoardEditorSettingsView
from sveedocuments.views.page import (PageCreateView, PageQuicksaveView,
                                      PageEditView, PageDeleteView, PageDeleteView)
from sveedocuments.views.insert import (InsertCreateView, InsertEditView, 
                                        InsertDeleteView, InsertQuicksaveView)

urlpatterns = patterns('',
    url(r'^$', BoardIndexView.as_view(), name='documents-board'),
    
    url(r'^add/$', PageCreateView.as_view(), name='documents-page-add'),
    
    url(r'^preview/$', PreviewView.as_view(), name='documents-preview'),
    url(r'^editor_settings/$', BoardEditorSettingsView.as_view(), name='documents-editor-settings'),
    
    url(r'^quicksave/page/$', PageQuicksaveView.as_view(), name='documents-page-quicksave'),
    url(r'^quicksave/insert/$', InsertQuicksaveView.as_view(), name='documents-insert-quicksave'),
    
    url(r'^inserts/add/$', InsertCreateView.as_view(), name='documents-insert-add'),
    url(r'^inserts/(?P<slug>[-\w]+)/delete/$', InsertDeleteView.as_view(), name='documents-insert-delete'),
    url(r'^inserts/(?P<slug>[-\w]+)/edit/$', InsertEditView.as_view(), name='documents-insert-edit'),
    
    url(r'^(?P<slug>[-\w]+)/add/$', PageCreateView.as_view(), name='documents-page-add-child'),
    url(r'^(?P<slug>[-\w]+)/delete/$', PageDeleteView.as_view(), name='documents-page-delete'),
    url(r'^(?P<slug>[-\w]+)/edit/$', PageEditView.as_view(), name='documents-page-edit'),
)
