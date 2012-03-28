============
Introduction
============

**Sveetchies-documents** est une brique logicielle de gestions de documents textes pour 
Django.

Son principe de base repose en partie sur celui d'un Wiki mais sans système de révisions 
ni d'utilisation collaborative. C'est en fait une évolution de 
`Kiwi <http://kiwi.sveetch.net/>`_, simplifiée pour tenir dans sa propre brique intégrable 
aisément dans un projet existant et utilisant exclusivement le parser **ReStructuredText** 
de docutils.

Fonctionnalités
===============

* Utilisation du parser `ReStructuredText <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_;
* Éditeur de texte enrichi avec `CodeMirror <http://codemirror.net/>`_;
* Interface de gestion prête à l'emploi;
* Formulaires ergonomiques grâce à **django-uni-form**;
* Gestion de deux types de documents :

  * Page : Des pages HTML complètes dans une arborescence avec possibilité de 
    publication programmée;
  * Document à insérer : Des documents n'apparaissant dans aucune arborescence et qui 
    peuvent être intégrés à d'autres pages de n'importe quelle autre application de 
    vos projets;

* Utilisation du système de cache de Django pour la génération du rendu HTML des 
  documents par le parser ReST;
* Chemin d'accès (ou *pathline* ou *breadcrumbs*) toujours disponible grâce à 
  ``Sveetchies.django.autobreadcrumbs`` pour la gestion du chemin d'accès (pathline/breadcrumbs);
* Multiples *Template tags* pour utiliser les documents dans vos projets;
* Avertissement des problèmes de syntaxe détectés par le parser lors de la soumission du 
  formulaire d'un document, pour empêcher de publier tout document avec une erreur de 
  syntax;

Pré-requis
==========

* Python >= 2.6;
* `Django <https://www.djangoproject.com/>`_ >= 1.3.x;
* `docutils <http://docutils.sourceforge.net/>`_ >= 0.7;
* `django-uni-form <http://pypi.python.org/pypi/django-uni-form/0.9.0>`_ >= 0.9.x;
* `django-mptt <http://pypi.python.org/pypi/django-mptt/>`_ >= 0.5.2;
* `Pygments <http://pygments.org/>`_ >= 1.2.x (optionnel);

============
Installation
============

Intégration dans votre projet
=============================

**Sveetchies-documents** est une simple brique logicielle à intégrer dans un projet ou 
plateforme web sous Django, en lui-même il ne permet pas de produire directement un site.

Après avoir installé tout les pré-requis, il vous faut l'intégrer à votre projet sous 
Django.

Modification de vos Settings
****************************

INSTALLED_APPS
--------------

La première étape est de modifier les *settings* de votre application, d'abord avec 
``INSTALLED_APPS`` en y rajoutant ces deux lignes : ::

    INSTALLED_APPS = (
        ...
        'Sveetchies.django.autobreadcrumbs',
        'Sveetchies.django.documents',
        ...
    )

AUTOBREADCRUMBS_TITLES
----------------------

Vous pouvez ne pas utiliser ``autobreadcrumbs`` mais il vous faudra modifier les templates 
pour en retirer la mention de ses *template tags*. Si par contre vous l'utilisez, il vous 
faudra aussi ajouter dans les ``settings`` la partie configurant les titres des chemins : ::

    AUTOBREADCRUMBS_TITLES = {
        'documents-index': u'Plan du site',
        'documents-board': u'Administration des documents',
        'documents-insert-add': u'Nouveau document à insérer',
        'documents-insert-delete': u'Supprimer le document #{{ insert_instance.slug }}',
        'documents-insert-edit': u'Editer le document #{{ insert_instance.slug }}',
        'documents-page-add': u'Nouvelle page',
        'documents-page-delete': u'Supprimer la page #{{ page_instance.slug }}',
        'documents-page-edit': u'Editer la page #{{ page_instance.slug }}',
    }

Vous pouvez y modifier les titres si besoin, notez que les titres utilisent le système de 
variables et tags de Django. Si vous avec déjà un ``settings.AUTOBREADCRUMBS_TITLES`` rempli, 
mixez simplement le code précédant avec le votre.

