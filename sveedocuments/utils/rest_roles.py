# -*- coding: utf-8 -*-
"""
ReSTructured additional roles
"""
from docutils import nodes, utils
from docutils.parsers.rst import roles

from django.core.urlresolvers import reverse
from django.core.cache import cache

from sveedocuments.settings_local import DOCUMENTS_PARSER_WIKIROLE_SILENT_WARNING, PAGE_SLUGS_CACHE_KEY_NAME

from sveedocuments.models import Page

def get_page_slugs(force_update_cache=False):
    """
    Getting all visible *Pages* as a tuple ``(slug, title)``
    
    Use the cache system
    """
    if force_update_cache or not cache.get(PAGE_SLUGS_CACHE_KEY_NAME):
        slugs_map = dict(Page.objects.filter(visible=True).values_list('slug', 'title'))
        cache.set(PAGE_SLUGS_CACHE_KEY_NAME, slugs_map)
        return slugs_map
    return cache.get(PAGE_SLUGS_CACHE_KEY_NAME)

def page_link(role, rawtext, text, lineno, inliner, options={}, content=[]):
    """
    Role to make a reference link to other *Pages* by using their ``slug``
    """
    slugs = get_page_slugs()
    if text not in slugs and not DOCUMENTS_PARSER_WIKIROLE_SILENT_WARNING:
        msg = inliner.reporter.error('Page with slug "%s" does not exist.' % text, line=lineno)
        prb = inliner.problematic(rawtext, rawtext, msg)
        return [prb], [msg]
    options.update({'classes': ['documents_page_link']})
    roles.set_classes(options)
    node = nodes.reference(rawtext, utils.unescape(slugs[text]), refuri=reverse('documents-page-details', args=[text]), **options)
    return [node], []

roles.register_local_role('page', page_link)
