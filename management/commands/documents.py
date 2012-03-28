# -*- coding: utf-8 -*-
"""
Command line tool
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
        make_option("--get_pages", dest="get_pages", default=None, help="Get pages from given slug. Each slug separated by comma, order does matter. Special slug 'ALL' means all pages.", metavar="SLUG"),
        make_option("--follows", dest="followed_pages", default=None, help="Specify each page slug to recursively follow for their children. Each slug separated by comma. Special slug 'ALL' means all pages.", metavar="SLUGS"),
        make_option("--excludes", dest="excluded_pages", default=None, help="Specify each page slug to excludes (but not their children). Each slug separated by comma.", metavar="SLUGS"),
        make_option("--print", dest="print_docs", action="store_true", default=False, help="Print selected documents."),
        make_option("--resume", dest="resume_docs", action="store_true", default=False, help="Resume (by titles) selected documents."),
        make_option("--export_file", dest="export_file", default=None, help="Export selected documents to file.", metavar="FILEPATH"),
    )
    help = "Command for Sveetchies-documents"

    def handle(self, *args, **options):
        if len(args) != 0:
            raise CommandError("Command doesn't accept any arguments")
        
        self.clearcache = options.get('clearcache')
        self.export_file = options.get('export_file')
        self.print_docs = options.get('print_docs')
        self.resume_docs = options.get('resume_docs')
        self.get_pages = options.get('get_pages')
        self.followed_pages = options.get('followed_pages')
        self.excluded_pages = options.get('excluded_pages')
        self.verbosity = int(options.get('verbosity'))
        
        if self.clearcache:
            self.do_clearcache()
        
        if self.print_docs or self.resume_docs:
            output = StringIO.StringIO()
            self.output_documents(output, resumed=self.resume_docs)
            print output.getvalue()
            output.close()
        
        if self.export_file:
            output = open(self.export_file, "w")
            self.output_documents(output)
            output.close()

    def get_documents(self):
        """
        Get all documents matched by given options
        """
        instances = []
        
        if self.get_pages:
            followed = [v for v in (self.followed_pages or '').split(',') if v]
            excluded = [v for v in (self.excluded_pages or '').split(',') if v]
            if self.verbosity:
                print "Followed slugs:", followed
                print "Excluded slugs:", excluded
            
            # Recherche des enfants des pages à exclure
            if excluded:
                tmp = []
                for item in excluded:
                    try:
                        p = Page.objects.get(slug=item).get_descendants(include_self=True).values_list('slug', flat=True)
                    except Page.DoesNotExist:
                        raise CommandError("Excludes: slug '{0}' does not exist".format(item))
                    else:
                        tmp.extend(p)
                    
                excluded = tmp
                if self.verbosity:
                    print "Excluded pages:", excluded
                
            # Slugs des pages à extraire
            if self.get_pages == 'ALL':
                page_slugs = Page.objects.root_nodes().exclude(slug__in=excluded).values_list('slug', flat=True)
            else:
                page_slugs = [s for s in self.get_pages.split(',') if s not in excluded]
            
            # Récupère chaque page
            for slug in page_slugs:
                # Si mode suivi intégrale des enfants, ou que le slug de la page est explicitement spécifié à suivre
                if followed and ('ALL' in followed or slug in followed):
                    try:
                        queryset = Page.objects.get(slug=slug).get_descendants(include_self=True).exclude(id__in=[i.id for i in instances]).exclude(slug__in=excluded)
                    except Page.DoesNotExist:
                        raise CommandError("Get many: slug '{0}' does not exist".format(slug))
                    else:
                        instances.extend(queryset)
                # Pas de suivi on récupère que la page
                else:
                    try:
                        page = Page.objects.get(slug=slug)
                    except Page.DoesNotExist:
                        raise CommandError("Get single: slug '{0}' does not exist".format(slug))
                    else:
                        instances.append(page)
        
        if self.verbosity:
            print "Pages instances:", instances
        if not instances:
            raise CommandError("No document finded")
        return instances

    def output_documents(self, output, resumed=False):
        """
        Export all matched documents in a file
        
        Documents are ordered and their titles are added at top of each them as the 
        highest title
        """
        for document in self.get_documents():
            if not resumed:
                output.write( "\n" )
                output.write( self._to_rest_title(document.title.encode('UTF8').strip(), character="=")+"\n\n" )
                output.write( document.content.encode('UTF8')+"\n" )
            else:
                output.write( "*"+document.title.encode('UTF8')+"\n" )
        
        return output

    def _to_rest_title(self, title, character="="):
        width = max([len(line) for line in title.splitlines()])
        ascii_line = character*width
        return ascii_line+"\n"+title+"\n"+ascii_line
    
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
