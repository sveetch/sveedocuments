.. _ReStructuredText: http://docutils.sourceforge.net/rst.html
.. _django-uni-form: https://github.com/pydanny/django-uni-form

Introduction
============

**Sveetchies-documents** is a Django application to manage text documents. It work almost like a Wiki 
except the collaborative way.

You can download it on his `Github repository <https://github.com/sveetch/sveedocuments>`_ and find 
his `documentation on DjangoSveetchies <http://sveetchies.sveetch.net/sveedocuments/>`_.

Features
********

* Usage of the `ReStructuredText`_ docutils parser;
* Rich editor **djangocodemirror**;
* Ergonomic form with `django-uni-form`_;
* Usage of **autobreadcrumbs** in *Pages* templates;
* Usage of the Django cache system for the parser rendering;
* Management board ready to use;
* Two kind of documents :

  * Page : For documents in full page with children pages in a sitemap tree;
  * Insert : For documents to insert as fragment in your templates;

* Templatetags to use documents in your templates;

Requires
========

* Python >= 2.6;
* `Django <https://www.djangoproject.com/>`_ >= 1.3.x;
* `docutils <http://docutils.sourceforge.net/>`_ >= 0.7;
* `django-uni-form`_ >= 0.9.x;
* `django-mptt <http://pypi.python.org/pypi/django-mptt/>`_ >= 0.5.2;
* `Pygments <http://pygments.org/>`_ >= 1.2.x (optionnel);

