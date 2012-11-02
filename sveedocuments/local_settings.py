# -*- coding: utf-8 -*-
"""
App default settings
"""
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

# Add custom cache keys to delete with the command option ``django-admin documents --clearcache``
DOCUMENTS_CACHE_KEYS_TO_CLEAN = getattr(settings, 'DOCUMENTS_CACHE_KEYS_TO_CLEAN', [])

# Forbidden words for slug values in documents
DOCUMENTS_PAGE_RESERVED_SLUGS = getattr(settings, 'DOCUMENTS_PAGE_MENU', ('board','add','preview','documents-help','inserts'))

# Default template to generate tree menu
DOCUMENTS_PAGE_TREEMENU = getattr(settings, 'DOCUMENTS_PAGE_TREEMENU', "sveedocuments/page_treemenu.html")
# Default template to generate flat menu
DOCUMENTS_PAGE_FLATMENU = getattr(settings, 'DOCUMENTS_PAGE_FLATMENU', "sveedocuments/page_flatmenu.html")

# Available templates for Pages
DOCUMENTS_PAGE_TEMPLATES = {
    'elastic': ('sveedocuments/page_details/elastic.html', _('Elastic with an unique column')),
    'elastic_with_columns': ('sveedocuments/page_details/elastic_with_columns.html', _('Elastic with two columns')),
    'fixed_absolute': ('sveedocuments/page_details/fixed_absolute.html', _('Absolute fixed with an unique column')),
    'fixed_absolute_with_columns': ('sveedocuments/page_details/fixed_absolute_with_columns.html', _('Absolute fixed with two columns')),
    'fixed_relative': ('sveedocuments/page_details/fixed_relative.html', _('Relative fixed an unique column')),
    'fixed_relative_with_columns': ('sveedocuments/page_details/fixed_relative_with_columns.html', _('Relative fixed with two columns')),
}
DOCUMENTS_PAGE_TEMPLATES.update(getattr(settings, 'DOCUMENTS_PAGE_TEMPLATES', {}))

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
        'preview_url': ('documents-preview',),
        'quicksave_url': ('documents-page-quicksave',),
        'quicksave_datas': 'DJANGOCODEMIRROR_OBJECT',
        'lineWrapping': False,
        'lineNumbers': True,
        'search_enabled': True,
        #'settings_cookie': DJANGOCODEMIRROR_USER_SETTINGS_COOKIE_NAME,
        'help_link': ('documents-help',),
        'settings_url': ('documents-editor-settings', [], {}),
    },
    'sveetchies-documents-insert': {
        'mode': 'rst',
        'csrf': 'CSRFpass',
        'preview_url': ('documents-preview',),
        'quicksave_url': ('documents-insert-quicksave',),
        'quicksave_datas': 'DJANGOCODEMIRROR_OBJECT',
        'lineWrapping': False,
        'lineNumbers': True,
        'search_enabled': True,
        #'settings_cookie': DJANGOCODEMIRROR_USER_SETTINGS_COOKIE_NAME,
        'help_link': ('documents-help',),
        'settings_url': ('documents-editor-settings', [], {}),
    },
}

"""
Internal settings only, can't be modified from your webapp settings
"""

# Cache keys for document elements
PAGE_RENDER_CACHE_KEY_NAME = 'documents-render-page_{id}-setting_{setting}'
INSERT_RENDER_CACHE_KEY_NAME = 'documents-render-insert_{id}-setting_{setting}-hlv_{header_level}'
PAGE_TOC_CACHE_KEY_NAME = 'documents-toc-page_{id}-setting_{setting}'
INSERT_TOC_CACHE_KEY_NAME = 'documents-toc-insert_{id}-setting_{setting}-hlv_{header_level}'
PAGE_SLUGS_CACHE_KEY_NAME = 'documents-page_slugs'
