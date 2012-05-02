# -*- coding: utf-8 -*-
"""
Application Crumbs
"""
from autobreadcrumbs import site
from django.utils.translation import ugettext_lazy

site.update({
    'documents-index': ugettext_lazy('Sitemap'),
    'documents-board': ugettext_lazy('Document management'),
    'documents-insert-add': ugettext_lazy('Add a new insert document'),
    'documents-insert-delete': ugettext_lazy('Delete insert document #{{ insert_instance.slug }}'),
    'documents-insert-edit': ugettext_lazy('Edit insert document #{{ insert_instance.slug }}'),
    'documents-page-add': ugettext_lazy('Add a new page'),
    'documents-page-delete': ugettext_lazy('Delete page #{{ page_instance.slug }}'),
    'documents-help': ugettext_lazy('Usage help'),
    'documents-page-edit': ugettext_lazy('Edit page #{{ page_instance.slug }}'),
    'documents-page-add-child': ugettext_lazy('Add a new child page to #{{ parent_page_instance.slug }}'),
})
