# -*- coding: utf-8 -*-
"""
Data models
"""
from datetime import datetime

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
                                        DOCUMENTS_PAGE_ARCHIVED)
from sveedocuments.utils import _get_cache_keyset

DOCUMENTS_PAGE_TEMPLATES_CHOICES = [(k,v[1]) for k,v in DOCUMENTS_PAGE_TEMPLATES.items()]

DOCUMENTS_VISIBILTY_CHOICES = (
    (True, _('Visible')),
    (False, _('Hidden')),
)

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
    Full page document
    """
    created = models.DateTimeField(_('created'), blank=True)
    author = models.ForeignKey(User, verbose_name=_('author'))
    title = models.CharField(_('title'), blank=False, max_length=255)
    published = models.DateTimeField(_('publish date'), blank=True, help_text=_("Define when the document will be displayed on the site. Empty value mean an instant publish, use a coming date to program a futur publish."))
    template = models.CharField(_('template'), max_length=50, choices=DOCUMENTS_PAGE_TEMPLATES_CHOICES, default='default', help_text=_("This template will be used to render the page."))
    order = models.SmallIntegerField(_('order'), default=1, help_text=_("Display order in lists and trees."))
    visible = models.BooleanField(_('visibility'), choices=DOCUMENTS_VISIBILTY_CHOICES, default=True)
    content = models.TextField(_('content'), blank=False)

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
    
    def save(self, *args, **kwargs):
        # First create
        if not self.created:
            self.created = datetime.now()
        # Creating a new revision archive
        elif DOCUMENTS_PAGE_ARCHIVED:
            old = Page.objects.get(pk=self.id)
            rev_no = self.revision.all().aggregate(models.Max('revision')).get('revision__max') or 0
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
                revision=rev_no+1,
            ).save()
        
        # Fill in the published date with the created date if empty
        if not self.published:
            self.published = self.created
        # Invalidate all caches at edit
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
    page = models.ForeignKey(Page, verbose_name=_('page source'), related_name='revision')
    parent = models.ForeignKey(Page, null=True, blank=True, related_name="revision_parent")
    revision = models.IntegerField(_('revision number'), blank=False, default=0, editable=False)
    
    class Meta:
        verbose_name = _("page revision")
        verbose_name_plural = _("pages revisions")