TEMPLATE_DIRS
-------------

Vous devez enregistrer l'emplacement des templates de *Sveetchies-documents* dans vos settings : ::

    TEMPLATE_DIRS = (
        ...
        '/home/foo/Sveetchies/src/django/documents/templates/documents/',
        ...
    )

Le chemin est à modifier selon l'emplacement de votre installation de **Sveetchies**.

STATICFILES_DIRS
----------------

Vous devez enregistrer l'emplacement des fichiers statiques de *Sveetchies-documents* dans vos settings : ::

    STATICFILES_DIRS = (
        ...
        '/home/foo/Sveetchies/src/django/documents/static/',
        ...
    )

Le chemin est à modifier selon l'emplacement de votre installation de **Sveetchies**.

Autres
------

Ensuite si besoin, il existe quelques options de fonctionnement que vous pouvez modifier 
depuis les settings, pour cela consulter le fichier ``documents/__init__.py`` où chaque option 
est résumée. Ne modifiez rien dans ce fichier, pour *écraser* ces options remplissez les 
simplements dans vos settings.

Urls
****

Il faut ensuite insérer la *map* des urls dans votre projet, la pratique la plus simple est 
d'utiliser celle déjà intégrée à *Sveetchies-documents* dans le fichier ``urls.py`` à la racine de votre 
projet de la manière suivante : ::

    urlpatterns = patterns('',
        ...
        (r'^documents/', include('Sveetchies.django.documents.urls')),
        ...
    )

Vous pouver utiliser un autre chemin que ``documents/`` si besoin. Pour des besoins plus spécifiques vous
pouvez redéfinir la *map* des pages et garder celles de l'interface de gestion des documents (voir la 
page `Utilisation`_.

Synchronisation des données de la brique logicielle
***************************************************

À ce stade la brique est installée et prête à l'emploi dans votre projet, il ne reste qu'à utiliser 
la commande de synchronisation pour ajouter ses modèles en base données : ::

    django-admin syncdb

Démonstration
=============

**Sveetchies** contient une démonstration dans son répertoire ``demo/`` qui repose en partie 
**Sveetchies-documents**.

Settings
********

En général, on évite de modifier le fichier de *settings* livré pour éviter toute perte en cas de mise 
à jour. On préfère dupliquer le fichier original et le modifier, il suffit ensuite de le spécifier dans 
toute les commandes de ``django-admin`` en utilisant l'option ``--settings`` par exemple avec un fichier 
``dev_settings.py`` : ::

  django-admin COMMAND --settings=dev_settings

On peut aussi faire plus simple, il suffit de créer votre fichier, d'y importer les ``settings`` 
du fichier original et les *écraser*.

