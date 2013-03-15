# -*- coding: utf-8 -*-
"""
General Command line tool
"""
import StringIO

from optparse import OptionValueError, make_option

from django.conf import settings
from django.core.cache import cache
from django.core.management.base import CommandError, BaseCommand

from sveedocuments.local_settings import DOCUMENTS_CACHE_KEYS_TO_CLEAN
from sveedocuments.models import Page, Insert

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option("--clearcache", dest="clearcache", action="store_true", default=False, help="Clear all documents (Page and Insert) cache."),
        make_option("--treefix", dest="treefix", action="store_true", default=False, help="Rebuild the Pages tree. This is currently used to fix a bug when deleting some item. This should be a temporary trick that will be deleted when a correct fix will be finded."),
    )
    help = "General command for Sveetchies-documents"

    def handle(self, *args, **options):
        if len(args) != 0:
            raise CommandError("Command doesn't accept any arguments")
        
        self.clearcache = options.get('clearcache')
        self.treefix = options.get('treefix')
        self.verbosity = int(options.get('verbosity'))
        
        if self.clearcache:
            self.do_clearcache()
        
        if self.treefix:
            self.do_treefix()

    def do_treefix(self):
        """
        Rebuild Pages tree info
        """
        Page.tree.rebuild()

    def do_clearcache(self):
        """
        Clear all possible caches from documents
        """
        inserts = Insert.objects.all().order_by('id')
        for instance_item in inserts:
            keys = instance_item.clear_cache()
            
        pages = Page.objects.all().order_by('id')
        for page_item in pages:
            keys = page_item.clear_cache()
        
        if DOCUMENTS_CACHE_KEYS_TO_CLEAN:
            cache.delete_many(DOCUMENTS_CACHE_KEYS_TO_CLEAN)
            
        if self.verbosity:
            print "* All documents cache cleared"
