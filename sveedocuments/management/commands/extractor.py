# -*- coding: utf-8 -*-
"""
Export/Import Command line tool

TODO: * Better command name;
      * Option to select only some items from entries;
      * Item fields to edit some other object field;

Use this tool with a JSON config that contain mapping between Pages object and files.

Export
------

This will fetch items from the database and create it as files (or rewrite them if exists).

If an item filepath directory destination does not exists this will raise a CommandError. 

Use '--smart' option to automatically create missing directories. Take care before that your 
filepath destination is correct.

Import
------

This will read items filepath and import their content into their Pages.

If a slug does not exists this will raise a CommandError.

Use '--smart' option to automatically create a new Page if it does not exist yet. It will use the slug as the title, all other fields are let at their default value except the 'author'.

Pages are created or edited with the given 'author' if any, else with the default 
author (the first superuser). And the 'comment' is something like 
"Imported from 'FILE'".

Sample :

[
    {
        "kind": "export",
        "name": "Exporting project README's",
        "items": [
            {
                "slug": "djangosveetchies",
                "filepath": "./README.2.rst"
            },
            ...
        ]
    },
    {
        "kind": "import",
        "author": "sveetch",
        "name": "Importing project README's",
        "items": [
            {
                "slug": "djangosveetchies",
                "filepath": "./README.rst"
            },
            ...
        ]
    },
    ...
]

"""
import os, json, StringIO

from optparse import OptionValueError, make_option

from django.conf import settings
from django.core.management.base import CommandError, BaseCommand
from django.contrib.auth.models import User

from sveedocuments.models import Page

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option("--config", dest="config_file", default=None, help="JSON config file", metavar="FILEPATH"),
        make_option("--smart", dest="smart", action="store_true", default=False, help="If used, path destination that does not exist will be created if needed in Export mode, in Import mode this will create entry that does not allready exist. Be carefull, if your filepath entry is incorrect, this can do some mess on your Filesystem or Database."),
        make_option("--dry-run", dest="dry_run", action="store_true", default=False, help="Does not create any file or edit database, just do all the process"),
    )
    help = "Import/export command line tool"

    def handle(self, *args, **options):
        if len(args) != 0:
            raise CommandError("Command doesn't accept any arguments")
        
        config_file = options.get('config_file')
        self.verbosity = int(options.get('verbosity'))
        self.dry_run = int(options.get('dry_run'))
        self.smart = int(options.get('smart'))
        
        if not config_file:
            raise CommandError("You need to specify a config file")
        
        self.configs = self.parse_config_file(config_file)
        self.proceed()

    def parse_config_file(self, config_file):
        """
        Open the config file, validate it, fill in some useful datas and return it
        """
        items = []
        default = {
            "name": None,
            "prepend_path": None,
            "backup": False,
            "author": None,
        }
        
        # Default author is the first superuser finded
        self.default_author = User.objects.filter(is_superuser=True)[0]
        
        _configs = json.load(open(config_file))
        
        for i, entry in enumerate(_configs, start=1):
            if "name" not in entry or not entry.get("name"):
                entry["name"] = "Entry {0}".format(i)
            if "kind" not in entry or entry.get("kind") not in ["export", "import"]:
                raise CommandError("{0} : Missing a correct value for the 'kind' key".format(entry["name"]))
            if "author" in entry and entry.get("kind"):
                try:
                    entry["author"] = User.objects.get(username=entry["author"])
                except User.DoesNotExist:
                    raise CommandError("{0} : 'author' key : username '{1}' does not exist".format(entry["name"], entry["author"]))
            
            for j, item in enumerate(entry["items"], start=1):
                # Required keys
                if "slug" not in item or "filepath" not in item:
                    raise CommandError("{0} : Item #{1} must have 'slug' and 'filepath' keys.".format(entry["name"], j))
                # Check the page object
                item["object"] = None
                try:
                    item["object"] = Page.objects.get(slug=item["slug"])
                except Page.DoesNotExist:
                    if entry["kind"]=='export' or (entry["kind"]=='import' and not self.smart):
                        raise CommandError("{0} : Item #{1} : slug '{2}' does not exist".format(entry["name"], j, item["slug"]))
                        
                # Check filepath
                item["filepath"] = os.path.abspath(item["filepath"])
                item["_filepath_dir"], item["_filepath_filename"] = os.path.split(item["filepath"])
                if not self.smart and not os.path.exists(item["_filepath_dir"]):
                    raise CommandError("{0} : Item #{1} : filepath directory '{2}' does not exist, use --smart if you want to automatically create it.".format(entry["name"], j, item["_filepath_dir"]))
                if entry["kind"]=='import' and not os.path.exists(item["filepath"]):
                    raise CommandError("{0} : Item #{1} : filepath '{2}' does not exist.".format(entry["name"], j, item["filepath"]))
            
            _cfg = default.copy()
            _cfg.update(entry)
            items.append(_cfg)
        
        return items

    def proceed(self):
        """
        Proceed to the entry action 
        """
        for i, entry in enumerate(self.configs, start=1):
            if hasattr(self, "do_{0}".format(entry["kind"])):
                getattr(self, "do_{0}".format(entry["kind"]))(entry)
            else:
                raise CommandError("{0} : Command method for kind '{1}' does not exist.".format(entry["name"], entry["kind"]))

    def do_import(self, entry):
        """
        Import documents from their file destination to their database object
        """
        if self.verbosity > 0:
            print "=== Import '{0}' ===".format(entry["name"])
        
        for i, item in enumerate(entry['items'], start=1):
            # Get the content to import
            fp = open(item["filepath"], 'r')
            new_content = fp.read()
            fp.close()
            author = entry.get("author") or self.default_author
            if item["object"] is None and self.smart:
                item["object"] = Page(title=item["slug"], slug=item["slug"], author=author, content=new_content)
                if self.verbosity > 0:
                    print "Document '{0}' does not exist, create it".format(item["slug"])
            else:
                item["object"].author = author
                item["object"].content = new_content
                if self.verbosity > 0:
                    print "Document '{0}' updated".format(item["slug"])
                
            item["object"].comment = "Imported from file '{0}'".format(item["_filepath_filename"])
            
            if not self.dry_run:
                item["object"].save()

    def do_export(self, entry):
        """
        Export documents to their given file destination
        """
        if self.verbosity > 0:
            print "=== Export '{0}' ===".format(entry["name"])
            
        for i, item in enumerate(entry['items'], start=1):
            # Create the missing dir if smart mode is enabled
            if self.smart and not os.path.exists(item["_filepath_dir"]):
                if not self.dry_run:
                    os.makedirs(item["_filepath_dir"])
            # Create the file to its destination
            if not self.dry_run:
                fp = open(item["filepath"], 'w')
                fp.write(item['object'].content.encode('UTF8'))
                fp.close()
            if self.verbosity > 0:
                print "Document '{0}' writed to: {1}".format(item["slug"], item["filepath"])