L'exemple suivant montre un fichier de settings pour une utilisation en production, dans un fichier 
``prod_settings.py`` : ::

    # -*- coding: utf-8 -*-
    """
    Django settings for Sveetchies demo
    
    For production environnment, using the default project settings
    """
    from settings import *
    
    # WEBAPP_ROOT must be manually specified in production
    WEBAPP_ROOT = "/home/django/projects/Sveetchies/demo/"
    
    # Database access
    DATABASES = {
        'default': {
            'NAME': 'sveetchies',
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'USER': 'django',
            'PASSWORD': 'dj4ng0',
        }
    }
    
    # Make this unique, and don't share it with anybody.
    SECRET_KEY = 'long_key'
    
    # SMTP Settings to send Applications error, uncomment to active mail sending
    #EMAIL_HOST = 'localhost'
    #EMAIL_SUBJECT_PREFIX = '[Sveetchies] '
    #SERVER_EMAIL = 'Sveetchies errors <your@email>'
    #DEFAULT_FROM_EMAIL = 'Sveetchies <your@email>'
    
    # Emails receiver for errors if SMTP settings are actived
    #ADMINS = (
        #('YourName', 'your@email'),
    #)
    
    # Disable all debug mode
    DEBUG = False
    TEMPLATE_DEBUG = DEBUG
    UNIFORM_FAIL_SILENTLY = not DEBUG
    
    # Another site ID than default
    SITE_ID = 1
    
    # Adapt for WEBAPP_ROOT and STATIC_DIRNAME changes
    MEDIA_ROOT = os.path.join(WEBAPP_ROOT, MEDIA_DIRNAME)+"/"
    STATIC_DIRNAME = '_statics'
    STATIC_URL = '/{0}/'.format(STATIC_DIRNAME)
    STATIC_ROOT = os.path.join(WEBAPP_ROOT, STATIC_DIRNAME)+"/"
    STATICFILES_DIRS = (
        os.path.join(WEBAPP_ROOT, 'webapp_statics/'),
        os.path.join(SVEETCHIES_PATH_INSTALL, 'django/documents/static/'),
    )
    ADMIN_MEDIA_PREFIX = os.path.join('/', STATIC_DIRNAME, 'admin/')
    TEMPLATE_DIRS = (
        os.path.join(WEBAPP_ROOT, 'templates/'),
        os.path.join(SVEETCHIES_PATH_INSTALL, 'django/documents/templates/documents/'),
    )
    
    # Disable the DebugToolbar in production
    MIDDLEWARE_CLASSES = tuple([item for item in list(MIDDLEWARE_CLASSES) if item != 'debug_toolbar.middleware.DebugToolbarMiddleware'])
    INSTALLED_APPS = tuple([item for item in list(INSTALLED_APPS) if item != 'debug_toolbar'])
    
Les lignes mises en surbrillance sont les seules que vous avez à modifier, tout le reste nécessaire 
est automatiquement mis en place :

* ``WEBAPP_ROOT`` est le chemin absolu vers le répertoire de votre installation de la démonstration qui 
  contient au moins le fichier de *settings* et celui des *urls*.
* ``DATABASES`` contient la configuration d'accès à votre base de données, référez vous à la 
  `documentation Django sur settings.DATABASES <https://docs.djangoproject.com/en/dev/ref/settings/#databases>`_ 
  pour un détails des possibilités;
* ``SECRET_KEY`` est une longue chaine de caractères variés qui sert à encrypter certaines données comme 
  les sessions ou les mots de passes utilisateurs prenez exemple de celle fourni dans les settings par 
  défaut mais rendez la bien différente;

Optionnellement, vous pouvez renseigner les options concernant l'envoi SMTP et ``settings.ADMINS`` 
pour recevoir des notifications d'erreurs (Http500) par email.

Notez aussi ``SITE_ID`` est à la valeur ``1``, par convention on utilise cette valeur pour la 
version en développement. Mais vous pouvez la changer si besoin, mais il vous faut d'abord créer son entrée 
correspondante depuis l'administration de Django (via le chemin ``Accueil › Sites › Sites › Ajouter site``) 
ou modifier l'entrée par défaut créer lors de la **Synchronisation des données**.

Synchronisation des données de la démonstration
***********************************************

Vous pouvez l'installer en renseignant correctement les ``settings`` (à faire dans un autre fichier, 
par exemple ``prod_settings.py``) puis lancer une synchronisation des données : ::

  django-admin syncdb --settings=prod_settings

Répondez positivement à la demande de création d'un super utilisateur, puis lorsque le processus s'est achevé 
correctement il faut charger les données de la démonstration : ::

  django-admin loaddata --settings=prod_settings demo_data.json

Déploiement en production
*************************

Si vous souhaitez utiliser la démonstration autrement qu'avec le serveur de développement intégré de Django, 
vous devrez penser à collecter les fichiers statiques (css, images, etc..) avec la commande : ::

  django-admin collectstatic --settings=prod_settings

Pour plus d'informations référez vous à la 
`documentation Django sur la commande collectstatic <https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#collectstatic>`_.

Ensuite déployez le projet sur le serveur web de votre choix, pour cela référez vous à 
la `documentation de Django sur le déploiement <https://docs.djangoproject.com/en/dev/howto/deployment/>`_. 
La démonstration en ligne de ce site utilise FastCGI, probablement le plus simple à mettre en place.


