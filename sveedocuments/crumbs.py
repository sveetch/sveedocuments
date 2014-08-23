# -*- coding: utf-8 -*-
"""
Application Crumbs
"""
from autobreadcrumbs import site
from django.utils.translation import ugettext_lazy

site.update({
    'sveedocuments:index': ugettext_lazy('Document sitemap'),
    'sveedocuments:board': ugettext_lazy('Document management'),
    'sveedocuments:insert-index': ugettext_lazy('Insert documents'),
    'sveedocuments:insert-add': ugettext_lazy('Add a new insert document'),
    'sveedocuments:insert-delete': ugettext_lazy('Delete #{{ insert_instance.slug }}'),
    'sveedocuments:insert-edit': ugettext_lazy('Edit #{{ insert_instance.slug }}'),
    'sveedocuments:page-index': ugettext_lazy('Pages'),
    'sveedocuments:page-add': ugettext_lazy('Add a new page'),
    'sveedocuments:page-details': ugettext_lazy('{{ page_instance.title }}'),
    'sveedocuments:page-delete': ugettext_lazy('Delete #{{ page_instance.slug }}'),
    'sveedocuments:page-history': ugettext_lazy('History'),
    'sveedocuments:page-attachments': ugettext_lazy('Attachments'),
    'sveedocuments:help': ugettext_lazy('Usage help'),
    'sveedocuments:page-edit': ugettext_lazy('Edit #{{ page_instance.slug }}'),
    'sveedocuments:page-add-child': ugettext_lazy('Add a new child page to #{{ parent_page_instance.slug }}'),
})
