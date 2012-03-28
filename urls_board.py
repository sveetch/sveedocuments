# -*- coding: utf-8 -*-
"""
Url's map for documents board
"""
from django.conf.urls.defaults import *

from sveedocuments.views.board import BoardIndex
from sveedocuments.views.page import (PagePreview, PageCreate, PageQuicksave,
                                                    PageEdit, PageDelete, PageDelete)
from sveedocuments.views.insert import (InsertCreate, InsertEdit, InsertDelete,
                                                      InsertQuicksave)

urlpatterns = patterns('',
    url(r'^$', BoardIndex.as_view(), name='documents-board'),
    
    url(r'^add/$', PageCreate.as_view(), name='documents-page-add'),
    
    url(r'^preview/$', PagePreview.as_view(), name='documents-preview'),
    
    url(r'^quicksave/page/$', PageQuicksave.as_view(), name='documents-page-quicksave'),
    url(r'^quicksave/insert/$', InsertQuicksave.as_view(), name='documents-insert-quicksave'),
    
    url(r'^inserts/add/$', InsertCreate.as_view(), name='documents-insert-add'),
    url(r'^inserts/(?P<slug>[-\w]+)/delete/$', InsertDelete.as_view(), name='documents-insert-delete'),
    url(r'^inserts/(?P<slug>[-\w]+)/edit/$', InsertEdit.as_view(), name='documents-insert-edit'),
    
    url(r'^(?P<slug>[-\w]+)/add/$', PageCreate.as_view(), name='documents-page-add-child'),
    url(r'^(?P<slug>[-\w]+)/delete/$', PageDelete.as_view(), name='documents-page-delete'),
    url(r'^(?P<slug>[-\w]+)/edit/$', PageEdit.as_view(), name='documents-page-edit'),
)
