# -*- coding: utf-8 -*-
"""
Utilitaire autour des objets/instances de Django
"""
def get_instance_children(obj, depth=0, sig=0):
    """
    Récupèration récursive des relations enfants d'un objet
    
    @depth: integer limitant le niveau de recherche des enfants, 0=illimité
    """
    children = []
    # Pour toute les relations enfants de l'objet
    for child in obj._meta.get_all_related_objects():
        # Nom de l'attribut d'accès
        cname = child.get_accessor_name()
        verbose_name = child.model._meta.verbose_name
        # Récupère tout les objets des relations
        for elem in getattr(obj, cname).all():
            followed = []
            # Recherche récursive des enfants
            if depth == 0 or sig < depth:
                followed = get_instance_children(elem, depth=depth, sig=sig+1)
            children.append( (verbose_name, unicode(elem), followed) )
    return children
