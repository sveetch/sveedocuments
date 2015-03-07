# -*- coding: utf-8 -*-
"""
Insert documents management views
"""
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views import generic
from django.contrib import messages
from django.utils.translation import ugettext as _

from braces.views import PermissionRequiredMixin

from djangocodemirror.views import SampleQuicksaveMixin

from sveedocuments.models import Insert
from sveedocuments.forms.insert import InsertForm, InsertEditForm, InsertQuickForm
from sveedocuments.utils.objects import get_instance_children

class InsertCreateView(PermissionRequiredMixin, generic.CreateView):
    """
    Form view to create an *Insert* document
    """
    model = Insert
    context_object_name = "insert_instance"
    template_name = "sveedocuments/board/insert_form.html"
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
            return reverse('sveedocuments:insert-edit', args=[self.object.slug])
        return reverse('sveedocuments:insert-index')
    
    def form_valid(self, form):
        resp = super(InsertCreateView, self).form_valid(form)
        messages.add_message(self.request, messages.SUCCESS, _("Insert with slug <strong>{0}</strong> has been added successfully").format(self.object.slug), fail_silently=True)
        return resp
    
    def get_form_kwargs(self):
        kwargs = super(InsertCreateView, self).get_form_kwargs()
        kwargs.update({
            'author': self.request.user,
        })
        return kwargs

class InsertEditView(PermissionRequiredMixin, generic.UpdateView):
    """
    Form view to edit an *Insert* document
    """
    model = Insert
    context_object_name = "insert_instance"
    template_name = "sveedocuments/board/insert_form.html"
    form_class = InsertEditForm
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
            return reverse('sveedocuments:insert-edit', args=[self.object.slug])
        return reverse('sveedocuments:insert-index')
    
    def form_valid(self, form):
        resp = super(InsertEditView, self).form_valid(form)
        messages.add_message(self.request, messages.SUCCESS, _("Insert with slug <strong>{0}</strong> has been edited successfully").format(self.object.slug), fail_silently=True)
        return resp
    
    def get_form_kwargs(self):
        kwargs = super(InsertEditView, self).get_form_kwargs()
        kwargs.update({'author': self.request.user})
        return kwargs

class InsertDeleteView(PermissionRequiredMixin, generic.DeleteView):
    """
    Form view to delete an *Insert* document
    
    This display a tree of relations to confirm the object and relations deletion
    """
    model = Insert
    context_object_name = "insert_instance"
    template_name = "sveedocuments/board/insert_delete.html"
    permission_required = "sveedocuments.delete_insert"
    raise_exception = True

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context.update({'relations': get_instance_children(self.object)})
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.memoized_object_values = {'title':self.object.title, 'slug':self.object.slug, }
        return super(InsertDeleteView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        messages.add_message(
            self.request, messages.WARNING,
            _('Insert with slug <strong>{0}</strong> has been deleted successfully').format(self.memoized_object_values['slug']),
            fail_silently=True
        )
        return reverse('sveedocuments:insert-index')

class InsertQuicksaveView(SampleQuicksaveMixin, InsertEditView):
    """
    Quicksave view for an *Insert* content
    """
    form_class = InsertQuickForm
    
    def get_object(self, queryset=None):
        if self.request.POST.get('slug', False):
            self.kwargs['slug'] = self.request.POST['slug']
        return super(InsertQuicksaveView, self).get_object(queryset=queryset)
