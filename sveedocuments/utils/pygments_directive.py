# -*- coding: utf-8 -*-
"""
Pygments ReStructuredText directive

To use it, adjust the options below and copy the code into a module
that you import on initialization.  The code then automatically
registers a ``sourcecode`` directive that you can use instead of
normal code blocks like this::

    .. sourcecode:: python

        My code goes here.

If you want to have different code styles, e.g. one with line numbers
and one without, add formatters with their names in the VARIANTS dict
below.  You can invoke them instead of the DEFAULT one by using a
directive option::

    .. sourcecode:: python
        :linenos:

        My code goes here.

With ``lineos`` option actived you can highlight some lines :

    .. sourcecode:: python
        :linenos:
        :hl_lines: 3,5

        My code start here at line 1.
        
        This line is important.
        
        This one too.

This will highlight line 3 and 5, you must supply each line number to highlight.

Used command line to generate the Pygments CSS for **Sveetchies-documents** : ::

    pygmentize -P "classprefix=pygments_" -S trac -a ".pygments" -f html > webapp_statics/theme/css/pygments.css
"""
from pygments import highlight
from pygments.lexers import get_lexer_by_name, TextLexer
from pygments.formatters import HtmlFormatter

from docutils import nodes
from docutils.parsers.rst import directives

from sveedocuments.settings_local import PYGMENTS_CONTAINER_CLASSPREFIX, PYGMENTS_INLINESTYLES

OPTS = {
    'linenos': directives.flag, # line number
    'hl_lines': directives.unchanged_required, # highlight lines with their line number
}

def pygments_directive(name, arguments, options, content, lineno, content_offset, block_text, state, state_machine):
    try:
        lexer = get_lexer_by_name(arguments[0])
    except ValueError:
        # no lexer found - use the text one instead of an exception
        lexer = TextLexer()
    # formatter options
    opt_kwargs = {}
    if 'hl_lines' in options:
        opt_kwargs['hl_lines'] = format_hllines_list(options['hl_lines'])
    if 'linenos' in options or opt_kwargs.get('hl_lines', False):
        opt_kwargs['linenos'] = True
    formatter = HtmlFormatter(
        noclasses=PYGMENTS_INLINESTYLES,
        classprefix="{0}_".format(PYGMENTS_CONTAINER_CLASSPREFIX),
        cssclass=PYGMENTS_CONTAINER_CLASSPREFIX,
        **opt_kwargs
    )
    
    parsed = highlight(u'\n'.join(content), lexer, formatter)
    return [nodes.raw('', parsed, format='html')]

def format_hllines_list(value):
    """
    Parse line number list, each number must be separated with comma, unvalid 
    number is ignored.
    """
    linelist = []
    for item in value.split(','):
        try:
            v = int(item)
        except ValueError:
            pass
        else:
            linelist.append(v)
    return linelist

# Directive registration
pygments_directive.arguments = (1, 0, 1)
pygments_directive.content = 1
pygments_directive.options = OPTS
directives.register_directive('sourcecode', pygments_directive)
