# -*- coding: utf-8 -*-
"""
App default settings
"""
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

# Add custom cache keys to delete with the command option ``django-admin documents --clearcache``
DOCUMENTS_CACHE_KEYS_TO_CLEAN = getattr(settings, 'DOCUMENTS_CACHE_KEYS_TO_CLEAN', [])

# Forbidden words for slug values in documents
DOCUMENTS_PAGE_RESERVED_SLUGS = getattr(settings, 'DOCUMENTS_PAGE_MENU', ('add','board','help','inserts','preview','sitemap'))

# Default template to generate tree menu
DOCUMENTS_PAGE_TREEMENU = getattr(settings, 'DOCUMENTS_PAGE_TREEMENU', "sveedocuments/menu_tree.html")
# Default template to generate flat menu
DOCUMENTS_PAGE_FLATMENU = getattr(settings, 'DOCUMENTS_PAGE_FLATMENU', "sveedocuments/menu_flat.html")

# Enable or disable Pages archiving
DOCUMENTS_PAGE_ARCHIVED = True

# Available templates for Pages
DOCUMENTS_PAGE_TEMPLATES = {
    'default': ('sveedocuments/page_details/page_default.html', _('Default template with document content only')),
    'with_toc': ('sveedocuments/page_details/page_with-toc.html', _('Template with a Table Of Content and the document content')),
}
DOCUMENTS_PAGE_TEMPLATES.update(getattr(settings, 'DOCUMENTS_PAGE_TEMPLATES', {}))

DOCUMENTS_PAGE_TEMPLATE_DEFAULT = getattr(settings, 'DOCUMENTS_PAGE_TEMPLATE_DEFAULT', 'elastic')

# Active a silent reporter to avoid warnings about missing page on role ``:page:xxx``
# If ``True`` the role will be transformed to link despite the page does not exist, 
# if ``False`` the warning will be inserted in the render
DOCUMENTS_PARSER_WIKIROLE_SILENT_WARNING = getattr(settings, 'DOCUMENTS_PARSER_WIKIROLE_SILENT_WARNING', False)

"""
Sample settings, you have to put them yourself in your webapp settings
"""

# Additional Django-CodeMirror settings for sveedocuments
CODEMIRROR_SETTINGS = {
    'sveetchies-documents-page': {
        'mode': 'rst',
        'csrf': 'CSRFpass',
        'preview_url': ('sveedocuments:preview',),
        #'quicksave_url': ('sveedocuments:page-quicksave',),
        #'quicksave_datas': 'DJANGOCODEMIRROR_OBJECT',
        'quicksave_url': None,
        'lineWrapping': False,
        'lineNumbers': True,
        'search_enabled': True,
        #'settings_cookie': DJANGOCODEMIRROR_USER_SETTINGS_COOKIE_NAME,
        'help_link': ('sveedocuments:help',),
        'settings_url': ('sveedocuments:editor-settings', [], {}),
    },
    'sveetchies-documents-insert': {
        'mode': 'rst',
        'csrf': 'CSRFpass',
        'preview_url': ('sveedocuments:preview',),
        #'quicksave_url': ('sveedocuments:insert-quicksave',),
        #'quicksave_datas': 'DJANGOCODEMIRROR_OBJECT',
        'quicksave_url': None,
        'lineWrapping': False,
        'lineNumbers': True,
        'search_enabled': True,
        #'settings_cookie': DJANGOCODEMIRROR_USER_SETTINGS_COOKIE_NAME,
        'help_link': ('sveedocuments:help',),
        'settings_url': ('sveedocuments:editor-settings', [], {}),
    },
}

# This is the preface that will be added at start of the Page content when they are 
# exported to PDF
# The default preface put some document informations, add summary of content on the 
# first page and active the section numbering.
_PDF_PREFACE = u"""==================
{page.title}
==================

:author: {page.author.first_name} {page.author.last_name} <{page.author.email}>
:date: {page.modified}
:revision: $LastChangedRevision: {page.current_revision} $

.. class:: alert alert-info pull-right

.. contents::

.. section-numbering::

.. raw:: pdf

   PageBreak oneColumn

"""
DOCUMENTS_EXPORT_PDF_PREFACE = getattr(settings, 'DOCUMENTS_EXPORT_PDF_PREFACE', _PDF_PREFACE)
DOCUMENTS_EXPORT_PDF_HEADER = getattr(settings, 'DOCUMENTS_EXPORT_PDF_PREFACE', "###Section###")
DOCUMENTS_EXPORT_PDF_FOOTER = getattr(settings, 'DOCUMENTS_EXPORT_PDF_PREFACE', "Page ###Page### / ###Total###")

"""
Internal settings only, can't be overriden from your webapp settings
"""

# Cache keys for document elements
PAGE_RENDER_CACHE_KEY_NAME = 'documents-render-page_{id}-setting_{setting}'
PAGEREV_RENDER_CACHE_KEY_NAME = 'documents-render-page-revision_{id}-setting_{setting}'
INSERT_RENDER_CACHE_KEY_NAME = 'documents-render-insert_{id}-setting_{setting}-hlv_{header_level}'
PAGE_TOC_CACHE_KEY_NAME = 'documents-toc-page_{id}-setting_{setting}'
PAGEREV_TOC_CACHE_KEY_NAME = 'documents-toc-page-revision_{id}-setting_{setting}'
INSERT_TOC_CACHE_KEY_NAME = 'documents-toc-insert_{id}-setting_{setting}-hlv_{header_level}'
PAGE_SLUGS_CACHE_KEY_NAME = 'documents-page_slugs'
PAGE_ATTACHMENTS_SLUGS_CACHE_KEY_NAME = 'documents-page-attachments-slugs'
