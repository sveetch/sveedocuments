# -*- coding: utf-8 -*-
"""
General Command line tool
"""
import StringIO

from optparse import OptionValueError, make_option

from django.conf import settings
from django.core.cache import cache
from django.core.management.base import CommandError, BaseCommand

from sveedocuments.models import Page, Insert

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option("--clearcache", dest="clearcache", action="store_true", default=False, help="Clear all documents (Page and Insert) cache."),
    )
    help = "General command for Sveetchies-documents"

    def handle(self, *args, **options):
        if len(args) != 0:
            raise CommandError("Command doesn't accept any arguments")
        
        self.clearcache = options.get('clearcache')
        self.verbosity = int(options.get('verbosity'))
        
        if self.clearcache:
            self.do_clearcache()

    def do_clearcache(self):
        """
        Clear all possible caches from the parser for documents
        """
        inserts = Insert.objects.all().order_by('id')
        for instance_item in inserts:
            keys = instance_item.clear_cache()
            
        pages = Page.objects.all().order_by('id')
        for page_item in pages:
            keys = page_item.clear_cache()
            
        if self.verbosity:
            print "* All documents cache cleared"
