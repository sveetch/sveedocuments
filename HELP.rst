.. _ReStructuredText: http://docutils.sourceforge.net/rst.html

.. contents::

L'édition se fait uniquement dans la syntaxe de `ReStructuredText`_, l'insertion directe de HTML 
n'est en général pas permise.

Syntaxe de ReStructuredText
===========================

Le principe de `ReStructuredText`_ (ou **ReST**) est de pouvoir rédiger son contenu en texte brut sans 
balisages avec une syntaxe évoluée qui permet de conserver un aspect lisible et une mise en évidence 
de l'information.

Il y a deux types d'éléments de syntaxe, les éléments dits *en ligne* comme la mise en gras ou en 
italique et les éléments du types *blocs* tel qu'un paragraphe ou une liste à puce. Sur ces derniers la 
chose principale à retenir est de toujours respecter l'indentation lors de vos retours à la ligne explicites.

Vous pouvez retrouver les documentations originales de RestructuredText pour plus de détails si besoin (tous 
en anglais) :

* `Introduction à la syntaxe <http://docutils.sourceforge.net/docs/user/rst/quickstart.html>`_; 
* `Référence rapide de la syntaxe <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_;
* `Un Résumé de la syntaxe en version texte <http://docutils.sourceforge.net/docs/user/rst/cheatsheet.txt>`_;
* `Spécification complète de la syntaxe <http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html>`_.

Éléments en lignes
******************

Les éléments communs de mise en forme tel que :

* La mise en **gras** avec ``**gras**``;
* La mise en *italique* avec ``*italique*``;
* La mise en ``code littéral`` avec ````code littéral````;

Liens
*****

Il y a diverses possibilités de créer des liens et de différents types. Avec `ReStructuredText`_ on utilise plutôt le 
terme de **référence** au lieu de lien.

Lien externe direct
-------------------

Pour un simple lien ponctuel on utilise une **référence externe directe** : ::

  Mon texte avec mon `Lien <http://perdu.com/>`_ et voila.

Référence interne
-----------------

Dès lors que vous comptez utiliser une même URL plusieurs fois dans un même document, il faut utiliser une **référence 
interne** qui s'apparente une ancre sauf qu'elle peut faire référence aussi bien à une position dans le document (là 
où elle a été définie) qu'à une URL.

Par exemple : ::

  .. _Mon lien perdu: http://perdu.com

Pourra ensuite être utilisé comme une référence interne de la façon suivante : ::

  Mon texte avec mon `Mon lien perdu`_ et voila.

Si vous utilisez plusieurs fois une même URL (on parle bien d'URL complète et pas simplement de son 
domaine), `ReStructuredText`_ vous en avertira.

Ancre
-----

Comme annoncé plus haut, vous pouvez aussi créer une référence interne qui servira d'ancre à la position 
ou elle a été définie.

Par exemple : ::

  .. Ma super position:
  
  Mon texte lorem ipsum.
  
  ...

Permettra d'utiliser la référence interne comme une ancre de la façon suivante : ::

  Vous pouvez retrouver plus de détails à `Ma super position`_.

À noter qu'il est inutile de créer des références internes pour les `Titres`_ car ils le sont tous 
déjà automatiquement.

Éléments en blocs
*****************

Généralement tout les éléments en blocs doivent être séparés par une ligne vide (ou contenant juste 
l'indentation en cours) sinon il y a risque de confusion dans la mise en forme. De fait si vous 
respectez cette indentation vous pouvez aussi imbriquer plusieurs blocs différents.

Le bloc le plus simple est le paragraphe, c'est celui par défaut lorsque vous rédigez simplement 
votre contenu sans indentation ou autre préfixe de ligne ou de *directive*. À noter que 
`ReStructuredText`_ ne tient pas compte de vos retours de ligne dans vos paragraphes par 
exemple la source suivante : ::

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

Les titres tiennent sur une ligne et doivent être complètement souslignés sur toute leur longueur, 
par exemple : ::

  Titre 1
  =======
  
  Mon texte..

Et valide, mais pas l'élément suivant : ::

  Titre 1
  =====
  
  Mon texte..
    
Un titre ouvre ce qu'on apelle une **section**. Lorsque vous ouvrez un titre dans une section, cela ouvre une 
sous section et ainsi de suite jusqu'à un autre titre. Mais sauf cas particulier, ceci vous est totalement transparent.

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

  ..  sourcecode:: javascript
      :linenos:
  
      function foobar(arg) {
          var foo = 'bar';
          var bar = arg*5;
          return false;
      };
      
      FOO = {
        toto: true,
        hello: 'world'
      };

Donnera :

..  sourcecode:: javascript

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

  ..  sourcecode:: python
      :linenos:
      :hl_lines: 1,6
  
      class foobar(object):
        def __init__(self, dummyarg):
          self.plop = True
      
      FOO = {
        'toto': True,
        'hello': 'world',
      }

Donnera :

..  sourcecode:: python
    :linenos:
    :hl_lines: 1,6

    class foobar(object):
      def __init__(self, dummyarg):
        self.plop = True
    
    FOO = {
      'toto': True,
      'hello': 'world',
    }
