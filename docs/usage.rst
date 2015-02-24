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

=====
Usage
=====

Permissions
***********

sveedocuments make usage of Django permissions and groups.

You need to use the Django admin and be a staff user with the right permissions for managing permissions and groups for your users.

And so, you can add the needed permissions globally to all documents within each user accounts.

* All users can see the sitemap and visible pages (except if restricted mode is enabled);
* Users with ``sveedocuments.add_page`` permission can create new pages;
* Users with ``sveedocuments.change_page`` permission can edit pages, add them new attachment item or delete them;
* Users with ``sveedocuments.delete_page`` permission can create delete pages;

Others Page's and Insert's model permissions have no roles on frontend.

Signals
*******

sveedocuments use Django signals to send signals when a ``Page`` object or an ``Insert`` object is updated (created or edited), you can listen to them to perform some tasks.

These signals are :

* ``sveedocuments.models.documents_page_update_signal`` for ``Page`` updates;
* ``sveedocuments.models.documents_insert_update_signal`` for ``Insert`` updates;

Each of them send the page or insert intance and a boolean about update kind (edited if ``True``, created if ``False``) as method kwargs.

Templates
*********

You can add many additional templates and each page can use its own template.

To define new templates just add them to your settings:

.. sourcecode:: python

    DOCUMENTS_PAGE_TEMPLATES = {
        'default': ('sveedocuments/page_details/page_default.html', gettext('Default template with document content only')),
        'custom_sample': ('sveedocuments/page_details/mytemplate.html', gettext('Custom template sample')),
    }

Obviously, if you remove template that was allready used in your pages, there will be an error, you should modify them before removing their template.
