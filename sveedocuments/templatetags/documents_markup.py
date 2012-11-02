# -*- coding: utf-8 -*-
"""
Parser template tags 
"""
from django import template
from django.conf import settings
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

from rstview.parser import SourceParser

from sveedocuments.templatetags import get_render_with_cache, get_toc_with_cache

register = template.Library()

def source_render(source, setting_key="default"):
    """
    Return the parser result from the given string source and settings
    """
    return mark_safe( SourceParser(source, setting_key=setting_key) )
source_render.is_safe = True
register.filter(source_render)

def document_render(document_instance, setting_key="default"):
    """
    Return the parser result from the content of the given instance (*Pages* or 
    *Insert*) and settings
    """
    return mark_safe( get_render_with_cache(document_instance, setting_key=setting_key) )
document_render.is_safe = True
register.filter(document_render)

def document_toc(document_instance, setting_key="default"):
    """
    Get the TOC (Table Of Content) from the content of the given instance (*Pages* 
    or *Insert*) and settings
    """
    return mark_safe( get_toc_with_cache(document_instance, setting_key=setting_key) )
document_toc.is_safe = True
register.filter(document_toc)
