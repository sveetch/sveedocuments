# -*- coding: utf-8 -*-
"""
Model admin
"""
from django.contrib import admin
from models import *

class InsertAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title', 'modified', 'author', 'visible' )
    list_filter = ('created', 'modified', 'visible')
    ordering = ('slug',)
    search_fields = ('title','content',)
    readonly_fields = ('author',)
    list_display_links = ('title',)
    prepopulated_fields = {"slug": ("title",)}
    
    def save_model(self, request, obj, form, change):
        """
        Automatically add/update the author field with the ``request.user``
        """
        instance = form.save(commit=False)
        instance.author = request.user
        instance.save()
        form.save_m2m()

        return instance

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'modified', 'published', 'author', 'visible' )
    list_filter = ('created', 'modified', 'published', 'visible')
    ordering = ('order',)
    search_fields = ('title','content',)
    readonly_fields = ('author',)
    list_display_links = ('title',)
    prepopulated_fields = {"slug": ("title",)}
    
    def save_model(self, request, obj, form, change):
        """
        Automatically add/update the author field with the ``request.user``
        """
        instance = form.save(commit=False)
        instance.author = request.user
        instance.save()
        form.save_m2m()

        return instance

class PageRevisionAdmin(admin.ModelAdmin):
    list_display = ('title', 'revision', 'author', 'visible' )
    list_filter = ('created', 'published', 'visible')
    ordering = ('order', 'revision')
    search_fields = ('title','content',)
    readonly_fields = ('author', 'revision')
    list_display_links = ('title',)
    
    def save_model(self, request, obj, form, change):
        """
        Automatically add/update the author field with the ``request.user``
        """
        instance = form.save(commit=False)
        instance.author = request.user
        instance.save()
        form.save_m2m()

        return instance

admin.site.register(Insert, InsertAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(PageRevision, PageRevisionAdmin)
admin.site.register(Attachment)
