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
.. _rst2pdf: http://code.google.com/p/rst2pdf/

Introduction
============

**Sveetchies-documents** is a Django application to manage text documents. It work almost like a Wiki.

Features
--------

* Usage of the `ReStructuredText`_ docutils parser;
* Templates builded with `Foundation5`_;
* Rich editor `djangocodemirror`_;
* Nice forms with `django-crispy-forms`_;
* Usage of `autobreadcrumbs`_;
* Optional usage of Assets bundles with `django-assets`_;
* Usage of the Django cache system for the parser rendering;
* A management board ready to use in frontend;
* Two kind of documents :

  * Page : For full page documents with children pages in a sitemap tree;
  * Insert : For documents to insert as fragment in your templates;

* Simple collaborative way (History, authoring) for Pages;
* Templatetags to use documents in your templates;
* Fully internationalized;

Links
-----

* Download his `PyPi package <http://pypi.python.org/pypi/sveedocuments>`_;
* Clone it on his `Github repository <https://github.com/sveetch/sveedocuments>`_;

Requires
--------

* Django >= 1.5;
* `docutils`_ >= 0.7;
* `rstview`_ >= 0.2;
* `autobreadcrumbs`_ >= 1.0;
* `djangocodemirror`_ >= 0.9.4;
* `django-mptt`_ >= 0.5.2;
* `crispy-forms-foundation`_ >= 1.4.0;
* `django-braces`_ >= 1.3.0;

Optionnally :

* `django-assets`_ to use Assets bundles instead of plain assets, you will have to load these bundles instead of raw asset files, perform this with overriding ``sveedocuments/assets_css.html`` and ``sveedocuments/assets_js.html`` in your project templates directory.
* `South`_ to perform database migrations for next releases;

Install
=======

Add it to your installed apps in settings : ::

    INSTALLED_APPS = (
        ...
        'autobreadcrumbs',
        'djangocodemirror',
        'rstview',
        'mptt',
        'sveedocuments',
        ...
    )

Also you can overrides app settings to change some behaviors, see ``sveedocuments.local_settings`` to see what you can override in your project settings like ``DOCUMENTS_PAGE_TEMPLATES`` to add new templates to use to build your pages.

Finally mount its urls into your main ``urls.py`` : ::

    urlpatterns = patterns('',
        ...
        (r'^documents/', include('sveedocuments.urls', namespace='sveedocuments')),
        ...
    )

Usage
=====

Signals
-------

sveedocuments use Django signals to send signals when ``Page`` or ``Insert`` is updated (when created or edited), you can listen to them to perform some tasks. These signals are :

* ``sveedocuments.models.documents_page_update_signal`` for ``Page`` updates;
* ``sveedocuments.models.documents_insert_update_signal`` for ``Insert`` updates;