===========
Utilisation
===========

Urls
====

Pour des cas plus particuliers par exemple si vous souhaitez utiliser uniquement cette 
brique à la racine de votre site, il vous faudra alors insérer et modifier chaque 
directives dans votre ``urls.py`` par exemple : ::

    from Sveetchies.django.documents.views.page import PageIndex, PageDetails, PageSource
    
    urlpatterns = patterns('',
        url(r'^$', PageIndex.as_view(), name='documents-index'),
        
        (r'^board/', include('Sveetchies.django.documents.urls_board')),
    
        url(r'^sitemap/$', PageIndex.as_view(), name='documents-index'),
        
        url(r'^(?P<slug>[-\w]+)/$', PageDetails.as_view(), name='documents-page-details'),
        url(r'^(?P<slug>[-\w]+)/source/$', PageSource.as_view(), name='documents-page-source'),
        ...
    )

L'interface d'administration des documents et ses autres pages se trouvent dans ``board/``, mais 
vous pouvez modifier son nom si besoin. Pour des besoins encore plus particuliers, vous pouvez aussi 
intégrer une version modifiée de ``urls_board``.

Views
=====

Les urls utilisent les vues suivantes, toute celles liés à l'interface de gestion sont 
en général protégés par des permissions utilisateur.

documents-index
  Le plan du site listant l'arborescence complète des pages visibles.
documents-preview
  Vue permettant la réception d'un POST de contenu à rendre avec le parser, sert à la 
  prévisualisation, c'est une ressource protégée nécessitant d'être identifié.
documents-board
  Interface de gestion des documents, c'est une ressource protégée nécessitant d'être 
  identifié.
documents-page-add
  Formulaire de création d'une nouvelle page, ressource protégée nécessitant d'être 
  identifié et avec la permission de créer des pages.
documents-page-edit
  Formulaire d'édition d'une page, ressource protégée nécessitant d'être identifié et 
  avec la permission de modifier des pages.
documents-page-delete
  Formulaire de suppression d'une page (et éventuelles sous-pages), ressource protégée 
  nécessitant d'être identifié et avec la permission de supprimer des pages.
documents-insert-add
  Formulaire de création d'un document insérable, ressource protégée nécessitant d'être 
  identifié et avec la permission de créer des documents insérables.
documents-insert-edit
  Formulaire d'édition d'un document insérable, ressource protégée nécessitant d'être 
  identifié et avec la permission de modifier des documents insérables.
documents-insert-delete
  Formulaire de suppression d'un document insérable, ressource protégée nécessitant d'être 
  identifié et avec la permission de supprimer des documents insérables.
documents-page-details
  Vue pour afficher la page avec son contenu.
documents-page-source
  Vue pour afficher la source *brute* du contenu sans aucun rendu par le parser.

Templates
=========

Tout les gabarits se trouvent dans le répertoire ``templates/documents/`` de votre 
installation de **Sveetchies-documents**. Pour utiliser vos propres gabarit, il suffit de 
les créer sous le même nom dans le répertoire ``templates/documents/`` de votre projet.

page_index.html
  Plan du site, utilisé par la vue ``documents-index``.
board.html
  Index de l'interface de gestion, utilisé par la vue ``documents-board``.
page_form.html
  Formulaire d'une page, utilisé par les vues ``documents-page-add`` 
  et ``documents-page-edit``.
page_delete.html
  Formulaire de suppression d'une page, utilisé par la vue ``documents-page-delete``.
insert_form.html
  Formulaire d'un document insérable, utilisé par les vues ``documents-insert-add`` 
  et ``documents-insert-edit``.
insert_delete.html
  Formulaire de suppression d'un document insérable, utilisé par la 
  vue ``documents-page-delete``.
editor_supercodemirror_includes.html
  Fragment de code inclus automatiquement dans les formulaires pour utiliser 
  l'éditeur ``CodeMirror``.
editor_markitup_includes.html
  Fragment de code inclus automatiquement dans les formulaires pour utiliser 
  l'éditeur ``MarkItUp``.
