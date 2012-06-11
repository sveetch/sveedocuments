# -*- coding: utf-8 -*-
"""
Insert document views
"""
import json

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views import generic

from braces.views import LoginRequiredMixin, PermissionRequiredMixin

from sveedocuments.models import Insert
from sveedocuments.parser import SourceParser
from sveedocuments.forms import InsertForm, InsertQuickForm
from sveedocuments.utils.objects import get_instance_children

class InsertCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    """
    Form view to create an *Insert* document
    """
    model = Insert
    context_object_name = "insert_instance"
    template_name = "sveedocuments/insert_form.html"
    form_class = InsertForm
    permission_required = "sveedocuments.add_insert"
    raise_exception = True
    _redirect_to_self = False

    def post(self, request, *args, **kwargs):
        # Mark to go back to the form page after save, triggered by special submit
        if request.POST:
            if request.POST.get('submit_and_continue', False):
                self._redirect_to_self = True
        return super(InsertCreateView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        if self._redirect_to_self:
            return reverse('documents-insert-edit', args=[self.object.slug])
        return reverse('documents-board')
    
    def get_form_kwargs(self):
        kwargs = super(InsertCreateView, self).get_form_kwargs()
        kwargs.update({
            'author': self.request.user,
        })
        return kwargs

class InsertEditView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    """
    Form view to edit an *Insert* document
    """
    model = Insert
    context_object_name = "insert_instance"
    template_name = "sveedocuments/insert_form.html"
    form_class = InsertForm
    permission_required = "sveedocuments.change_insert"
    raise_exception = True
    _redirect_to_self = False

    def post(self, request, *args, **kwargs):
        # Mark to go back to the form page after save, triggered by special submit
        if request.POST:
            if request.POST.get('submit_and_continue', False):
                self._redirect_to_self = True
        return super(InsertEditView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        if self._redirect_to_self:
            return reverse('documents-insert-edit', args=[self.object.slug])
        return reverse('documents-board')
    
    def get_form_kwargs(self):
        kwargs = super(InsertEditView, self).get_form_kwargs()
        kwargs.update({'author': self.request.user})
        return kwargs

class InsertQuicksaveView(InsertEditView):
    """
    Quicksave view for an *Insert* content
    """
    form_class = InsertQuickForm
    
    def get_object(self, queryset=None):
        if self.request.POST.get('slug', False):
            self.kwargs['slug'] = self.request.POST['slug']
        return super(InsertQuicksaveView, self).get_object(queryset=queryset)

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

class InsertDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    """
    Form view to delete an *Insert* document
    
    This display a tree of relations to confirm the object and relations deletion
    """
    model = Insert
    context_object_name = "insert_instance"
    template_name = "sveedocuments/insert_delete.html"
    permission_required = "sveedocuments.delete_insert"
    raise_exception = True

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context.update({'relations': get_instance_children(self.object)})
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse('documents-board')
