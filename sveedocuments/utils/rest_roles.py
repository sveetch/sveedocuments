# -*- coding: utf-8 -*-
"""
ReSTructured additional roles
"""
import os, re

from docutils import nodes, utils
from docutils.parsers.rst import roles

from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.contrib.sites.models import Site

from sveedocuments.local_settings import (DOCUMENTS_PARSER_WIKIROLE_SILENT_WARNING, 
                                            PAGE_SLUGS_CACHE_KEY_NAME, 
                                            PAGE_ATTACHMENTS_SLUGS_CACHE_KEY_NAME)

from sveedocuments.models import Page, Attachment

_ATTACHMENT_ROLE_REGEX = re.compile(r"^(?:id)(?P<id>[0-9]+)(?:\-)(?P<slug>.*?)$")

def rst_parser_error(msg, rawtext, text, lineno, inliner):
        msg = inliner.reporter.error(msg, line=lineno)
        prb = inliner.problematic(rawtext, rawtext, msg)
        return [prb], [msg]

def get_page_slugs(force_update_cache=False):
    """
    Get a dict of all visible *Pages* as a tuple ``(slug, title)``
    
    Try to get it from the cache if it exist, else build it
    """
    if force_update_cache or not cache.get(PAGE_SLUGS_CACHE_KEY_NAME):
        slugs_map = dict(Page.objects.filter(visible=True).values_list('slug', 'title'))
        cache.set(PAGE_SLUGS_CACHE_KEY_NAME, slugs_map)
        return slugs_map
    return cache.get(PAGE_SLUGS_CACHE_KEY_NAME)

def page_link(role, rawtext, text, lineno, inliner, options={}, content=[]):
    """
    Role to make a reference link to other *Pages* by using their ``slug``
    
    Usage in document :
    
        Blah blah :page:`my-page-slug`
    """
    # Get the page slugs map
    slugs = get_page_slugs()
    # Throw error if the given slug does not exist
    if text not in slugs and not DOCUMENTS_PARSER_WIKIROLE_SILENT_WARNING:
        msg = inliner.reporter.error('Page with slug "%s" does not exist.' % text, line=lineno)
        prb = inliner.problematic(rawtext, rawtext, msg)
        return [prb], [msg]
    # Add a class to the item
    options.update({'classes': ['documents_page_link']})
    roles.set_classes(options)
    # Return the node as reference to display the link for the given page's slug
    site_current = Site.objects.get_current()
    url = "http://{0}{1}".format(site_current.domain, reverse('documents-page-details', args=[text]))
    node = nodes.reference(rawtext, utils.unescape(slugs[text]), refuri=url, **options)
    return [node], []

roles.register_local_role('page', page_link)


def get_page_attachment_slugs(page_id, force_update_cache=False):
    """
    Get a dict of all Attachments linked to a Page
    
    Try to get it from the cache if it exist, else build it
    """
    cache_key = PAGE_ATTACHMENTS_SLUGS_CACHE_KEY_NAME.format(page_id)
    if force_update_cache or not cache.get(cache_key):
        page = Page.objects.get(pk=page_id)
        slugs_map = dict(page.attachment.all().values_list('slug', 'file'))
        cache.set(cache_key, slugs_map)
        return slugs_map
    return cache.get(cache_key)

def page_attachment(role, rawtext, text, lineno, inliner, options={}, content=[]):
    """
    Role to make a reference link to a Page's attachment
    
    Usage in document :
    
        Blah blah :attachment:`idX-slug`
        
    Where X is the page id and slug his slugname
    
    The page id is needed because i can't find a clean way to give some page context to 
    the docutils parser.
    """
    matched = _ATTACHMENT_ROLE_REGEX.match(text)
    if not matched or len(matched.groups())<2:
        return rst_parser_error('Attachment role syntax is not respected with "{0}", you should write something like "idXX-ATTACHMENT_SLUG".'.format(text), rawtext, text, lineno, inliner)
    
    # Get the page slugs map
    pk, attachment_slug = matched.groups()
    try:
        slugs_map = get_page_attachment_slugs(pk)
    except Page.DoesNotExist:
        return rst_parser_error('Page with id "{pk}" does not exist in pattern "{pattern}"'.format(pk=pk, pattern=text), rawtext, text, lineno, inliner)
    else:
        if attachment_slug not in slugs_map and not DOCUMENTS_PARSER_WIKIROLE_SILENT_WARNING:
            return rst_parser_error('Attachment with slug "{slug}" does not exist for page id "{pk}" in pattern "{pattern}".'.format(pk=pk, slug=attachment_slug, pattern=text), rawtext, text, lineno, inliner)
        link = slugs_map[attachment_slug]
        # Add a class to the item
        options.update({'classes': ['documents_page_attachment']})
        roles.set_classes(options)
        # Return the node as reference to display the link for the given page's slug
        node = nodes.reference(rawtext, utils.unescape(attachment_slug), refuri=os.path.join(settings.MEDIA_URL, link), **options)
        return [node], []

roles.register_local_role('attachment', page_attachment)
