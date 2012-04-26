# -*- coding: utf-8 -*-
"""
Template tags used in admin or board
"""
from django import template

register = template.Library()

@register.filter(name='calcul_indent')
def calcul_indent(value, coef=20):
    return (value+1)*coef
