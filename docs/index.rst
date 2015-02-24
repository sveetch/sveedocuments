.. Sveedocuments documentation master file, created by
   sphinx-quickstart on Mon Feb 23 03:47:19 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _Django: https://www.djangoproject.com/
.. _Django internationalization system: https://docs.djangoproject.com/en/dev/topics/i18n/
.. _South: http://south.readthedocs.org/en/latest/
.. _rstview: http://pypi.python.org/pypi/rstview
.. _autobreadcrumbs: http://pypi.python.org/pypi/autobreadcrumbs
.. _docutils: http://docutils.sourceforge.net/
.. _djangocodemirror: http://pypi.python.org/pypi/djangocodemirror
.. _django-crispy-forms: https://github.com/maraujop/django-crispy-forms
.. _django-assets: http://pypi.python.org/pypi/django-assets
.. _crispy-forms-foundation: https://github.com/sveetch/crispy-forms-foundation
.. _django-mptt: http://pypi.python.org/pypi/django-mptt
.. _django-braces: https://github.com/brack3t/django-braces
.. _ReStructuredText: http://docutils.sourceforge.net/rst.html
.. _Pygments: http://pygments.org/
.. _Foundation5: http://foundation.zurb.com/docs/
.. _django-sendfile: https://github.com/johnsensible/django-sendfile

Welcome to Sveedocuments's documentation!
=========================================

**Sveetchies-documents** is a Django application to manage text documents. It work almost like a Wiki.

Features
********

* Usage of the `ReStructuredText`_ docutils parser;
* Templates builded with `Foundation5`_;
* Rich editor `djangocodemirror`_;
* Nice forms with `django-crispy-forms`_;
* Usage of `autobreadcrumbs`_;
* Optional usage of Assets bundles with `django-assets`_;
* Usage of the Django cache system for Markup parser and renderer;
* A management board ready to use in frontend;
* Two kind of documents :

  * Page : For full page documents with children pages in a sitemap tree;
  * Insert : For documents to insert as fragment in your templates;

* Simple collaborative way (History, authoring) for Pages;
* Templatetags to use documents in your templates;
* Internationalized interface (English and French for now);
* Optional usage of `django-sendfile`_ for page's attachments when page are restricted to loggued users;

Links
*****

* Read the documentation on `Read the docs <https://sveedocuments.readthedocs.org/>`_;
* Download his `PyPi package <http://pypi.python.org/pypi/sveedocuments>`_;
* Clone it on his `Github repository <https://github.com/sveetch/sveedocuments>`_;

Table of contents
*****************

.. toctree::
   :maxdepth: 2
   
   install.rst
   usage.rst
