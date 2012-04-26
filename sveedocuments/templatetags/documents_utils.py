# -*- coding: utf-8 -*-
"""
Templates tags divers pour les documents
"""
from django import template
from django.utils.safestring import mark_safe
from django.core.cache import cache

from sveedocuments.settings_local import DOCUMENTS_PAGE_TREEMENU, DOCUMENTS_PAGE_FLATMENU
from sveedocuments.models import Insert, Page
from sveedocuments.templatetags import get_render_with_cache, get_toc_with_cache
from sveedocuments.utils.templatetags import resolve_string_or_variable

register = template.Library()

class DocumentTagContext(template.Node):
    """
    Generate the document elements (content, TOC, navigation)
    
    This doesn't add any HTML, all elements are injected in the current template context 
    where you can use them.
    """
    def __init__(self, insert_instance_varname, setting_key_varname=None, title_level_varname=None, with_toc=True, with_navigation=True):
        """
        :type insert_instance_varname: string or object ``django.db.models.Model``
        :param insert_instance_varname: Nom de variable de l'instance ou un string 
                                        pour le slug.
                                        
        :type setting_key_varname: string
        :param setting_key_varname: (optionnel) Nom clé du schéma d'options du parser à 
                                    utiliser, par défaut utilise le schéma "short" dédié 
                                    aux documents à insérer.
        
        :type title_level_varname: int
        :param title_level_varname: Niveau minimale des titres de premier niveau, par 
                                    défaut utilise celui du schéma. Si une valeur est 
                                    spécifiée, elle sera utilisée comme limite, par 
                                    exemple avec une valeur de 4, aucun titres ne sera 
                                    plus haut qu'un ``<h4/>`` (donc seulement h4, h5, h6).
        """
        self.insert_instance_varname = insert_instance_varname
        self.setting_key_varname = setting_key_varname
        self.title_level_varname = title_level_varname
        self.with_toc = with_toc
        self.with_navigation = with_navigation
    
    def render(self, context):
        """
        TODO: Lever une exception de template évident quand le setting demandé n'existe 
              pas.
        
        :type context: object ``django.template.Context``
        :param context: Objet du contexte du tag.
        
        :rtype: string
        :return: Le rendu généré pour le tag capturé.
        """
        html = ''
        parser_kwargs = {}
        content_render = toc_render = navigation_render = None
        
        # Résolution des arguments
        instance = resolve_string_or_variable(self.insert_instance_varname, context)
        
        setting_key = resolve_string_or_variable(self.setting_key_varname, context)
        if setting_key:
            parser_kwargs['setting_key'] = setting_key
        
        title_level = resolve_string_or_variable(self.title_level_varname, context)
        if title_level:
            parser_kwargs['initial_header_level'] = title_level
        
        content_render = mark_safe( get_render_with_cache(instance, **parser_kwargs) )
        if self.with_toc:
            toc_render = mark_safe( get_toc_with_cache(instance, **parser_kwargs) )
        if self.with_navigation and isinstance(instance, Page):
            navigation = instance.get_descendants(include_self=False).filter(visible=True)
        
        context.update({
            'document_toc': toc_render,
            'document_navigation': navigation,
            'document_render': content_render,
        })
        
        return ''

