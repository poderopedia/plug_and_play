# -*- coding: utf-8 -*-
__author__ = 'Evolutiva'

def index():
    a_form = SQLForm(db.persona)
    return dict(form= a_form)