page_details/default.html
  Gabarit simple pour afficher une page.  
page_details/columned_bytwo.html
  Gabarit prévu pour fonctionner sur deux colonnes, la première pour le contenu et la 
  seconde pour le sommaire des titres et la navigation des sous-pages.  
page_treemenu.html
  Fragment pour générer un menu d'arborescence de pages. Utilisé par défaut lors 
  de l'usage du template tag ``document_page_treemenu``.
page_flatmenu.html
  Fragment pour générer un menu des pages adjacentes. Utilisé par défaut lors de 
  l'usage du template tag ``document_page_flatmenu``.

Templates tags et filtres
=========================

Les différentes filtres et tags disponibles dans les gabarits dès lors qu'ils ont 
été importés.

documents_markup
****************

À importer dans vos templates via la balise ``{% load documents_markup %}``.

source_render
  Filtre de rendu par le parser du texte fournit, accepte un argument optionnel pour spécifier 
  un nom clé de configuration de parser à utiliser par exemple ``{{ myvar|source_render:"mysettings" }}``.
document_render
  Filtre de rendu du contenu d'une instance de ``Page`` ou ``Insert``, accepte un argument optionnel pour 
  spécifier un nom clé de configuration de parser à utiliser par 
  exemple ``{{ page_instance|document_render:"mysettings" }}``. 
  Le contenu renvoyé est directement celui du parser sans ajout ni utilisation de gabarit.
document_toc
  Filtre générant le TOC (sommaire) des titres du contenus. Renvoi une arborescence sous forme 
  d'une liste à puce si le document contient bien des titres. Accepte les mêmes arguments 
  que ``document_render``.

documents_utils
***************

À importer dans vos templates via la balise ``{% load documents_utils %}``.

pprint_recurse
  Tag qui renvoi une liste à puce récursive de toute les relations d'un objet. C'est un tag 
  très particulier utilisé en interne pour lister les relations d'un objet lors de sa 
  suppression. En théorie vous n'avez pas utilité de ce tag.
document_insert
  Tag pour utiliser un document insérable dans n'importe quel autre template dans votre projet. 
  Nécessite un argument qui peut être soit une chaine de caractères contenant le *slug* du 
  document à utiliser, soit directement l'instance d'un document insérable. Deux arguments 
  optionnels sont possibles, le premier pour un nom clé de configuration de parser à utiliser, 
  le second pour un entier qui spécifie le niveau minimale des titres de premier niveau (à 3 
  il n'y aura jamais de ``h1`` ou de ``h2``). Notez que ce dernier argument permet d'écraser 
  une valeur déjà définie dans les configurations par défaut du parser.
document_page_treemenu
  Tag pour générer un menu d'arborescence de pages à partir d'un point donné (soit une Page, 
  soit la racine de toute les pages), l'arborescence n'inclue pas le point de départ (une 
  instance ou la racine). Requiert un argument pour spécifier soit un *slug* d'une page, soit 
  une instance de Page, soit ``0`` pour signifier de commencer à partir de la racine de 
  l'arborescence de toute les pages. Accepte un argument optionnel pour spécifier un gabarit 
  spécifique à utiliser autre que celui par défaut.
document_page_flatmenu
  Tag pour générer un menu des pages adjacentes d'une page ou de la racine (auquel cas ce ne 
  sont pas les pages adjacentes mais les pages de premier niveau). Accepte les mêmes 
  arguments que ``document_page_treemenu``.
document_context
  Tag générant le rendu, un sommaire des titres automatiques et la navigation sur les sous-pages 
  de la page en cours. Ce tag ne modifie pas ni n'injecte de html dans le template, à la place 
  les variables suivantes sont ajoutés dans le contexte du template :
  
  * ``document_toc`` : Fragment HTML d'une liste à puces récursive pour l'arborescence des 
    titres de la page;
  * ``document_navigation`` : Queryset des sous-pages de la page en cours, à exploiter avec la 
    méthode ``recursetree`` de ``mptt``;
  * ``document_render`` : Fragment HTML du rendu du contenu par le parser;
  
  Les éléments ``document_toc`` et ``document_render`` bénéficient du cache.

