.. _docutils: http://docutils.sourceforge.net/
.. _Django: https://www.djangoproject.com/
.. _Django internationalization system: https://docs.djangoproject.com/en/dev/topics/i18n/
.. _django-crispy-forms: https://github.com/maraujop/django-crispy-forms
.. _django-mptt: http://pypi.python.org/pypi/django-mptt/
.. _ReStructuredText: http://docutils.sourceforge.net/rst.html
.. _Pygments: http://pygments.org/

============
Introduction
============

**Sveetchies-documents** is a Django application to manage text documents. It work almost like a Wiki 
except the collaborative way.

Features
========

* Usage of the `ReStructuredText`_ docutils parser;
* Rich editor **djangocodemirror**;
* Ergonomic form with `django-crispy-forms`_;
* Usage of **autobreadcrumbs** in *Pages* templates;
* Usage of the Django cache system for the parser rendering;
* Management board ready to use;
* Two kind of documents :

  * Page : For full page documents with children pages in a sitemap tree;
  * Insert : For documents to insert as fragment in your templates;

* Templatetags to use documents in your templates;
* Fully internationalized;

Links
=====

* Download his `PyPi package <http://pypi.python.org/pypi/sveedocuments>`_;
* Clone it on his `Github repository <https://github.com/sveetch/sveedocuments>`_;
* Documentation and demo to come on his `DjangoSveetchies page <http://sveetchies.sveetch.net/sveedocuments/>`_.

Requires
========

* Python >= 2.6;
* `Django`_ >= 1.3.x;
* `docutils`_ >= 0.7;
* `django-crispy-forms`_ >= 1.1.x;
* `django-mptt`_ >= 0.5.2;
* `Pygments`_ >= 1.2.x (optionnel);

Internationalization and localization
=====================================

This application make usage of the `Django internationalization system`_, see the Django documentation about this if 
you want to add a new language translation.


=======
Install
=======

.. _ReStructuredText: http://docutils.sourceforge.net/rst.html

In your project
===============

Settings
********

First, register the application and his dependancies in your project settings like this :

::

    INSTALLED_APPS = (
        ...
        'mptt',
        'crispy_forms',
        'autobreadcrumbs',
        'djangocodemirror',
        'sveedocuments',
        ...
    )

Then you have to add the context processor of **autobreadcrumbs** in your settings :

::

    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        'autobreadcrumbs.context_processors.AutoBreadcrumbsContext',
        ...
    )

Application settings
--------------------

All default app settings is located in the ``settings_local.py`` file of ``sveedocuments``, you can modify them in 
your project settings.

.. NOTE:: All app settings are overwritten if present in your project settings with the exception of 
          dict variables. This is to be remembered when you want to add a new entry in a list variable, you will have to 
          copy the default version in your settings with the new entry otherwise default variable will be lost.

Urls
****

You have to add the application urls to your project, for this the easy way is to include the shipped urls like 
this :

::

    urlpatterns = patterns('',
        ...
        (r'^documents/', include('sveedocuments.urls')),
        ...
    )

If needed you can change the mounting directory ``documents/`` to another. For more possibilities you can define your own 
urls for sveedocuments views. *(More details to come)*

Database synchronization
************************

The application is now installed in your project, you just need to add his tables to your database, you have to do this 
with the ``django-admin`` command line : ::

    django-admin syncdb

Known Problems and Fixes
========================

There is a minor bug in Django with `ReStructuredText`_ when the ``django.contrib.admindocs`` is enabled in your project and 
some application directives or roles are used with the parser. See the `bug entry <https://code.djangoproject.com/ticket/6681>`_ 
for more details.

Nevertheless it does not happen using a default configuration so you don't have to worry about this, as long as the exception described 
in the bug entry is not raised.

If it happens you have two choices, the first one (not recommended) is to patch the ``django/contrib/admindocs/utils.py`` file in your 
Django installation, just comment the line below :

::
    
    docutils.parsers.rst.roles.DEFAULT_INTERPRETED_ROLE = 'cmsreference'

The second choice, is simply to disable ``django.contrib.admindocs`` by removing it from ``settings.INSTALLED_APPS`` and your 
``urls.py`` project. But this is only if you don't need of *admindocs*.

