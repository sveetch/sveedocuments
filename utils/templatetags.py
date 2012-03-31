# -*- coding: utf-8 -*-
from django.template import Variable, TemplateSyntaxError, VariableDoesNotExist

def resolve_string_or_variable(value, context, safe=False, default=None, capture_none_value=True):
    """
    Resolve a template variable within the given context
    
    If the variable is a string (detected with surrounded quotes or double-quotes) it is 
    directly returned, else the ``Variable(value).resolve(context)`` method will be used 
    to find the variable in the context.
    
    As opposite to ``Variable().resolve()`` this method can silently work with ``None`` or 
    empty value.
    
    The process is :
    
    * Surrounded variable by single ou double quotes mean a string that is returned without 
      the surround quotes;
    * Else try to resolve it in the context;
    * If the resolve fail, raise an exception ``TemplateSyntaxError`` if ``safe`` is ``False`` 
      else return the ``default`` value that is ``None`` by default.
    
    :type value: string
    :param value: Valeur à résoudre. C'est soit directement une chaîne de caractères, 
                  soit un nom de variable à résoudre dans le context du template.
    
    :type context: object `django.template.RequestContext`
    :param context: Objet du contexte du template en cours ou sera recherché la valeur 
                    de la variable si ce n'est pas un simple string.
    
    :type safe: bool
    :param safe: (optional) Indique que l'échec pour retrouver le contenu de la variable 
                 doit être silencieux. Si activé, la valeur par défaut de ``default`` 
                 est renvoyée. False par défaut, l'échec remonte une exception 
                 `django.template.TemplateSyntaxError`.
    
    :type default: any
    :param default: (optional) Valeur par défaut renvoyée en cas d'échec pour retrouver 
                    la variable et si le mode silencieux est activé. Par défaut la 
                    valeur est ``None``.
    
    :type capture_none_value: bool
    :param capture_none_value: (optional) Indique si l'on doit capturer une variable du 
                               nom de "None" directement comme un ``None`` sans tenter de 
                               la résoudre comme un nom de variable. Dans ce cas, "None" 
                               deviendra un nom réservé pour le templatetag en cours. Si 
                               cette argument vaut ``False``, la méthode essayera de 
                               résoudre "None" comme un nom de variable dans le contexte. 
                               Par défaut cette option est activé (``True``).
    
    :rtype: any
    :return: La valeur de la variable si retrouvée, sinon la valeur par défaut.
    """
    # Capture du nom de variable "None" directement comme un ``None``
    if capture_none_value and value == "None":
        return None
    
    if value != None:
        # Ne résoud pas les chaînes de texte (toujours encerclés par des simples ou 
        # doubles quotes)
        if not(value[0] == value[-1] and value[0] in ('"', "'")):
            # Tente de résoudre le nom de variable dans le context donné
            try:
                value = Variable(value).resolve(context)
            except VariableDoesNotExist:
                # Échec qui remonte une exception de template
                if not safe:
                    raise TemplateSyntaxError("Unable to resolve '%s'" % value)
                # Échec silencieux qui renvoi la valeur par défaut sans lever d'exception
                else:
                    return default
        # Chaîne de texte dont on retire les quotes d'encerclement de la valeur
        else:
            value = value[1:-1]
    
    return value
