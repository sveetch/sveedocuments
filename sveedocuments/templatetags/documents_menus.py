# -*- coding: utf-8 -*-
"""
Templates tags divers pour les documents
"""
from django import template
from django.utils.safestring import mark_safe

from sveedocuments.local_settings import DOCUMENTS_PAGE_TREEMENU, DOCUMENTS_PAGE_FLATMENU
from sveedocuments.models import Insert, Page
from sveedocuments.utils.templatetags import resolve_string_or_variable

register = template.Library()

class PageMenuTagRender(template.Node):
    """
    Generate HTML of the node *PageMenuTagRender*
    
    TODO: @flat_mode usage is a failure because it works like the tree, flat menu should 
          never include the Page from where to start and display only his direct 
          children.
    """
    def __init__(self, page_var_name, template_path_varname=None, flat_mode=0):
        """
        :type page_var_name: string or object ``django.db.models.Model``
        :param page_var_name: Nom de variable de l'instance ou un string 
                                        pour le slug.
                                        
        :type template_path_varname: string
        :param template_path_varname: (optionnel) Chemin d'un template à utiliser pour 
                                      le rendu du menu à générer
                                        
        :type flat_mode: int
        :param flat_mode: (optionnel) Indique si on doit gérer un menu avec seulement les 
                          pages adjacentes (flat) à la page ciblée ou bien l'arborescence 
                          récursive de ses enfants (tree).
        """
        self.page_var_name = page_var_name
        self.template_path_varname = template_path_varname
        self.flat_mode = flat_mode
    
    def render(self, context):
        """
        Rendu de tout les éléments du formulaire indiqué
        
        :type context: object ``django.template.Context``
        :param context: Objet du contexte du tag.
        
        :rtype: string
        :return: Le rendu généré pour le tag capturé.
        """
        html = ''
        parser_kwargs = {}
        active_page_instance = None
        
        # Résolution des arguments
        page_var = resolve_string_or_variable(self.page_var_name, context)
        # Template par défaut selon le mode (arborescence/plat)
        if not self.flat_mode:
            self.template_path = DOCUMENTS_PAGE_TREEMENU
        else:
            self.template_path = DOCUMENTS_PAGE_FLATMENU
        # Custom template if any
        if self.template_path_varname:
            self.template_path = resolve_string_or_variable(self.template_path_varname, context)
        
        # Transmet au contexte du tag l'instance de la page courante si elle est présente 
        # dans le contexte de la page
        if 'page_instance' in context:
            active_page_instance = context['page_instance']
        
        return self.build(context, page_var, active_page_instance)
    
    def build(self, context, page_var, active_page_instance=None):
        """
        Calcul du rendu du menu, renvoi le menu html ou bien une chaine vide dans 
        certains cas ou la cible n'existe pas
        """
        # Recherche d'un zéro pour signifier qu'on doit commencer non pas depuis une 
        # instance mais depuis la racine de l'arborescence
        if isinstance(page_var, int):
            if page_var == 0:
                page_instance = None
                page_list = Page.objects
                if self.flat_mode:
                    page_list = page_list.root_nodes()
                page_list = page_list.filter(visible=True)
            # Page ids are not supported
            else:
                return ''
        # Instance directement transmise
        elif isinstance(page_var, Page):
            page_instance = page_var
            if self.flat_mode == 1:
                page_list = page_var.get_siblings(include_self=True).filter(visible=True)
            elif self.flat_mode == 2:
                page_list = page_var.get_children().filter(visible=True)
            else:
                page_list = page_var.get_descendants(include_self=False).filter(visible=True)
        # Réception d'un slug pour récupérer l'instance
        else:
            try:
                instance = Page.objects.get(slug=page_var, visible=True)
            except Page.DoesNotExist:
                return ''
            else:
                page_instance = instance
                if self.flat_mode == 1:
                    page_list = instance.get_siblings(include_self=True).filter(visible=True)
                elif self.flat_mode == 2:
                    page_list = instance.get_children().filter(visible=True)
                else:
                    page_list = instance.get_descendants(include_self=False).filter(visible=True)
        
        # Aucun élément, on ne poursuit pas
        if not page_list:
            return ''
        
        # Permet à un menu "plat" (flat) de retrouver le parent de la page en cours
        # NOTE: ne marchera qu'avec un menu à la racine, il faut utiliser get_ancestors 
        # et test "in"
        if active_page_instance:
            active_page_instance.root_slug = None
            if self.flat_mode:
                active_page_instance.root_slug = active_page_instance.get_root().slug
        
        subcontext = {
            'active_page_instance': active_page_instance,
            'page_instance': page_instance,
            'page_list': page_list,
        }
        
        html = template.loader.get_template(self.template_path).render(template.Context(subcontext))
        
        return mark_safe(html)

@register.tag(name="document_page_treemenu")
def do_document_page_treemenu(parser, token):
    """
    Display a tree menu of **Pages**
    
    TODO: Pouvoir limiter le niveau de récursivité (0->n)
    
    Arguments :
    
    document_object
        Instance "Page" ou un string contenant un slug de l'instance à récupérer
        
    Exemple d'utilisation par une instance Page : ::
    
        {% document_page_treemenu instance %}
        
    Ou par le slug de l'Insert à utiliser : ::
    
        {% document_page_treemenu "my-page-slug" %}
    
    Ou la totalité de l'arborescence des pages avec un zéro pour signifier qu'on 
    commence depuis la racine : ::
    
        {% document_page_treemenu 0 %}
    
    On peut aussi spécifier un template autre que celui par défaut : ::
    
        {% document_page_treemenu instance "mymenu.html" %}
        
    :type parser: object ``django.template.Parser``
    :param parser: Objet du parser de template.
    
    :type token: object ``django.template.Token``
    :param token: Objet de la chaîne découpée du tag capturé dans le template.
    
    :rtype: object ``PageMenuTagRender``
    :return: L'objet du générateur de rendu du tag.
    """
    args = token.split_contents()
    if len(args) < 2:
        raise template.TemplateSyntaxError, "You need to specify at less a \"Page\" instance, a slug or a 0 (for full sitemap)"
    else:
        return PageMenuTagRender(*args[1:])

do_document_page_treemenu.is_safe = True

@register.tag(name="document_page_flat_adjacents")
def do_document_page_flat_adjacents(parser, token):
    """
    Display a flat menu of adjacents **Pages**
    """
    args = token.split_contents()
    if len(args) < 2:
        raise template.TemplateSyntaxError, "You need to specify at less a \"Page\" instance or a slug"
    else:
        return PageMenuTagRender(*args[1:], flat_mode=1)

do_document_page_flat_adjacents.is_safe = True

@register.tag(name="document_page_flat_children")
def do_document_page_flat_children(parser, token):
    """
    Display a flat menu of children **Pages**
    """
    args = token.split_contents()
    if len(args) < 2:
        raise template.TemplateSyntaxError, "You need to specify at less a \"Page\" instance or a slug"
    else:
        return PageMenuTagRender(*args[1:], flat_mode=2)

do_document_page_flat_children.is_safe = True

@register.simple_tag
def pprint_recurse(elements):
    return recurse_list(elements)

def recurse_list(relations, sig=0):
    """
    Renvoi une liste à puce récursive de toute les relations
    """
    output = ""
    if not relations:
        return output
    for name, object_title, followed in relations:
        children = recurse_list(followed, sig=sig+1)
        output += "<li><p><strong>%s :</strong> %s</p>%s</li>" % (name.title(), object_title, children)
    return ("""<ul class="level_%s">"""%sig) + output + "</ul>"
