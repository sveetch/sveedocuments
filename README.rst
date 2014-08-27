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
.. _django-guardian: https://github.com/lukaszb/django-guardian
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
* Global or 'per object' moderation on categories, threads and messages;
* Internationalized (English and French for now);

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
* `django-guardian`_ >= 1.2.0;

Optionnally :

* `django-assets`_ to use Assets bundles instead of plain assets, you will have to load these bundles instead of raw asset files, perform this with overriding ``sveedocuments/assets_css.html`` and ``sveedocuments/assets_js.html`` in your project templates directory.
* `South`_ to perform database migrations for next releases;

Install
=======

Add it to your installed apps in your project settings : ::

    INSTALLED_APPS = (
        ...
        'autobreadcrumbs',
        'guardian',
        'djangocodemirror',
        'rstview',
        'mptt',
        'sveedocuments',
        ...
    )

Add `django-guardian`_ settings (see its doc for more details) :

::

    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend', # this is default
        'guardian.backends.ObjectPermissionBackend',
    )

    ANONYMOUS_USER_ID = None

And add the `djangocodemirror`_ required settings : ::

    DJANGOCODEMIRROR_USER_SETTINGS_COOKIE_NAME = "djangocodemirror_user_settings"
    CODEMIRROR_SETTINGS = {
        'sveetchies-documents-edit-page': {
            'mode': 'rst',
            'csrf': 'CSRFpass',
            'preview_url': ('sveedocuments:preview',),
            'quicksave_url': ('sveedocuments:page-quicksave',),
            'quicksave_datas': 'DJANGOCODEMIRROR_OBJECT',
            'lineWrapping': True,
            'lineNumbers': True,
            'search_enabled': True,
            'settings_cookie': DJANGOCODEMIRROR_USER_SETTINGS_COOKIE_NAME,
            'help_link': ('sveedocuments:help',),
            'settings_url': ('sveedocuments:editor-settings', [], {}),
        },
        'sveetchies-documents-edit-insert': {
            'mode': 'rst',
            'csrf': 'CSRFpass',
            'preview_url': ('sveedocuments:preview',),
            'quicksave_url': ('sveedocuments:insert-quicksave',),
            'quicksave_datas': 'DJANGOCODEMIRROR_OBJECT',
            'lineWrapping': True,
            'lineNumbers': True,
            'search_enabled': True,
            'settings_cookie': DJANGOCODEMIRROR_USER_SETTINGS_COOKIE_NAME,
            'help_link': ('sveedocuments:help',),
            'settings_url': ('sveedocuments:editor-settings', [], {}),
        },
    }
    CODEMIRROR_SETTINGS['sveetchies-documents-add-page'] = CODEMIRROR_SETTINGS['sveetchies-documents-edit-page'].copy()
    CODEMIRROR_SETTINGS['sveetchies-documents-add-page']['quicksave_url'] = None
    CODEMIRROR_SETTINGS['sveetchies-documents-add-insert'] = CODEMIRROR_SETTINGS['sveetchies-documents-edit-insert'].copy()
    CODEMIRROR_SETTINGS['sveetchies-documents-add-insert']['quicksave_url'] = None

Also you can overrides app settings to change some behaviors, see ``sveedocuments.local_settings`` to see what you can override in your project settings like ``DOCUMENTS_PAGE_TEMPLATES`` to add new templates to use to build your pages.

Optionnally if you plan to use `autobreadcrumbs`_,  register its *context processor* in settings :

::

    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        'autobreadcrumbs.context_processors.AutoBreadcrumbsContext',
        ...
    )


Finally mount its urls into your main ``urls.py`` : ::

    import autobreadcrumbs
    autobreadcrumbs.autodiscover()
    
    urlpatterns = patterns('',
        ...
        (r'^documents/', include('sveedocuments.urls', namespace='sveedocuments')),
        ...
    )

The first two lines are for the `autobreadcrumbs`_ *autodiscover* remove them if you don't plan to use it.

Usage
=====

Permissions
-----------

sveedocuments make usage of `django-guardian`_ to manage 'per object permissions' or 'global permissions'.

Actually you need to use the Django admin and be a staff user with the right permissions for managing Page or Insert objects to add these permissions for your users.

And so, you can add the needed permissions globally to the all documents within each user accounts. Or you can add a permission for a specific object in its edit page (in Django admin) using the link named *Object permissions*.

* All users can see the sitemap and visible pages;
* Users with ``sveedocuments.add_page`` permission can create new pages;
* Users with ``sveedocuments.change_page`` permission can edit pages, add them new attachment item or delete them;
* Users with ``sveedocuments.delete_page`` permission can create delete pages;

Others Page's and Insert's model permissions have no roles on frontend.

Permission error response
.........................

Permission error is rendered though a ``403.html`` template that is allready embedded within this app, you can override it in your project with adding your custom ``403.html`` template in your project templates directory.

Also you can use another template name, you will have to define its name in ``settings.GUARDIAN_TEMPLATE_403`` (yes, this is a setting from `django-guardian`_, see its doc for more details).

Signals
-------

sveedocuments use Django signals to send signals when a ``Page`` object or an ``Insert`` object is updated (when created or edited), you can listen to them to perform some tasks. These signals are :

* ``sveedocuments.models.documents_page_update_signal`` for ``Page`` updates;
* ``sveedocuments.models.documents_insert_update_signal`` for ``Insert`` updates;

