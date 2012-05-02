# -*- coding: utf-8 -*-
"""
Board views
"""
from sveedocuments.models import Page, Insert
from sveedocuments.views import RestrictedTemplateView

class BoardIndex(RestrictedTemplateView):
    """
    Documents management board
    """
    template_name = "sveedocuments/board.html"

    def get(self, request, *args, **kwargs):
        context = {
            'page_list' : Page.objects.filter(),
            'insert_list' : Insert.objects.filter().order_by('slug'),
        }
        return self.render_to_response(context)