class InsertTagRender(template.Node):
    """
    Generate HTML of the node *InsertTagRender*
    """
    def __init__(self, insert_instance_varname, setting_key_varname=None, title_level_varname=None):
        """
        :type insert_instance_varname: string or object ``django.db.models.Model``
        :param insert_instance_varname: Nom de variable de l'instance ou un string 
                                        pour le slug.
                                        
        :type setting_key_varname: string
        :param setting_key_varname: (optionnel) Nom clé du schéma d'options du parser à 
                                    utiliser, par défaut utilise le schéma "short" dédié 
                                    aux documents à insérer.
        
        :type title_level_varname: int
        :param title_level_varname: Niveau minimale des titres de premier niveau, par 
                                    défaut utilise celui du schéma. Si une valeur est 
                                    spécifiée, elle sera utilisée comme limite, par 
                                    exemple avec une valeur de 4, aucun titres ne sera 
                                    plus haut qu'un ``<h4/>`` (donc seulement h4, h5, h6).
        """
        self.insert_instance_varname = insert_instance_varname
        self.setting_key_varname = setting_key_varname
        self.title_level_varname = title_level_varname
    
    def render(self, context):
        """
        TODO: Lever une exception de template évident quand le setting demandé n'existe 
              pas.
        
        :type context: object ``django.template.Context``
        :param context: Objet du contexte du tag.
        
        :rtype: string
        :return: Le rendu généré pour le tag capturé.
        """
        html = ''
        parser_kwargs = {}
        
        # Résolution de l'instance du formulaire
        self.insert_instance = resolve_string_or_variable(self.insert_instance_varname, context)
        
        self.setting_key = resolve_string_or_variable(self.setting_key_varname, context)
        if self.setting_key:
            parser_kwargs['setting_key'] = self.setting_key
        
        self.title_level = resolve_string_or_variable(self.title_level_varname, context)
        if self.title_level:
            parser_kwargs['initial_header_level'] = self.title_level
        
        # Réception d'un slug pour récupérer l'instance
        if isinstance(self.insert_instance, basestring):
            try:
                instance = Insert.objects.get(slug=self.insert_instance, visible=True)
            except Insert.DoesNotExist:
                return ''
            else:
                self.insert_instance = instance
        
        html = get_render_with_cache(self.insert_instance, **parser_kwargs)
        
        return mark_safe(html)

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
        # Template spécifié if any
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

@register.tag(name="document_context")
def do_document_context(parser, token):
    """
    Push the document elements in the context
    
    Arguments :
    
    document_object
        Instance (``Page`` ou ``Insert``) ou un string contenant un slug de l'instance 
        à récupérer
        
    Exemple d'utilisation par une instance Insert : ::
    
        {% document_insert instance %}
        
    Exemple d'utilisation par le slug de l'Insert à utiliser : ::
    
        {% document_insert "my-insert-slug" %}
    
    :type parser: object ``django.template.Parser``
    :param parser: Objet du parser de template.
    
    :type token: object ``django.template.Token``
    :param token: Objet de la chaîne découpée du tag capturé dans le template.
    
    :rtype: object ``InsertTagRender``
    :return: L'objet du générateur de rendu du tag.
    """
    args = token.split_contents()
    if len(args) < 2:
        raise template.TemplateSyntaxError, "You need to specify at less an instance (Insert or Page) or a slug"
    else:
        return DocumentTagContext(*args[1:])

@register.tag(name="document_insert")
def do_document_insert(parser, token):
    """
    Display the parsed content of an **Insert** document
    
    Arguments :
    
    document_object
        Instance "Insert" ou un string contenant un slug de l'instance à récupérer
        
    Exemple d'utilisation par une instance Insert : ::
    
        {% document_insert instance %}
        
    Exemple d'utilisation par le slug de l'Insert à utiliser : ::
    
        {% document_insert "my-insert-slug" %}
    
    :type parser: object ``django.template.Parser``
    :param parser: Objet du parser de template.
    
    :type token: object ``django.template.Token``
    :param token: Objet de la chaîne découpée du tag capturé dans le template.
    
    :rtype: object ``InsertTagRender``
    :return: L'objet du générateur de rendu du tag.
    """
    args = token.split_contents()
    if len(args) < 2:
        raise template.TemplateSyntaxError, "You need to specify at less an \"Insert\" instance or a slug"
    else:
        return InsertTagRender(*args[1:])

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
        raise template.TemplateSyntaxError, "You need to specify at less a \"Page\" instance or a slug"
    else:
        return PageMenuTagRender(*args[1:])

do_document_page_treemenu.is_safe = True

#@register.tag(name="document_page_flatmenu")
#def do_document_page_flatmenu(parser, token):
    #pass

#do_document_page_flatmenu.is_safe = True

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
