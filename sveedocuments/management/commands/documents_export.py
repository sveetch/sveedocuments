# -*- coding: utf-8 -*-
"""
Command line tool to export

DEPRECATED
"""
import re, StringIO

from optparse import OptionValueError, make_option

from django.conf import settings
from django.core.cache import cache
from django.core.management.base import CommandError, BaseCommand

from sveedocuments.models import Page, Insert

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option("--get_pages", dest="get_pages", default=None, help="Get pages from given slug. Each slug separated by comma, order does matter. Special slug 'ALL' means all pages in their sitemap order.", metavar="SLUGS"),
        make_option("--follows", dest="followed_pages", default=None, help="Specify each page slug to recursively follow for their children in select. Each slug separated by comma. Special slug 'ALL' means all pages.", metavar="SLUGS"),
        make_option("--excludes", dest="excluded_pages", default=None, help="Specify each page slug to excludes (but not their children) in select. Each slug separated by comma.", metavar="SLUGS"),
        make_option("--print", dest="print_docs", action="store_true", default=False, help="Print out the selected documents."),
        make_option("--resume", dest="resume_docs", action="store_true", default=False, help="Print a title list of selected documents."),
        make_option("--to_file", dest="export_to_file", default=None, help="Export selected documents in a file.", metavar="FILEPATH"),
        make_option("--to_github", dest="export_to_github", default=None, help="Export selected documents in a file but with some changes to be suitable with the Github ReSructuredText parser.", metavar="FILEPATH"),
    )
    help = "[DEPRECATED] Command to export documents from Sveetchies-documents"

    def handle(self, *args, **options):
        if len(args) != 0:
            raise CommandError("Command doesn't accept any arguments")
        
        self.export_to_file = options.get('export_to_file')
        self.export_to_github = options.get('export_to_github')
        self.print_docs = options.get('print_docs')
        self.resume_docs = options.get('resume_docs')
        self.get_pages = options.get('get_pages')
        self.followed_pages = options.get('followed_pages')
        self.excluded_pages = options.get('excluded_pages')
        self.verbosity = int(options.get('verbosity'))
        
        self.compile_hack_regex()
        
        if self.print_docs or self.resume_docs:
            output = StringIO.StringIO()
            self.output_documents(output, resumed=self.resume_docs)
            print output.getvalue()
            output.close()
        
        if self.export_to_file or self.export_to_github:
            output = open(self.export_to_file or self.export_to_github, "w")
            self.output_documents(output)
            output.close()

    def compile_hack_regex(self):
        """
        Compile all regex used for syntax hacks
        
        ``_page_role_regex`` to match : ::
        
            :page:`VALUE`
            
        ``_sourcecode_directive_regex`` to match : ::
        
            ..  sourcecode:: python
                :linenos:
                :hl_lines: 1,2,3
        """
        self._page_role_regex = re.compile(r"(?:\:page\:`)(?P<name>.*?)(?:`)")
        
        simple = r"(?:\s)"
        with_linenos = r"(?:\s[\ ]+\:linenos\:)"
        with_hl_lines = r"(?:\s[\ ]+\:linenos\:\s[\ ]+\:hl_lines\:[\ ][1-9,]+)"
        self._sourcecode_directive_regex = re.compile(r"(?:..[\ ]+sourcecode\:\:[\ ]+)(?P<language>.*?)(?:" + with_hl_lines + r"|" + with_linenos + r"|" + simple + r")")

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
                page_slugs = Page.objects.root_nodes().exclude(visible=False, slug__in=excluded).values_list('slug', flat=True)
            else:
                page_slugs = [s for s in self.get_pages.split(',') if s not in excluded]
            
            # Récupère chaque page
            for slug in page_slugs:
                # Si mode suivi intégrale des enfants, ou que le slug de la page est explicitement spécifié à suivre
                if followed and ('ALL' in followed or slug in followed):
                    try:
                        queryset = Page.objects.get(slug=slug).get_descendants(include_self=True).exclude(id__in=[i.id for i in instances]).exclude(visible=False, slug__in=excluded)
                    except Page.DoesNotExist:
                        raise CommandError("Get many: slug '{0}' does not exist".format(slug))
                    else:
                        instances.extend(queryset)
                # Pas de suivi on récupère que la page
                else:
                    try:
                        page = Page.objects.get(slug=slug, visible=True)
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
        loaded_docs = self.get_documents()
        from_multiple_docs = len(loaded_docs)>1
        
        for document in loaded_docs:
            content = document.content
            
            if not resumed:
                # Apply hacks on content if needeed
                if self.export_to_github:
                    content = self._page_role_regex.sub(self._page_role_sub_replacement, content)
                    content = self._sourcecode_directive_regex.sub(self._sourcecode_directive_sub_replacement, content)
                # Output the document title + content
                if from_multiple_docs:
                    output.write( "\n" )
                    output.write( self._to_rest_title(document.title.encode('UTF8').strip(), character="=")+"\n\n" )
                output.write( content.encode('UTF8')+"\n" )
            else:
                # Output the document title only
                output.write( "* /%s/ : %s\n" % (document.slug.encode('UTF8'), document.title.encode('UTF8')) )
        
        return output

    def _to_rest_title(self, title, character="="):
        """Transform the document title to a ReST TOC title"""
        width = max([len(line) for line in title.splitlines()])
        ascii_line = character*width
        return ascii_line+"\n"+title+"\n"+ascii_line

    def _page_role_sub_replacement(self, matchobj):
        """Transform page roles to strong emphasis"""
        return u"**{name}**".format(name=matchobj.group(1))

    def _sourcecode_directive_sub_replacement(self, matchobj):
        """Transform sourcecode directives to pre"""
        return u"::"
        