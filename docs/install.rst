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

=======
Install
=======


Requires
********

* Django >= 1.5;
* `docutils`_ >= 0.7;
* `rstview`_ >= 0.2;
* `autobreadcrumbs`_ >= 1.0;
* `djangocodemirror`_ >= 0.9.4;
* `django-mptt`_ >= 0.5.2;
* `crispy-forms-foundation`_ >= 0.3.4;
* `django-braces`_ >= 1.3.0;

Optionnally
-----------

* `django-assets`_ to use Assets bundles instead of plain assets, you will have to load these bundles instead of raw asset files, perform this with overriding ``sveedocuments/assets_css.html`` and ``sveedocuments/assets_js.html`` in your project templates directory.
* `South`_ to perform database migrations for next releases;
* `django-sendfile`_ to protect download for page's attachments;


Procedure
*********

Install it from PyPi: ::

    pip install sveedocuments

You will need to set a setting about the absolute directory path of your project:

.. sourcecode:: python
    
    import os
    PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
    
Register required apps in your project settings file:

.. sourcecode:: python

    INSTALLED_APPS = (
        ...
        'autobreadcrumbs',
        'crispy_forms',
        'crispy_forms_foundation', 
        'djangocodemirror',
        'rstview',
        'mptt',
        'sveedocuments',
        ...
    )

Import its default settings (still in your project settings file):

.. sourcecode:: python

    from sveedocuments.settings import *

(Also you can override some default values, see ``sveedocuments/settings.py`` file for more details about available settings).

Then you need to register some settings for `djangocodemirror`_, this does not reside in the default settings to avoid to break other apps that could define another codemirror settings. So just copy the code below in your project settings file or merge it with you existing config if any:

.. sourcecode:: python

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

Then for `autobreadcrumbs`_, register its *context processor* in settings:

.. sourcecode:: python

    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        'autobreadcrumbs.context_processors.AutoBreadcrumbsContext',
        ...
    )


Finally mount its urls into your main ``urls.py``:

.. sourcecode:: python

    import autobreadcrumbs
    autobreadcrumbs.autodiscover()
    
    urlpatterns = patterns('',
        ...
        (r'^documents/', include('sveedocuments.urls', namespace='sveedocuments')),
        ...
    )

Options
*******

Page archiving
--------------

Default behavior is to create an archive of previous version when saving any changes on a page.

Sometime you don't want to archive page changes, for this define the following setting:

.. sourcecode:: python

    DOCUMENTS_PAGE_ARCHIVED = False

Restricted mode
---------------

When enabled, this mode restrict page views to authenticated users only. This is enabled for all pages without exception, and will apply also on sitemap and page's attachment downloads.

To enable this mode, just define the setting below:

.. sourcecode:: python

    DOCUMENTS_PAGE_RESTRICTED = True

When enabled, default behavior for page's attachment is to use `django-sendfile`_ to protect them to public download. If you don't want to use it, set the following setting:

.. sourcecode:: python

    DOCUMENTS_ATTACHMENT_USE_SENDFILE = False

If you plan to use `django-sendfile`_, you will register it in your project settings file:

.. sourcecode:: python

    INSTALLED_APPS = (
        ...
        'sendfile',
        ...
    )

And finally add its settings:

.. sourcecode:: python

    # Backend type: do not define any other backend that the development one, for 
    # other environnement define backend in their own setting file
    SENDFILE_BACKEND = 'sendfile.backends.development' # Dummy backend for django's wsgi 'runserver'
    #SENDFILE_BACKEND = 'sendfile.backends.nginx' # For Nginx
    #SENDFILE_BACKEND = 'sendfile.backends.xsendfile' # For Apache or Lighttpd

    # Protected files directory name, this dir have to exists in your project, but don't put 
    # it under media or static dir as it will be served unprotected
    PROTECTED_MEDIAS_DIRNAME = 'protected_medias'

    # Send File paths and url
    SENDFILE_ROOT = join(PROJECT_PATH, PROTECTED_MEDIAS_DIRNAME)
    SENDFILE_URL = '/%s' % PROTECTED_MEDIAS_DIRNAME

See `django-sendfile`_ documentation for more details.
