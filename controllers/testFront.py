#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Evolutiva'


def index():

    my_dict = dict()


    my_dict['a_error']=''

    label_dict = dict(ICN='Rut', firstLastName='Apellido Paterno',
                      otherLastName='Apellido Materno')
    fields_dict = [
        'ICN',
        'firstName',
        'firstLastName',
        'otherLastName',
        'alias',
        'birth',
        'shortBio',
        'countryofResidence',
        'depiction',
    ]

    # hidden_dict = dict(state_publication='draft',date_publication=request.now,
        # state_colaboration=False)

    a_form = SQLFORM(db.persona, labels=label_dict, fields=fields_dict)

    # a_form.vars['state_publication']='draft'
    # a_form.vars['date_publication']=request.now
    # a_form.vars['state_colaboration']=False

    if a_form.process().accepted:
        # response.flash = 'form accepted'
        redirect(URL('accepted'))
    elif a_form.errors:
        my_dict['a_error'] = T('Ocurrio un error en el formulario')
        response.flash = 'form has errors'

    my_dict['form'] = a_form
    return my_dict

def accepted():

    return dict(form= a_form)

def grid():
    a_grid = SQLFORM.grid(db.auth_user,user_signature=False)
    return dict(grid= a_grid)

def display():

    label_dict = {'persona.ICN': T('Rut'),
                  'persona.firstLastName': T('Apellido Paterno'),
                  'persona.otherLastName': T('Apellido Materno')}

    show_fields = [db.persona.id, db.persona.ICN, db.persona.firstName,
                   db.persona.firstLastName, db.persona.otherLastName]

    grid = SQLFORM.grid(
        db.persona.state_publication=='draft',
        editable=True,
        details=False,
        user_signature=False,
        fields=show_fields,
        create=False,
        headers=label_dict,
        csv=False,
        paginate=25,
        searchable=False
        )

    # implementa plantilla main

    return dict(grid=grid)


def publicaciones_general():
    #grilla publicaciones general
    return locals()
    
def paginas_general():
    #grilla páginas general
    return locals()
    
def publicaciones_empresas():
    #grilla de publiaciones general
    return locals()
    
def usuarios_general():
    #lista de usuarios
    return locals()
    
def publicaciones_casos():
    #grilla de publicaciones casos
    return locals()
    
def publicaciones_organizaciones():
    #grilla de publicaciones organizaciones
    return locals()
    
def usuarios_historial():
    #historial de usuarios
    return locals()
