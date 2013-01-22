.. _rstview: http://pypi.python.org/pypi/rstview
.. _autobreadcrumbs: http://pypi.python.org/pypi/autobreadcrumbs
.. _docutils: http://docutils.sourceforge.net/
.. _Django: https://www.djangoproject.com/
.. _Django internationalization system: https://docs.djangoproject.com/en/dev/topics/i18n/
.. _djangocodemirror: http://pypi.python.org/pypi/djangocodemirror
.. _django-crispy-forms: https://github.com/maraujop/django-crispy-forms
.. _django-assets: http://pypi.python.org/pypi/django-assets
.. _crispy-forms-foundation: https://github.com/sveetch/crispy-forms-foundation
.. _django-mptt: http://pypi.python.org/pypi/django-mptt
.. _django-braces: https://github.com/brack3t/django-braces
.. _ReStructuredText: http://docutils.sourceforge.net/rst.html
.. _Pygments: http://pygments.org/
.. _Foundation: http://github.com/zurb/foundation
.. _rst2pdf: http://code.google.com/p/rst2pdf/

Introduction
============

**Sveetchies-documents** is a Django application to manage text documents. It work almost like a Wiki.

Features
********

* Usage of the `ReStructuredText`_ docutils parser;
* Templates builded with `Foundation`_;
* Rich editor `djangocodemirror`_;
* Ergonomic form with `django-crispy-forms`_;
* Usage of `autobreadcrumbs`_ in *Pages* templates;
* Usage of the Django cache system for the parser rendering;
* Optional usage of Assets bundles with `django-assets`_;
* A management board ready to use in frontend;
* Two kind of documents :

  * Page : For full page documents with children pages in a sitemap tree;
  * Insert : For documents to insert as fragment in your templates;

* Simple collaborative way (History, authoring) for Pages;
* Optional PDF export for Pages if `rst2pdf`_ is installed;
* Templatetags to use documents in your templates;
* Fully internationalized;

Links
*****

* Download his `PyPi package <http://pypi.python.org/pypi/sveedocuments>`_;
* Clone it on his `Github repository <https://github.com/sveetch/sveedocuments>`_;
* Documentation and demo on `DjangoSveetchies page <http://sveetchies.sveetch.net/sveedocuments/>`_.

Requires
========

* `docutils`_ >= 0.7;
* `rstview`_;
* `autobreadcrumbs`_;
* `djangocodemirror`_;
* `django-mptt`_ >= 0.5.2;
* `django-crispy-forms`_ >= 1.1.x;
* `crispy-forms-foundation`;
* `django-braces`_;

Optionnally, to use Assets bundles instead of plain assets, you can install `django-assets`_.

Internationalization and localization
=====================================

This application make usage of the `Django internationalization system`_, see the Django documentation about this if 
you want to add a new language translation.

