# -*- coding: utf-8 -*-
"""
Application Crumbs
"""
from autobreadcrumbs import site
from django.utils.translation import ugettext_lazy

site.update({
    'documents-index': ugettext_lazy('Document sitemap'),
    'documents-board': ugettext_lazy('Document management'),
    'documents-insert-index': ugettext_lazy('Insert documents'),
    'documents-insert-add': ugettext_lazy('Add a new insert document'),
    'documents-insert-delete': ugettext_lazy('Delete #{{ insert_instance.slug }}'),
    'documents-insert-edit': ugettext_lazy('Edit #{{ insert_instance.slug }}'),
    'documents-page-index': ugettext_lazy('Pages'),
    'documents-page-add': ugettext_lazy('Add a new page'),
    'documents-page-delete': ugettext_lazy('Delete #{{ page_instance.slug }}'),
    'documents-page-history': ugettext_lazy('History'),
    'documents-page-attachments': ugettext_lazy('Attachments'),
    'documents-help': ugettext_lazy('Usage help'),
    'documents-page-edit': ugettext_lazy('Edit #{{ page_instance.slug }}'),
    'documents-page-add-child': ugettext_lazy('Add a new child page to #{{ parent_page_instance.slug }}'),
})
