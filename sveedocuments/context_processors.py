# -*- coding: utf-8 -*-
"""
Context processors
"""
from sveedocuments.views.page import PagePDFView

def SveedocumentsContext(request):
    """
    Context processor to add some sveedocuments globals to template context
    """
    return {
        'pdf_export_enabled': not( getattr(PagePDFView, 'is_dummy', False) ),
    }
