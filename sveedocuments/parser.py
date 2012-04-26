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
import docutils.nodes
import docutils.utils
import docutils.parsers.rst

import sveedocuments.utils.rest_roles

from sveedocuments.settings_local import DOCUMENTS_PARSER_FILTER_SETTINGS

# Loading directive with failsafe if Pygments is not installed
try:
    import sveedocuments.utils.pygments_directive
except ImportError:
    pass

def get_functional_settings(setting_key, body_only, initial_header_level, silent):
    """
    Compute various parser settings and options to return an unique settings dict
    """
    parser_settings = copy.deepcopy(DOCUMENTS_PARSER_FILTER_SETTINGS[setting_key])
    parser_settings.update({'halt_level':6, 'enable_exit':0})
    if silent:
        parser_settings.update({'report_level': 5})
    if initial_header_level:
        parser_settings['initial_header_level'] = initial_header_level
    return parser_settings

def SourceParser(source, setting_key="default", body_only=True, initial_header_level=None, silent=True):
    """
    Parse the source with the given options and settings
    """
    parser_settings = get_functional_settings(setting_key, body_only, initial_header_level, silent)
    
    parts = docutils.core.publish_parts(source=smart_str(source), writer_name="html4css1", settings_overrides=parser_settings)

    if body_only:
        return parts['fragment']
    return parts

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

class SilentReporter(docutils.utils.Reporter):
    """
    Silent reporter
    
    All warnings and errors will be stored and can be used subsequently through the 
    reporter instance
    """
    def __init__(self, source, report_level, halt_level, stream=None,
                    debug=0, encoding='ascii', error_handler='replace'):
        self.messages = []
        docutils.utils.Reporter.__init__(self, source, report_level, halt_level, stream,
                            debug, encoding, error_handler)

    def system_message(self, level, message, *children, **kwargs):
        self.messages.append((level, message, children, kwargs))

def SourceReporter(data, setting_key="default"):
    """
    Catch errors and syntax warnings to use them at part of the rendered content
    
    Renvoi une liste d'erreurs si il y'en a
    
    TODO: * Devrait renvoyer tout les avertissements et pas s'arrêter de parser dès la 
            première erreur;
          * Manque l'application des settings d'options possibles;
          * à mieux calibrer parce qu'en l'état je ne suis pas trop sûr du paramétrage 
            appliqué au parser et reporter;
    """
    source_path = None
    parser = docutils.parsers.rst.Parser()
    settings = docutils.frontend.OptionParser().get_default_values()
    settings.tab_width = 4
    settings.pep_references = None
    settings.rfc_references = None
    reporter = SilentReporter(
        source_path,
        settings.report_level,
        settings.halt_level,
        stream=settings.warning_stream,
        debug=settings.debug,
        encoding=settings.error_encoding,
        error_handler=settings.error_encoding_error_handler
    )

    document = docutils.nodes.document(settings, reporter, source=source_path)
    document.note_source(source_path, -1)
    try:
        parser.parse(data, document)
    except AttributeError:
        pass
    except TypeError:
        # Catch ``TypeError`` to avoid problems with local roles
        # NOTE: Is this still necessary ?
        pass
    return reporter.messages

def map_parsing_errors(error):
    """
    Nice render for errors and warnings
    """
    code, message, content, source = error
    return u"Ligne {lineno} : {message}".format(lineno=source.get('line', 0), message=message)
