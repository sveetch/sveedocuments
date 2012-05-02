# -*- coding: utf-8 -*-
from django.views import generic
from django.contrib.auth.decorators import login_required, permission_required

class RestrictedView(generic.View):
    """
    Generic view that check login_required
    """
    def dispatch(self, request, *args, **kwargs):
        @login_required
        def wrapper(request, *args, **kwargs):
            return super(RestrictedView, self).dispatch(request, *args, **kwargs)
        return wrapper(request, *args, **kwargs)

class RestrictedTemplateView(generic.TemplateView):
    """
    Generic template view that check login_required
    """
    def dispatch(self, request, *args, **kwargs):
        @login_required
        def wrapper(request, *args, **kwargs):
            return super(RestrictedTemplateView, self).dispatch(request, *args, **kwargs)
        return wrapper(request, *args, **kwargs)

class RestrictedListView(generic.ListView):
    """
    Generic list view that checks permissions
    """
    def dispatch(self, request, *args, **kwargs):
        @permission_required('%s.change_%s' % (self.model._meta.app_label, self.model._meta.module_name))
        def wrapper(request, *args, **kwargs):
            return super(RestrictedListView, self).dispatch(request, *args, **kwargs)
        return wrapper(request, *args, **kwargs)

class RestrictedUpdateView(generic.UpdateView):
    """
    Generic update view that checks permissions
    """
    def dispatch(self, request, *args, **kwargs):
        @permission_required('%s.change_%s' % (self.model._meta.app_label, self.model._meta.module_name))
        def wrapper(request, *args, **kwargs):
            return super(RestrictedUpdateView, self).dispatch(request, *args, **kwargs)
        return wrapper(request, *args, **kwargs)

class RestrictedCreateView(generic.CreateView):
    """
    Generic create view that checks permissions
    """
    def dispatch(self, request, *args, **kwargs):
        @permission_required('%s.add_%s' % (self.model._meta.app_label, self.model._meta.module_name))
        def wrapper(request, *args, **kwargs):
            return super(RestrictedCreateView, self).dispatch(request, *args, **kwargs)
        return wrapper(request, *args, **kwargs)

class RestrictedDeleteView(generic.DeleteView):
    """
    Generic delete view that checks permissions
    """
    def dispatch(self, request, *args, **kwargs):
        @permission_required('%s.delete_%s' % (self.model._meta.app_label, self.model._meta.module_name))
        def wrapper(request, *args, **kwargs):
            return super(RestrictedDeleteView, self).dispatch(request, *args, **kwargs)
        return wrapper(request, *args, **kwargs)
