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
    
    Actuellement c'est très gruik :
    
    * Pas de possibilité évidente d'avoir le TOC en dehors du document via la 
      directive ``contents`` donc cette méthode parse de son coté la source en lui 
      ajoutant cette directive au tout début;
    * Le résultat est parsé comme du ElementTree pour y retrouver le bloc concernant le 
      TOC et l'extraire;
    * Comme la recherche Xpath n'est pas assez développé dans le ElementTree embarqué dans 
      Python 2.6, on assume que le premier bloc est toujours celui du TOC (à ma 
      connaissance ce n'est pas possible autrement);
    """
    parser_settings = get_functional_settings(setting_key, body_only, initial_header_level, silent)
    
    toc_internal_id = "private-page-toc-menu"
    source = u".. contents:: {tocid}\n\n{source}".format(tocid=toc_internal_id, source=source)
    parts = docutils.core.publish_parts(source=smart_str(source), writer_name="html4css1", settings_overrides=parser_settings)

    extracted = fromstring((u"<div id=\"document_root_body\">"+parts['fragment']+u"</div>").encode('utf-8')).find("div")
    if extracted and 'id' in extracted.keys() and extracted.get("id") == toc_internal_id:
        return tostring(extracted.find("ul"), encoding="UTF-8").replace("<?xml version='1.0' encoding='UTF-8'?>", '').strip()
    
    return ''
