"""
Original code is from 'Bradley Wright' on Github :

https://github.com/bradleywright/rst-to-semantic-html5

Stealed and modified as i want to keep <section/> and i don't want to take the same way 
than 'rst-to-semantic-html5'
"""
import re

from docutils import nodes, utils
from docutils.writers import html4css1
from docutils.core import publish_parts
from docutils.parsers.rst import roles, directives, Directive

class SemanticHTML5Writer(html4css1.Writer):
    """
    This docutils writer will use the SemanticHTML5Translator class below.

    """
    def __init__(self):
        html4css1.Writer.__init__(self)
        self.translator_class = SemanticHTML5Translator


class SemanticHTML5Translator(html4css1.HTMLTranslator):
    """
    This is a translator class for the docutils system.
    It will produce a minimal set of html output.
    (No extra divs, classes over ids.)

    It also aims to produce HTML5 (section etc.)

    """

    def should_be_compact_paragraph(self, node):
        if(isinstance(node.parent, nodes.block_quote)):
            return 0
        return html4css1.HTMLTranslator.should_be_compact_paragraph(self, node)

    def visit_section(self, node):
        self.section_level += 1
        self.body.append(self.starttag(node, 'section', ''))

    def depart_section(self, node):
        self.section_level -= 1
        self.body.append('</section>')

    def visit_literal_block(self, node):
        "No classes please"
        self.body.append(self.starttag(node, 'pre', ''))

    def visit_literal(self, node):
        self.body.append(
            self.starttag(node, 'code', ''))

    def depart_literal(self, node):
        self.body.append('</code>')

    def visit_abbreviation(self, node):
        attrs = {}
        if node.hasattr('explanation'):
            attrs['title'] = node['explanation']
        self.body.append(self.starttag(node, 'abbr', '', **attrs))

    def depart_abbreviation(self, node):
        self.body.append('</abbr>')

    def visit_kbd(self, node):
        self.body.append(self.starttag(node, 'kbd', ''))

    def depart_kbd(self, node):
        self.body.append('</kbd>')



class kbd(nodes.Inline, nodes.TextElement):
    """Node for kbd element"""

nodes._add_node_class_names('kbd')

def inline_roles(role, raw, text, *args):
    if role == 'kbd':
        return [kbd('kbd', text)], []
    elif role == 'var':
        return [nodes.literal('var', text)], []

roles.register_local_role('kbd', inline_roles)
roles.register_local_role('var', inline_roles)

# FIXME: this has to be lowercase for some reason
class abbreviation(nodes.Inline, nodes.TextElement):
    """Node for abbreviations with explanations."""

nodes._add_node_class_names('abbreviation')

_abbr_re = re.compile('\((.*)\)$', re.S)

def abbr_role(typ, rawtext, text, lineno, inliner, options={}, content=[]):
    text = utils.unescape(text)
    m = _abbr_re.search(text)
    if m is None:
        return [abbreviation(text, text)], []
    abbr = text[:m.start()].strip()
    expl = m.group(1)
    return [abbreviation(abbr, abbr, explanation=expl)], []

roles.register_local_role('abbr', abbr_role)
