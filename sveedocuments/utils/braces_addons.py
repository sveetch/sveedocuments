import datetime, json

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.list import BaseListView
from django.views.generic.edit import BaseDeleteView, FormMixin

from braces.views import JSONResponseMixin

class DownloadMixin(object):
    """
    Simple Mixin to send a downloadable content
    
    Inherits must have :
    
    * Filled the ``self.content_type`` attribute with the content content_type to send;
    * Implementation of ``get_filename()`` that return the filename to use in response 
      headers;
    * Implementation of ``get_content()`` that return the content to send as downloadable.
    
    If the content is a not a string, it is assumed to be a fileobject to send as 
    the content with its ``read()`` method.
    
    Optionnaly implement a ``close_content()`` to close specifics objects linked to 
    content fileobject, if it does not exists a try will be made on a close() method 
    on the content fileobject;
    
    A "get_filename_timestamp" method is implemented to return a timestamp to use in your 
    filename if needed, his date format is defined in "timestamp_format" attribute (in a 
    suitable way to use with strftime on a datetime object).
    """
    content_type = None
    timestamp_format = "%Y-%m-%d"
    
    def get_filename_timestamp(self):
        return datetime.datetime.now().strftime(self.timestamp_format)
    
    def get_filename(self, context):
        raise ImproperlyConfigured("DownloadMixin requires an implementation of 'get_filename()' to return the filename to use in headers")
    
    def get_content(self, context):
        raise ImproperlyConfigured("DownloadMixin requires an implementation of 'get_content()' to return the downloadable content")
    
    def render_to_response(self, context, **response_kwargs):
        if getattr(self, 'content_type', None) is None:
            raise ImproperlyConfigured("DownloadMixin requires a definition of 'content_type' attribute")
        # Needed headers
        response = HttpResponse(content_type=self.content_type, **response_kwargs)
        response['Content-Disposition'] = 'attachment; filename={0}'.format(self.get_filename(context))
        # Read the content file object or string, append it to response and close it
        content = self.get_content(context)
        if isinstance(content, basestring):
            response.write(content)
        else:
            response.write(content.read())
        # Conditionnal closing content object
        if hasattr(self, 'close_content'):
            self.close_content(context, content)
        elif hasattr(content, 'close'):
            content.close()
            
        return response

    def get_context_data(self, **kwargs):
        return {
            'params': kwargs
        }

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class ExtendTemplateVariableMixin(object):
    """
    Get the extend variable to use in the template
    
    Default behaviour is to switch on two templates depending on the request is an ajax 
    request or not, if ajax "base_modal.html" is used else the default extend will 
    simply be "base.html".
    
    This only put the "template_extend" variable in the template context, your template 
    have to use it, this does not modify itself the response nor the template.
    """
    default_extend_template = "base.html"
    modal_extend_template = "base_modal.html"
    
    def get_template_extend(self):
        if self.request.is_ajax():
            return self.modal_extend_template
        return self.default_extend_template
    
    def get_context_data(self, **kwargs):
        context = super(ExtendTemplateVariableMixin, self).get_context_data(**kwargs)
        context.update({
            'template_extend': self.get_template_extend(),
        })
        return context


class SimpleListView(TemplateResponseMixin, BaseListView):
    """
    Like generic.ListView but use only ``get_template`` to find template and not an 
    automatic process on ``get_template_names``
    """
    pass


class DirectDeleteView(BaseDeleteView):
    """
    To directly delete an object without template rendering on GET or POST methods
    
    "get_success_url" or "success_url" should be correctly filled
    """
    memoize_old_object = False
    _memoized_attr = ['id', 'slug', 'title'] # memoized attributes if exists
    old_object = {} # where the attributes will be putted
    
    def get(self, *args, **kwargs):
        if self.memoize_old_object:
            self.memoize_object()
        return self.delete(*args, **kwargs)
    
    def memoize_object(self, *args, **kwargs):
        old = self.get_object()
        for item in self._memoized_attr:
            self.old_object[item] = getattr(old, item, None)


