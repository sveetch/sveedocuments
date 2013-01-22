# -*- coding: utf-8 -*-
"""
Url's map for documents board
"""
from django.conf.urls.defaults import *

from sveedocuments.views.board import (BoardIndexView, PreviewView, BoardEditorSettingsView,
                                        BoardPagesIndexView, BoardInsertsIndexView)
from sveedocuments.views.page import (PageCreateView, PageQuicksaveView,
                                      PageEditView, PageDeleteView, PageDeleteView, PageHistoryView, 
                                      PageAttachmentsView, PageAttachmentDeleteView)
from sveedocuments.views.insert import (InsertCreateView, InsertEditView, 
                                        InsertDeleteView, InsertQuicksaveView)

urlpatterns = patterns('',
    url(r'^$', BoardIndexView.as_view(), name='documents-board'),
    
    url(r'^preview/$', PreviewView.as_view(), name='documents-preview'),
    url(r'^editor_settings/$', BoardEditorSettingsView.as_view(), name='documents-editor-settings'),
    
    url(r'^quicksave/page/$', PageQuicksaveView.as_view(), name='documents-page-quicksave'),
    url(r'^quicksave/insert/$', InsertQuicksaveView.as_view(), name='documents-insert-quicksave'),
    
    url(r'^pages/$', BoardPagesIndexView.as_view(), name='documents-page-index'),
    url(r'^pages/add/$', PageCreateView.as_view(), name='documents-page-add'),
    url(r'^pages/(?P<slug>[-\w]+)/add/$', PageCreateView.as_view(), name='documents-page-add-child'),
    url(r'^pages/(?P<slug>[-\w]+)/delete/$', PageDeleteView.as_view(), name='documents-page-delete'),
    url(r'^pages/(?P<slug>[-\w]+)/edit/$', PageEditView.as_view(), name='documents-page-edit'),
    url(r'^pages/(?P<slug>[-\w]+)/edit/history/$', PageHistoryView.as_view(), name='documents-page-history'),
    url(r'^pages/(?P<slug>[-\w]+)/edit/attachments/$', PageAttachmentsView.as_view(), name='documents-page-attachments'),
    url(r'^pages/(?P<slug>[-\w]+)/edit/attachments/(?P<pk>\d+)/delete/$', PageAttachmentDeleteView.as_view(), name='documents-page-attachments-delete'),
    
    url(r'^inserts/$', BoardInsertsIndexView.as_view(), name='documents-insert-index'),
    url(r'^inserts/add/$', InsertCreateView.as_view(), name='documents-insert-add'),
    url(r'^inserts/(?P<slug>[-\w]+)/delete/$', InsertDeleteView.as_view(), name='documents-insert-delete'),
    url(r'^inserts/(?P<slug>[-\w]+)/edit/$', InsertEditView.as_view(), name='documents-insert-edit'),
)
