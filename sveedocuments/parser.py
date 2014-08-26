# -*- coding: utf-8 -*-
"""
ReStructuredText parser facilities
"""
import copy

try:
    from xml.etree.cElementTree import fromstring, tostring, ElementTree
except ImportError:
    from xml.etree.ElementTree import fromstring, tostring, ElementTree

from django.utils.encoding import smart_str

import docutils
import docutils.core

from rstview.parser import get_functional_settings

import sveedocuments.utils.rest_roles

def extract_toc(source, setting_key="default", body_only=True, initial_header_level=None, silent=True):
    """
    Extract the TOC from the rendered content by the parser
    
    This is very tricky, we add the ``contents`` directive to the document, 
    parse it again (sic) with docutils, then parse it with ElementTree to find 
    the TOC element to extract it. We assume the first element is allways the TOC.
    
    DEPRECATED: for some documents this cause Etree parsing errors
    """
    parser_settings = get_functional_settings(setting_key, body_only, initial_header_level, silent)
    
    toc_internal_id = "private-page-toc-menu"
    source = u".. contents:: {tocid}\n\n{source}".format(tocid=toc_internal_id, source=source)
    parts = docutils.core.publish_parts(source=smart_str(source), writer_name="html4css1", settings_overrides=parser_settings)

    extracted = fromstring((u"<div id=\"document_root_body\">"+parts['fragment']+u"</div>").encode('utf-8')).find("div")
    if extracted and 'id' in extracted.keys() and extracted.get("id") == toc_internal_id:
        return tostring(extracted.find("ul"), encoding="UTF-8").replace("<?xml version='1.0' encoding='UTF-8'?>", '').strip()
    
    return ''
