# -*- coding: utf-8 -*-
"""
Utilitaires liés aux champs de fichiers dans les modèles de données
"""
from datetime import datetime as real_datetime
from os import makedirs
from os.path import basename, dirname, exists, isdir, join, splitext

from django.conf import settings
from django.utils.datetime_safe import strftime

def content_file_name(upload_to_path, instance, filename=None, new_extension=None):
    """
    Méthode à utiliser pour l'attribut "upload_to" d'un FileField/ImageField pour 
    renommer automatiquement le nom de fichier avec un nom unique et empêcher la 
    conservation de fichier avec des caractères spéciaux.
    
    À ne pas utiliser directement sur l'attribut "FileField.upload_to" 
    mais via un callable pour indiquer le chemin "upload_to" par exemple :
    
        ATTACH_FILE_UPLOADTO = lambda x,y: content_file_name('attach/%Y/%m/%d', x, y)
    
    puis
    
        file = models.FileField(u'fichier', upload_to=ATTACH_FILE_UPLOADTO)
    """
    upload_to = real_datetime.now().strftime(upload_to_path)
    if not filename:
        return upload_to
    filename = get_unique_filename(filename, new_extension=new_extension)
    return '/'.join([upload_to, filename])

def get_unique_filename(filename, new_filename=None, new_extension=None):
    """
    Génère un nouveau nom pour un fichier en gardant son extension
    
    Soit le nouveau nom est généré à partir de la date 
    (heures+minutes+secondes+microsecondes) soit un nouveau nom est spécifié et on 
    l'utilise tel quel.
    
    :type filename: string
    :param filename: Nom du fichier original
    
    :type new_filename: string
    :param new_filename: (optional) Nouveau nom de fichier personnalisé, ceci implique que 
                         la date ne sera pas insérée dans le nouveau nom
    
    :type new_extension: string
    :param new_extension: (optional) Force une nouvelle extension de fichier au lieu de 
                          celle de l'original. À spécifier sans le "point" de début d'une 
                          extension.
    
    :rtype: string
    :return: Nouveau nom de fichier
    """
    if new_extension:
        extension = new_extension
    else:
        extension = splitext(filename)[1][1:]
    if not new_filename:
        now = real_datetime.now()
        return '%s%s%s%s.%s' % (unicode(now.hour).zfill(2), unicode(now.minute).zfill(2), unicode(now.second).zfill(2), unicode(now.microsecond).zfill(6), extension)
    else:
        return '%s.%s' % (new_filename, extension)

def generate_valid_path(filename, path, create_it=True, root_base=settings.MEDIA_ROOT, permissions=settings.FILE_UPLOAD_PERMISSIONS):
    """
    Génére le chemin prévu pour un fichier et créé le chemin si besoin
    
    :type filename: string
    :param filename: Nom du fichier cible
    
    :type path: string
    :param path: Chemin relatif (au répertoire des médias, ``settings.MEDIA_ROOT``) du 
                 répertoire contenant le fichier, peut contenir les paramètres de 
                 substitution possibles avec la méthode 
                 ``django.utils.datetime_safe.strftime``.
    
    :type create_it: bool
    :param create_it: (optional) Déclenche la création du répertoire si il n'existe pas déja
    
    :type root_base: string
    :param root_base: (optional) Chemin de base ou créer le fichier, par défaut dans 
                      le ``MEDIA_ROOT`` du projet.
    
    :type permissions: int
    :param permissions: (optional) Permission chmod sur le chemin à créer, par 
                             défaut utilise le ``FILE_UPLOAD_PERMISSIONS`` des settings 
                             du projet. Et si cette variable n'est pas renseigné dans vos 
                             settings, alors un mask 0744 sera utilisé.
    
    :rtype: tuple
    :return: * Chemin relatif du fichier
             * Chemin absolu du fichier
    """
    if not permissions:
        permissions = 0744
    # Forme le chemin absolu vers le nouvo fichier créé
    relative_path = strftime(real_datetime.now(), path)
    absolute_path = join(root_base, relative_path)
    # Création du répertoire
    if create_it:
        if not exists( absolute_path ):
            makedirs(absolute_path, permissions)
        elif not isdir( absolute_path ):
            # Le chemin existe et n'est pas un répertoire
            raise IOError("'%s' exists and is not a directory." % absolute_path)
    
    return join(relative_path, filename), join(absolute_path, filename)
