"""
Common forum mixins
"""
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext, TemplateDoesNotExist

from guardian.conf import settings as guardian_settings
from guardian.mixins import PermissionRequiredMixin

class PageChangePermissionRequiredMixin(PermissionRequiredMixin):
    """
    Mixin to check for "page_change" permission with a Page object
    
    This used for views where self.object is not a Page instance.
    
    The page instance must be set in a "page_object" View attribute.
    """
    permission_required = 'sveedocuments.change_page'
    
    def check_permissions(self, request):
        perms = self.get_required_permissions(request)
        page_instance = (hasattr(self, 'get_page_object') and self.get_page_object()
            or getattr(self, 'page_object', None))
        has_permissions = False
        # global perms check first (if accept_global_perms)
        has_permissions = any(request.user.has_perm(perm) for perm in perms)
        # if still no permission granted, try obj perms
        if not has_permissions:
            has_permissions = any(request.user.has_perm(perm, page_instance) for perm in perms)
        
        # Raise a forbidden response if still no permission at all
        if not has_permissions:
            try:
                response = render_to_response(getattr(guardian_settings, 'TEMPLATE_403', '403.html'), {}, RequestContext(request))
                response.status_code = 403
                return response
            except TemplateDoesNotExist as e:
                if settings.DEBUG:
                    raise e
        return False