Éditeurs de texte
=================

Deux éditeurs de texte sont actuellement disponibles pour les formulaires, **MarkItUp** 
et **CodeMirror**, pour modifier ce choix par défaut, il suffit de 
renseigner ``settings.DOCUMENTS_EDITOR``, soit avec ``markitup``, soit ``codemirror``, 
soit ``None`` pour désactiver l'utilisation d'un éditeur (l'édition se fera dans un simple 
textarea conventionnel).

**CodeMirror** a le grand avantage de posséder une coloration syntaxique du texte. Une 
`Aide à l'édition`_ est disponible.

.. figure:: /static/docs/supercodemirror_editor.png
   :alt: CodeMirror en mode édition
   :class: left
   
   Le mode édition avec la coloration syntaxique du contenu en train d'être édité.

.. figure:: /static/docs/supercodemirror_preview.png
   :alt: CodeMirror en mode édition
   :class: left
   
   Le mode prévisualisation avec le contenu rendu par le parser.

**MarkItUp** est en phase *deprecation*.

Cache
=====

Le système utilise le cache de Django pour mettre en mémoire certains éléments de rendus 
liés au parser, aucune autre partie n'est mis en cache (transaction base de données, etc..).

La gestion du temps de vie de ces caches dépends de votre configuration de votre cache dans les settings, 
cependant une invalidation de cache est effectuée à chaque sauvegarde d'une instance ou de sa suppression.

Si votre projet ne nécessite pas d'utilisation du cache, il vous suffit de l'ignorer, par défaut si il n'est 
pas configuré dans les *settings*, Django n'utilise pas de cache.


================
Aide à l'édition
================

L'édition se fait uniquement dans la syntaxe de **ReStructuredText**, l'insertion directe de HTML 
n'est en général pas permise.

Syntaxe de ReStructuredText
===========================

Le principe de ReStructuredText (ou **ReST**) est de pouvoir rédiger son contenu en texte brut sans 
balisages avec une syntaxe évoluée qui permet de conserver un aspect lisible et une mise en évidence 
de l'information.

Il y a deux types d'éléments de syntaxe, les éléments dits *en ligne* comme la mise en gras ou en 
italique et les éléments du types *blocs* tel qu'un paragraphe ou une liste à puce. Sur ces derniers la 
chose principale à retenir est de toujours respecter l'indentation lors de vos retours à la ligne explicites.


Éléments en lignes
******************

Les éléments communs de mise en forme tel que :

* La mise en **gras** avec ``**gras**``;
* La mise en *italique* avec ``*italique*``;
* La mise en ``code littéral`` avec ````code littéral````;
* Un `lien externe <http://perdu.com>`_ avec ```lien externe <http://perdu.com>`_``;

Éléments en blocs
*****************

