# -*- coding: utf-8 -*-
"""
Utilities
"""
import copy, itertools

def _get_cache_keyset(keytpl, **kwargs):
    """
    Return a list of possible cache keys of a document (*Pages* or *Insert*)
    
    Because a document can have various active cache key for his various possible render 
    (from the parser settings) and elements, this is useful to invalidate caches after 
    changes.
    
    >>> _get_cache_keyset("id_{id}", **{'id':42})
    >>> ['id_42']
    >>> _get_cache_keyset("id_{id}-set_{set}-hlv_{hlv}", **{'id':42, 'setting': ['short','long'], 'hlv': range(1, 4)})
    >>> ['id_42-setting_short-hlv_1', 'id_42-setting_long-hlv_1', 'id_42-setting_short-hlv_2', 'id_42-setting_long-hlv_2', 'id_42-setting_short-hlv_3', 'id_42-setting_long-hlv_3']
    """
    keys = []
    # Tout les arguments qui sont des list/tuple
    list_args = filter((lambda keyname: isinstance(kwargs[keyname], list) or isinstance(kwargs[keyname], tuple)), kwargs.keys())
    # Tout les arguments qui ne sont pas list/tuple donc des string/int, donc des valeurs uniques
    nonlist_args = [k for k in kwargs if k not in list_args]
    # Context de base avec les arguments 'simples'
    base_context = dict(zip(nonlist_args, [kwargs[k] for k in nonlist_args]))
    
    # Produit une liste de toute les possibilités des arguments
    for item in itertools.product(*[kwargs[item] for item in list_args]):
        context = base_context.copy()
        context.update(dict(zip(list_args, item)))
        keys.append(keytpl.format(**context))

    return keys

