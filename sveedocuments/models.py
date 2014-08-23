# -*- coding: utf-8 -*-
"""
Data models
"""
from datetime import datetime

import django.dispatch
from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache
from django.utils.translation import ugettext_lazy as _

import mptt
from mptt.models import TreeForeignKey

from rstview.local_settings import RSTVIEW_PARSER_FILTER_SETTINGS

from sveedocuments.local_settings import (DOCUMENTS_PAGE_TEMPLATES, PAGE_SLUGS_CACHE_KEY_NAME, 
                                        PAGE_RENDER_CACHE_KEY_NAME, INSERT_RENDER_CACHE_KEY_NAME,
                                        PAGE_TOC_CACHE_KEY_NAME, INSERT_TOC_CACHE_KEY_NAME,
                                        DOCUMENTS_PAGE_ARCHIVED, DOCUMENTS_PAGE_TEMPLATE_DEFAULT)
from sveedocuments.utils import _get_cache_keyset
from sveedocuments.utils.filefield import content_file_name

DOCUMENTS_PAGE_TEMPLATES_CHOICES = [(k,v[1]) for k,v in DOCUMENTS_PAGE_TEMPLATES.items()]

DOCUMENTS_VISIBILTY_CHOICES = (
    (True, _('Visible')),
    (False, _('Hidden')),
)

IMAGE_MIMETYPES = (
    'image/gif',
    'image/jpeg',
    'image/png',
    #'image/tiff',
    'image/svg+xml',
)

ATTACH_FILE_UPLOADTO = lambda x,y: content_file_name('pages/attachments/%Y/%m/%d', x, y)

class Insert(models.Model):
    """
    Document to insert
    """
    created = models.DateTimeField(_('created'), blank=True, auto_now_add=True)
    modified = models.DateTimeField(_('last edit'), auto_now=True)
    author = models.ForeignKey(User, verbose_name=_('author'))
    title = models.CharField(_('title'), blank=True, null=True, max_length=255)
    slug = models.SlugField(_('slug'), unique=True, max_length=75)
    visible = models.BooleanField(_('visibility'), choices=DOCUMENTS_VISIBILTY_CHOICES, default=True)
    content = models.TextField(_('content'), blank=False)

    def __unicode__(self):
        return self.slug
    
    def get_render_cache_key(self, **kwargs):
        """
        Get the cache key for the content render according to the given settings
        """
        return INSERT_RENDER_CACHE_KEY_NAME.format(id=self.id, **kwargs)
    
    def get_toc_cache_key(self, **kwargs):
        """
        Get the cache key for the content TOC according to the given settings
        """
        return INSERT_TOC_CACHE_KEY_NAME.format(id=self.id, **kwargs)
    
    def save(self, *args, **kwargs):
        # Invalidate all caches at edit
        if self.modified:
            self.clear_cache()
        
        super(Insert, self).save(*args, **kwargs)
    
    def delete(self, using=None):
        self.clear_cache()
        super(Insert, self).delete(using=using)
    
    def clear_cache(self):
        """
        Invalidate all possible cache keys
        """
        keys = _get_cache_keyset(INSERT_RENDER_CACHE_KEY_NAME, **{
            'id': self.id,
            'setting': RSTVIEW_PARSER_FILTER_SETTINGS.keys(),
            'header_level': ['None']+range(1, 7),
        })
        keys += _get_cache_keyset(INSERT_TOC_CACHE_KEY_NAME, **{
            'id': self.id,
            'setting': RSTVIEW_PARSER_FILTER_SETTINGS.keys(),
            'header_level': ['None']+range(1, 7),
        })
        cache.delete_many(keys)
        return keys
    
    class Meta:
        verbose_name = _("insert document")
        verbose_name_plural = _("insert document")

        
        
class PageModelBase(models.Model):
    """
    Model base for Pages
    """
    created = models.DateTimeField(_('created'), blank=True, editable=False)
    author = models.ForeignKey(User, verbose_name=_('author'))
    title = models.CharField(_('title'), blank=False, max_length=255)
    published = models.DateTimeField(_('publish date'), blank=True, help_text=_("Define when the document will be displayed on the site. Empty value mean an instant publish, use a coming date to program a futur publish."))
    template = models.CharField(_('template'), max_length=50, choices=DOCUMENTS_PAGE_TEMPLATES_CHOICES, default=DOCUMENTS_PAGE_TEMPLATE_DEFAULT, help_text=_("This template will be used to render the page."))
    order = models.SmallIntegerField(_('order'), default=1, help_text=_("Display order in lists and trees."))
    visible = models.BooleanField(_('visibility'), choices=DOCUMENTS_VISIBILTY_CHOICES, default=True)
    content = models.TextField(_('content'), blank=False)
    comment = models.CharField(_('comment'), blank=True, null=True, max_length=255)

    def __unicode__(self):
        return self.title

    def get_template(self):
        return DOCUMENTS_PAGE_TEMPLATES[self.template][0]
    
    class Meta:
        abstract = True    



