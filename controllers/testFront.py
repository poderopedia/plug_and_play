# -*- coding: utf-8 -*-
__author__ = 'Evolutiva'

def index():
    a_form = SQLFORM(db.persona)
    if a_form.process().accepted:
       response.flash = 'form accepted'
    elif a_form.errors:
       response.flash = 'form has errors'

    return dict(form= a_form)
