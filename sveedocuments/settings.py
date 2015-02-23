# -*- coding: utf-8 -*-
"""
sveedocuments default settings
"""
gettext = lambda s: s

# Forbidden words for slug values in documents
DOCUMENTS_PAGE_RESERVED_SLUGS = ('add','board','help','inserts','preview','sitemap')

# Default template to generate tree menu
DOCUMENTS_PAGE_TREEMENU = "sveedocuments/menu_tree.html"
# Default template to generate flat menu
DOCUMENTS_PAGE_FLATMENU = "sveedocuments/menu_flat.html"

# Enable or disable Pages archiving
DOCUMENTS_PAGE_ARCHIVED = True

# Page view restriction, if True page viewing will require to be authenticated, 
# if False page viewing is free for all
DOCUMENTS_PAGE_RESTRICTED = False

# To enable django-sendfile usage when DOCUMENTS_PAGE_RESTRICTED is True
DOCUMENTS_ATTACHMENT_USE_SENDFILE = True

# Available templates for Pages
DOCUMENTS_PAGE_TEMPLATES = {
    'default': ('sveedocuments/page_details/page_default.html', gettext('Default template with document content only')),
    # Disabled, because TOC extract is buggy
    #'with_toc': ('sveedocuments/page_details/page_with-toc.html', gettext('Template with a Table Of Content and the document content')),
}

DOCUMENTS_PAGE_TEMPLATE_DEFAULT = 'elastic'

# Active a silent reporter to avoid warnings about missing page on role ``:page:xxx``
# If ``True`` the role will be transformed to link despite the page does not exist, 
# if ``False`` the warning will be inserted in the render
DOCUMENTS_PARSER_WIKIROLE_SILENT_WARNING = False

"""
WARNING: Sample additional Django-CodeMirror settings, you have to put them yourself in your project settings
"""
#DJANGOCODEMIRROR_USER_SETTINGS_COOKIE_NAME = "djangocodemirror_user_settings"
#CODEMIRROR_SETTINGS = {
    #'sveetchies-documents-edit-page': {
        #'mode': 'rst',
        #'csrf': 'CSRFpass',
        #'preview_url': ('sveedocuments:preview',),
        #'quicksave_url': ('sveedocuments:page-quicksave',),
        #'quicksave_datas': 'DJANGOCODEMIRROR_OBJECT',
        #'lineWrapping': True,
        #'lineNumbers': True,
        #'search_enabled': True,
        #'settings_cookie': DJANGOCODEMIRROR_USER_SETTINGS_COOKIE_NAME,
        #'help_link': ('sveedocuments:help',),
        #'settings_url': ('sveedocuments:editor-settings', [], {}),
    #},
    #'sveetchies-documents-edit-insert': {
        #'mode': 'rst',
        #'csrf': 'CSRFpass',
        #'preview_url': ('sveedocuments:preview',),
        #'quicksave_url': ('sveedocuments:insert-quicksave',),
        #'quicksave_datas': 'DJANGOCODEMIRROR_OBJECT',
        #'lineWrapping': True,
        #'lineNumbers': True,
        #'search_enabled': True,
        #'settings_cookie': DJANGOCODEMIRROR_USER_SETTINGS_COOKIE_NAME,
        #'help_link': ('sveedocuments:help',),
        #'settings_url': ('sveedocuments:editor-settings', [], {}),
    #},
#}
#CODEMIRROR_SETTINGS['sveetchies-documents-add-page'] = CODEMIRROR_SETTINGS['sveetchies-documents-edit-page'].copy()
#CODEMIRROR_SETTINGS['sveetchies-documents-add-page']['quicksave_url'] = None
#CODEMIRROR_SETTINGS['sveetchies-documents-add-insert'] = CODEMIRROR_SETTINGS['sveetchies-documents-edit-insert'].copy()
#CODEMIRROR_SETTINGS['sveetchies-documents-add-insert']['quicksave_url'] = None

# Add custom cache keys to delete with the command option ``django-admin documents --clearcache``
DOCUMENTS_CACHE_KEYS_TO_CLEAN = []

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