class ListAppendView(SimpleListView, FormMixin):
    """
    A view to display an object list with a form to append a new object
    
    This view re-use some code from FormMixin and SimpleListView, sadly it seem not 
    possible to simply mix them.
    
    Need "model" and "form_class" attributes for the form parts and the required one 
    by BaseListView. "get_success_url" method should be filled too.
    
    "locked_form" is used to disable form (like if your list object is closed to new 
    object)
    """
    model = None
    form_class = None
    template_name = None
    paginate_by = None
    locked_form = False
    
    def form_valid(self, form):
        self.object = form.save()
        return super(ListAppendView, self).form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(object_list=self.object_list, form=form))

    def is_locked_form(self):
        return self.locked_form

    def get_form(self, form_class):
        """
        Returns an instance of the form to be used in this view.
        """
        if self.is_locked_form():
            return None
        return form_class(**self.get_form_kwargs())
        
    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        
        allow_empty = self.get_allow_empty()
        if not allow_empty and len(self.object_list) == 0:
            raise Http404(_(u"Empty list and '%(class_name)s.allow_empty' is False.")
                          % {'class_name': self.__class__.__name__})
        
        context = self.get_context_data(object_list=self.object_list, form=form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        
        allow_empty = self.get_allow_empty()
        if not allow_empty and len(self.object_list) == 0:
            raise Http404(_(u"Empty list and '%(class_name)s.allow_empty' is False.")
                          % {'class_name': self.__class__.__name__})
        
        if form and form.is_valid():
            return self.form_valid(form)
        elif form:
            return self.form_invalid(form)
        else:
            context = self.get_context_data(object_list=self.object_list, form=form)
            return self.render_to_response(context)

    def put(self, *args, **kwargs):
        return self.post(*args, **kwargs)

class DetailListAppendView(ListAppendView):
    """
    A view to display a parent object details, list his "children" and display a form 
    to append a new child
    
    Have the same behaviours than "ListAppendView" but get the parent object before 
    doing anything.
    
    "model" and "form_class" attribute are for the children, "context_parent_object_name" 
    is used to name the parent variable in the template context.
    
    "get_parent_object" must be defined to return the parent instance and also "get_queryset" 
    to filter queryset only for the children of the parent.
    
    The parent object is also given to the append form, under the name defined with the 
    "context_parent_object_name" attribute. Your Form should be aware of this.
    """
    context_parent_object_name = 'parent_object'
    
    def get_parent_object(self):
        raise ImproperlyConfigured(u"%(cls)s's 'get_parent_object' method must be defined " % {"cls": self.__class__.__name__})

    def get_context_data(self, **kwargs):
        kwargs.update({
            self.context_parent_object_name: self.parent_object,
        })
        return super(DetailListAppendView, self).get_context_data(**kwargs)
        
    def get_form_kwargs(self):
        """
        Returns an instance of the form to be used in this view.
        """
        kwargs = super(DetailListAppendView, self).get_form_kwargs()
        kwargs.update({
            self.context_parent_object_name: self.parent_object,
        })
        return kwargs
        
    def get(self, request, *args, **kwargs):
        self.parent_object = self.get_parent_object()
        return super(DetailListAppendView, self).get(request, *args, **kwargs)
        
    def post(self, request, *args, **kwargs):
        self.parent_object = self.get_parent_object()
        return super(DetailListAppendView, self).post(request, *args, **kwargs)

class JSONResponseExtendedMixin(JSONResponseMixin):
    """
    Simple Mixin to compile the context view as JSON
    
    This does not implement a direct response, you have to return it with the 
    ``json_to_response`` method in your view.
    """
    json_indent = None
    json_encoder = DjangoJSONEncoder
    json_ensure_ascii = False
    
    def encode_context(self, context):
        json_kwargs = {}
        if self.json_indent is not None:
            json_kwargs['indent'] = self.json_indent
        if self.json_encoder is not None:
            json_kwargs['encoder'] = self.json_encoder
        if self.json_ensure_ascii is not None:
            json_kwargs['ensure_ascii'] = self.json_ensure_ascii
        return json.dumps(context, **json_kwargs)

    def render_json_response(self, context_dict, **response_kwargs):
        """
        Limited serialization for shipping plain data. Do not use for models
        or other complex or custom objects.
        """
        if 'content_type' not in response_kwargs:
            response_kwargs['content_type'] = self.get_content_type()
        return HttpResponse(self.encode_context(context), **response_kwargs)


class JSONResponseViewMixin(JSONResponseExtendedMixin):
    """Mixin to directly return a JSON response"""
    def render_to_response(self, context, **response_kwargs):
        """
        Returns a response with a template rendered with the given context.
        """
        return self.json_to_response(context)
