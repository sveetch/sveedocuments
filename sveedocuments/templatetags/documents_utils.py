# -*- coding: utf-8 -*-
"""
Templates tags divers pour les documents
"""
from django import template
from django.utils.safestring import mark_safe

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
