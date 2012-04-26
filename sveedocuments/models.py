# -*- coding: utf-8 -*-
"""
Data models
"""
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache
from django.utils.translation import ugettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager

from sveedocuments.settings_local import (DOCUMENTS_PARSER_FILTER_SETTINGS, 
                                        DOCUMENTS_PAGE_TEMPLATES, PAGE_SLUGS_CACHE_KEY_NAME, 
                                        PAGE_RENDER_CACHE_KEY_NAME, INSERT_RENDER_CACHE_KEY_NAME,
                                        PAGE_TOC_CACHE_KEY_NAME, INSERT_TOC_CACHE_KEY_NAME)
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
    visible = models.BooleanField(_('visibility'), default=True)
    content = models.TextField(_('content'), blank=False)

    def __unicode__(self):
        return self.slug
    
    def get_render_cache_key(self, **kwargs):
        """
        Get the cache key for the content render with according to the given settings
        """
        return INSERT_RENDER_CACHE_KEY_NAME.format(id=self.id, **kwargs)
    
    def get_toc_cache_key(self, **kwargs):
        """
        Get the cache key for the content TOC with according to the given settings
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
            'setting': DOCUMENTS_PARSER_FILTER_SETTINGS.keys(),
            'header_level': ['None']+range(1, 7),
        })
        keys += _get_cache_keyset(INSERT_TOC_CACHE_KEY_NAME, **{
            'id': self.id,
            'setting': DOCUMENTS_PARSER_FILTER_SETTINGS.keys(),
            'header_level': ['None']+range(1, 7),
        })
        cache.delete_many(keys)
        return keys
    
    class Meta:
        verbose_name = _("insert document")
        verbose_name_plural = _("insert document")

class Page(MPTTModel):
    """
    Full page document
    """
    created = models.DateTimeField(_('created'), blank=True)
    modified = models.DateTimeField(_('last edit'), auto_now=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    author = models.ForeignKey(User, verbose_name=_('author'))
    title = models.CharField(_('title'), blank=False, max_length=255)
    published = models.DateTimeField(_('publish date'), blank=True, help_text=_("Define when the document will be displayed on the site. Empty value mean an instant publish, use a coming date to program a futur publish."))
    slug = models.SlugField(_('slug'), unique=True, max_length=75, help_text=_("Unique slug used in URL, should be automatically filled with sluggified title."))
    template = models.CharField(_('template'), max_length=50, choices=DOCUMENTS_PAGE_TEMPLATES_CHOICES, default='default', help_text=_("This template will be used to render the page."))
    order = models.SmallIntegerField(_('order'), default=1, help_text=_("Display order in lists and trees."))
    visible = models.BooleanField(_('visibility'), choices=DOCUMENTS_VISIBILTY_CHOICES, default=True)
    content = models.TextField(_('content'), blank=False)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('documents-page-details', [self.slug])
    
    def get_template(self):
        return DOCUMENTS_PAGE_TEMPLATES[self.template][0]
    
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
    
    def save(self, *args, **kwargs):
        # TODO: update all children to reflect visibility
        # Fill in the published date with the create date if empty
        self.created = datetime.now()
        if not self.published:
            self.published = self.created
        # Invalidate all caches at edit
        if self.modified:
            self.clear_cache()
        
        super(Page, self).save(*args, **kwargs)
    
    def delete(self, using=None):
        self.clear_cache()
        super(Page, self).delete(using=using)
    
    def clear_cache(self):
        """
        Invalidate all possible cache keys
        """
        keys = _get_cache_keyset(PAGE_RENDER_CACHE_KEY_NAME, **{
            'id': self.id,
            'setting': DOCUMENTS_PARSER_FILTER_SETTINGS.keys(),
        })
        keys += _get_cache_keyset(PAGE_TOC_CACHE_KEY_NAME, **{
            'id': self.id,
            'setting': DOCUMENTS_PARSER_FILTER_SETTINGS.keys(),
        })
        cache.delete_many([PAGE_SLUGS_CACHE_KEY_NAME]+keys)
        return keys
    
    class Meta:
        verbose_name = _("page")
        verbose_name_plural = _("pages")
    
    class MPTTMeta:
        order_insertion_by = ['order', 'title']