Généralement tout les éléments en blocs doivent être séparés par une ligne vide (ou contenant juste 
l'indentation en cours) sinon il y a risque de confusion dans la mise en forme. De fait si vous 
respectez cette indentation vous pouvez aussi imbriquer plus blocs différents.

Le bloc de plus simple est le paragraphe, c'est celui par défaut lorsque vous rédigez simplement 
votre contenu sans indentation ou autre préfixe de ligne ou de *directive*. À noter que ReST ne tient 
pas compte de vos retours de ligne dans vos paragraphes par exemple la source suivante : ::

  Nam ultrices venenatis tempus. 
  Sed amet.

Ne rend qu'un seul paragraphe :

  Nam ultrices venenatis tempus. Sed amet.

Alors que la source suivante : ::

  Nam ultrices venenatis tempus. 
  
  Sed amet.

Produit deux paragraphes :

  Nam ultrices venenatis tempus. 
  
  Sed amet.

Titres
------

Les titres peuvent se tenir sur une ligne ou plusieurs, l'important étant qu'ils soient souslignés 
sur toute leur longueur, par exemple : ::

  Titre 1
  =======
  
  Mon texte..

Et valide, mais pas l'élément suivant : ::

  Titre 1
  =====
  
  Mon texte..
    
Un titre ouvert ce qu'on apelle une **section**, qui en général reste invisible à l'affichage et n'est 
seulement spécifiée que dans le code HTML. Lorsque vous ouvrez un titre dans une section, cela ouvre une 
sous section et ainsi de suite jusqu'à un autre titre.

Tout les titres sont des références internes que vous pouvez utiliser comme lien interne au document par exemple : ::

  Un lien vers le titre `Éléments en blocs`_.

Donnera :

  Un lien vers le titre `Éléments en blocs`_.

Vous pouvez utiliser les caractères que vous souhaitez parmi ``=``, ``*``, ``-``, ``_``, ``#`` entre autres pour 
soulignés vos titres, ceci ne pointant pas vers un niveau de titre particulier car ce dernier est calculé 
automatiquement selon l'ordre d'utilisation dans ses *sections*.

Listes à puces et numérotées
----------------------------

Les listes à puces sont simplement déclarées en ajoutant respectivement ``*`` ou ``#.`` suivi d'un espace et 
votre texte pour une liste à puce ou une liste numérotée. Pour introduire une sous liste, il faut la séparer 
avec une ligne vide avant et après. Par exemple la source suivante : ::

  * élément 1
  * élément 2
  
    #. Sous élément 2.1
    #. Sous élément 2.2
  
  * élément 3
  * élément 4 avec un retour
    forcé à la ligne
  * élément 5

Donnera le résultat suivant :

  * élément 1
  * élément 2
  
    #. Sous élément 2.1
    #. Sous élément 2.2
  
  * élément 3
  * élément 4 avec un retour
    forcé à la ligne
  * élément 5

Citations
---------

Une citation se fait simplement en indentant chaque ligne de votre contenu, par exemple : ::

      Nam ultrices **venenatis** tempus. 
      *Sed amet*.

Rend une citation :

  Nam ultrices **venenatis** tempus. 
  *Sed amet*.

Texte préformaté
----------------

À la manière des citations, on peut citer du texte ou du code sans qu'il ne soit interprêté 
sur sa syntaxe par le parser, il suffit de précéder le contenu de ``::`` et d'indenter 
le contenu, par exemple : ::

  ::
  
    Praesent eget **nulla** vitae lectus nullam.
    
    * élément 1
    * élément 2
  
Donnera :
  
::

  Praesent eget **nulla** vitae lectus nullam.
  
  * élément 1
  * élément 2

Mais la façon la plus évidente est simplement d'ajouter ``::`` à la fin de la ligne du bloc 
précédant, par exemple : ::

  Mon annonce de citation préformatée : ::
  
    Praesent eget **nulla** vitae lectus nullam.

Donnera :

  Mon annonce de citation préformatée : ::
  
    Praesent eget **nulla** vitae lectus nullam.

Code source
-----------

Il est possible d'afficher un bloc de code source avec une coloration syntaxique selon son format. 
Ce bloc permet aussi de mettre en évidence certaines lignes du code source et d'afficher ou la 
numérotation des lignes.

Pour un code source en **Javascript** sans numérotation, la source suivante : ::

      function foobar(arg) {
          var foo = 'bar';
          var bar = arg*5;
          return false;
      };
      
      FOO = {
        toto: true,
        hello: 'world'
      };

Donnera : ::

    function foobar(dummyarg) {
        var foo = 'bar';
        var bar = dummyarg*5;
        return false;
    };
    
    FOO = {
      toto: true,
      hello: 'world'
    };

Ou pour un code source en **Python** avec numérotation des lignes et mise en évidence de 
certaines lignes : ::

      class foobar(object):
        def __init__(self, dummyarg):
          self.plop = True
      
      FOO = {
        'toto': True,
        'hello': 'world',
      }

Donnera : ::

    class foobar(object):
      def __init__(self, dummyarg):
        self.plop = True
    
    FOO = {
      'toto': True,
      'hello': 'world',
    }
