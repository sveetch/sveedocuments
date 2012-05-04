# -*- coding: utf-8 -*-
"""
Page document views
"""
import json, os
from datetime import datetime

from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from sveedocuments import settings_local
from sveedocuments.models import Page
from sveedocuments.parser import SourceParser
from sveedocuments.forms import PageForm, PageQuickForm
from sveedocuments.views import RestrictedView, RestrictedCreateView, RestrictedUpdateView, RestrictedDeleteView
from sveedocuments.utils.objects import get_instance_children

class PageIndex(TemplateView):
    """
    Pages index
    """
    template_name = "sveedocuments/page_index.html"
    
    def get(self, request, *args, **kwargs):
        context = {'page_list' : Page.objects.filter(visible=True)}
        return self.render_to_response(context)

class HelpPage(TemplateView):
    """
    Help document
    """
    template_name = "sveedocuments/help.html"
    
    def get(self, request, *args, **kwargs):
        path_root = os.path.abspath(os.path.dirname(settings_local.__file__))
        f = open(os.path.join(path_root, "HELP.rst"))
        content = f.read()
        f.close()
        
        context = {'content' : SourceParser(content, silent=False)}
        return self.render_to_response(context)

class PagePreview(RestrictedView):
    """
    Parser preview
    
    Procède au rendu par le parser d'un contenu soumis par POST dans un argument "data", 
    une requête GET renvoi toujours un document complètement vide, de même si le contenu 
    est vide.
    
    Le contenu du parser est seulement un "fragment" de page et non une page complète, 
    en clair uniquement le rendu HTML du contenu à placer quelque part dans le <body/>.
    """
    def parse_content(self, request, *args, **kwargs):
        content = request.POST.get('content', None)
        if content:
            return SourceParser(content, silent=False)
        return ''

    def get(self, request, *args, **kwargs):
        return HttpResponse('')
    
    def post(self, request, *args, **kwargs):
        content = self.parse_content(request, *args, **kwargs)
        return HttpResponse( content )

class PageDetails(DetailView):
    """
    *Page* view
    """
    model = Page
    context_object_name = "page_instance"
    template_name = "sveedocuments/page_details.html"
    
    def get_object(self, *args, **kwargs):
        """
        Memorize object to avoid multiple database access when using ``get_object()`` 
        method
        """
        cache_key = "_cache_get_object"
        if not hasattr(self, cache_key):
            setattr(self, cache_key, super(PageDetails, self).get_object(*args, **kwargs))
        return getattr(self, cache_key)
    
    def get(self, request, **kwargs):
        # Check if the object is ``visible``
        if not self.get_object().visible:
            raise Http404
        return super(PageDetails, self).get(request, **kwargs)
    
    def get_template_names(self):
        return [self.object.get_template()]

class PageSource(PageDetails):
    """
    Raw content *Page* view
    """
    def get(self, request, *args, **kwargs):
        # Check if the object is ``visible``
        if not self.get_object().visible:
            raise Http404
        return HttpResponse(self.get_object().content, content_type="text/plain; charset=utf-8")

class PageCreate(RestrictedCreateView):
    """
    Form view to create a *Page* document
    """
    model = Page
    context_object_name = "page_instance"
    template_name = "sveedocuments/page_form.html"
    form_class = PageForm
    _redirect_to_self = False

    def get(self, request, *args, **kwargs):
        self.parent_page_instance = self._get_parent(**kwargs)
        return super(PageCreate, self).get(request, *args, **kwargs)
        
    def post(self, request, *args, **kwargs):
        self.parent_page_instance = self._get_parent(**kwargs)
        # Mark to go back to the form page after save, triggered by special submit
        if request.POST:
            if request.POST.get('submit_and_continue', False):
                self._redirect_to_self = True
        return super(PageCreate, self).post(request, *args, **kwargs)
        
    def get_success_url(self):
        if self._redirect_to_self:
            return reverse('documents-page-edit', args=[self.object.slug])
        return reverse('documents-board')

    def _get_parent(self, **kwargs):
        if 'slug' in kwargs:
            return get_object_or_404(Page, slug=kwargs['slug'])
        return None
        
    def get_context_data(self, **kwargs):
        context = super(PageCreate, self).get_context_data(**kwargs)
        context.update({
            'parent_page_instance': self.parent_page_instance,
        })
        return context
    
    def get_form_kwargs(self):
        kwargs = super(PageCreate, self).get_form_kwargs()
        kwargs.update({
            'author': self.request.user,
            'parent': self.parent_page_instance,
            'initial': {'published': datetime.today()},
        })
        return kwargs

class PageEdit(RestrictedUpdateView):
    """
    Form view to edit a *Page* document
    """
    model = Page
    context_object_name = "page_instance"
    template_name = "sveedocuments/page_form.html"
    form_class = PageForm
    _redirect_to_self = False
        
    def post(self, request, *args, **kwargs):
        # Mark to go back to the form page after save, triggered by special submit
        if request.POST:
            if request.POST.get('submit_and_continue', False):
                self._redirect_to_self = True
        return super(PageEdit, self).post(request, *args, **kwargs)

    def get_success_url(self):
        if self._redirect_to_self:
            return reverse('documents-page-edit', args=[self.object.slug])
        return reverse('documents-board')

    def get_form_kwargs(self):
        kwargs = super(PageEdit, self).get_form_kwargs()
        kwargs.update({'author': self.request.user})
        return kwargs

class PageQuicksave(PageEdit):
    """
    Quicksave view for a *Page* content
    """
    form_class = PageQuickForm
    
    def get_object(self, queryset=None):
        if self.request.POST.get('slug', False):
            self.kwargs['slug'] = self.request.POST['slug']
        return super(PageQuicksave, self).get_object(queryset=queryset)

    def get(self, request, *args, **kwargs):
        return HttpResponse('')
    
    def form_valid(self, form):
        content = json.dumps({'status':'form_valid'})
        form.save()
        return HttpResponse(content, content_type='application/json')

    def form_invalid(self, form):
        content = json.dumps({
            'status':'form_invalid',
            'errors': dict(form.errors.items()),
        })
        return HttpResponse(content, content_type='application/json')

class PageDelete(RestrictedDeleteView):
    """
    Form view to delete a *Page* document
    
    This display a tree of relations to confirm the object and relations deletion
    """
    model = Page
    context_object_name = "page_instance"
    template_name = "sveedocuments/page_delete.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context.update({'relations': get_instance_children(self.object)})
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse('documents-board')
