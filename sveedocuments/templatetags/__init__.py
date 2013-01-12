# -*- coding: utf-8 -*-
from django.core.cache import cache

from rstview.parser import SourceParser

from sveedocuments.parser import extract_toc

def get_render_with_cache(instance, setting_key="default", force_update_cache=False, initial_header_level=None):
    """
    Get an instance content render by the parser
    
    Use the cache system, content will not be rendered again if it allready exists in the cache
    """
    cache_key = instance.get_render_cache_key(setting=setting_key, header_level=initial_header_level)
    if force_update_cache or not cache.get(cache_key):
        if not instance.content:
            rendered = ''
        rendered = SourceParser(instance.content, setting_key=setting_key, initial_header_level=initial_header_level)
        cache.set(cache_key, rendered)
        return rendered
    return cache.get(cache_key)

def get_toc_with_cache(instance, setting_key="default", force_update_cache=False, initial_header_level=None):
    """
    Extract the TOC from the rendered content of an instance and return it
    
    Use the cache system, content will not be rendered again if it allready exists in the cache
    """
    cache_key = instance.get_toc_cache_key(setting=setting_key, header_level=initial_header_level)
    if force_update_cache or not cache.get(cache_key):
        if not instance.content:
            toc = ''
        toc = extract_toc(instance.content, setting_key=setting_key, initial_header_level=initial_header_level)
        cache.set(cache_key, toc)
        return toc
    return cache.get(cache_key)