class Page(PageModelBase):
    """
    Full page document
    """
    modified = models.DateTimeField(_('last edit'), auto_now=True)
    slug = models.SlugField(_('slug'), unique=True, max_length=75, help_text=_("Unique slug used in URL, should be automatically filled with sluggified title."))
    
    @models.permalink
    def get_absolute_url(self):
        return ('documents-page-details', [self.slug])
    
    def get_render_cache_key(self, **kwargs):
        """
        Get the cache key for the content render with according to the given settings
        """
        return PAGE_RENDER_CACHE_KEY_NAME.format(id=self.id, **kwargs)
    
    def get_toc_cache_key(self, **kwargs):
        """
        Get the cache key for the content TOC with according to the given settings
        """
        return PAGE_TOC_CACHE_KEY_NAME.format(id=self.id, **kwargs)
    
    def clear_cache(self):
        """
        Invalidate all possible cache keys
        """
        keys = _get_cache_keyset(PAGE_RENDER_CACHE_KEY_NAME, **{
            'id': self.id,
            'setting': RSTVIEW_PARSER_FILTER_SETTINGS.keys(),
        })
        keys += _get_cache_keyset(PAGE_TOC_CACHE_KEY_NAME, **{
            'id': self.id,
            'setting': RSTVIEW_PARSER_FILTER_SETTINGS.keys(),
        })
        # Drop cache for knowed pages slugs used in the ``page`` rest role
        cache.delete_many([PAGE_SLUGS_CACHE_KEY_NAME]+keys)
        return keys
    
    def _get_current_revision(self):
        return (self.revision.all().aggregate(models.Max('revision')).get('revision__max') or 0)+1
    current_revision = property(_get_current_revision)
    
    def save(self, *args, **kwargs):
        # First create
        if not self.created:
            self.created = datetime.now()
        # Creating a new revision archive
        elif DOCUMENTS_PAGE_ARCHIVED:
            old = Page.objects.get(pk=self.id)
            PageRevision(
                page=self,
                created=self.modified,
                parent=old.parent,
                author=old.author,
                title=old.title,
                published=old.published,
                slug=old.slug,
                template=old.template,
                order=old.order,
                visible=old.visible,
                content=old.content,
                revision=self.current_revision,
                comment=old.comment,
            ).save()
        
        # Fill in the published date with the created date if empty
        if not self.published:
            self.published = self.created
        # Invalidate all caches on edit
        if self.modified:
            self.clear_cache()
        
        super(Page, self).save(*args, **kwargs)
    
    def delete(self, using=None):
        self.clear_cache()
        super(Page, self).delete(using=using)
    
    class Meta:
        verbose_name = _("page")
        verbose_name_plural = _("pages")

# Add a parent foreign key to the model without sublassing MPTTModel
TreeForeignKey(Page, blank=True, null=True, related_name="%(app_label)s_%(class)s_children").contribute_to_class(Page, 'parent')
mptt.register(Page, order_insertion_by=['order', 'title'])



class PageRevision(PageModelBase):
    """
    History revision for a Page document
    """
    slug = models.SlugField(_('slug'), max_length=75)
    page = models.ForeignKey(Page, verbose_name=_('page'), related_name='revision')
    parent = models.ForeignKey(Page, null=True, blank=True, related_name="revision_parent")
    revision = models.IntegerField(_('revision number'), blank=False, default=0, editable=False)
    
    class Meta:
        verbose_name = _("page revision")
        verbose_name_plural = _("pages revisions")



class Attachment(models.Model):
    """
    Attachment file for a Page document
    
    TODO: Remove attachment map cache on update/delete and also when Page is removed, and updated ?
    """
    page = models.ForeignKey(Page, verbose_name=_('page'), related_name='attachment')
    author = models.ForeignKey(User, verbose_name=_('author'))
    title = models.CharField(_('title'), max_length=75, blank=True)
    slug = models.CharField(_('slug'), max_length=75, blank=True, help_text=_("Used as the key to put the attachment in your documents. This does not really use the slug syntax, you can use more special characters. If empty, will be filled with the original file name."))
    created = models.DateTimeField(_('created'), auto_now_add=True)
    file = models.FileField(_('file'), upload_to=ATTACH_FILE_UPLOADTO, max_length=255, blank=False)
    size = models.IntegerField(_('size'), blank=False, default=0, editable=False)
    content_type = models.CharField(_('content_type'), max_length=120, blank=False, null=True, editable=False)
    
    def __unicode__(self):
        return self.slug
    
    def is_image(self):
        return (self.content_type and self.content_type in IMAGE_MIMETYPES)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # TODO: slugify
            self.slug = self.file.name.strip()
        if not self.title:
            self.title = self.slug
        super(Attachment, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("attachment file")
        verbose_name_plural = _("attachment files")


# Declaring signals
documents_page_update_signal = django.dispatch.Signal(providing_args=["page_instance","edited"])
documents_insert_update_signal = django.dispatch.Signal(providing_args=["insert_instance","edited"])

## Signal receiver demo
#def documents_page_update_receiver(sender, **kwargs):
    #page_instance = kwargs['page_instance']
    #edited = kwargs['edited']
    
    #if edited:
        #print u"* {0} has been edited !".format(page_instance.title)
    #else:
        #print u"* {0} has been created !".format(page_instance.title)

## Connecting signal to the receiver
#documents_page_update_signal.connect(documents_page_update_receiver)
