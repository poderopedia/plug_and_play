#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Evolutiva'


def index():
    return locals()


def persona():

    my_dict = dict()

    my_dict['a_error'] = ''

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

    a_form = SQLFORM(db.persona, labels=label_dict, fields=fields_dict,
                     submit_button=T('Sugerir'))

    if a_form.process().accepted:
        response.flash = 'Sugerencia Aceptada'
    elif a_form.errors:
        my_dict['a_error'] = T('Ocurrio un error en el formulario')
        response.flash = 'Formulario con errores'

    my_dict['form'] = a_form
    return my_dict


def organizacion():

    my_dict = dict()

    my_dict['a_error'] = ''

    label_dict = dict(ICN='Rut', firstLastName='Apellido Paterno',
                      otherLastName='Apellido Materno')
    fields_dict = [
        'hasSocialReason',
        'tipoOrg',
        'alias',
        'birth',
        'shortBio',
        'countryOfResidence',
        'depiction',
        ]

    # hidden_dict = dict(state_publication='draft',date_publication=request.now,
        # state_colaboration=False)

    a_form = SQLFORM(db.Organizacion, fields=fields_dict,
                     submit_button=T('Sugerir'))

    if a_form.process().accepted:
        response.flash = 'Sugerencia Aceptada'
        # redirect(URL('accepted'))
    elif a_form.errors:
        my_dict['a_error'] = T('Ocurrio un error en el formulario')
        response.flash = 'Formulario con errores'

    my_dict['form'] = a_form
    return my_dict


def grid():
    a_grid = SQLFORM.grid(db.auth_user, user_signature=False)
    return dict(grid=a_grid)


@auth.requires_login()
def display():

    return locals()

def display_persona():
    label_dict_persona = {'persona.ICN': T('Rut'),
                          'persona.firstLastName': T('Apellido Paterno'
                          ),
                          'persona.otherLastName': T('Apellido Materno'
                          )}

    show_fields_persona = [db.persona.id, db.persona.ICN,
                           db.persona.firstName,
                           db.persona.firstLastName,
                           db.persona.otherLastName]

    persona_grid = SQLFORM.grid(
        db.persona.state_publication == 'draft',
        editable=True,
        details=False,
        user_signature=False,
        fields=show_fields_persona,
        create=False,
        headers=label_dict_persona,
        csv=False,
        paginate=10,
        searchable=False,
        selectable=lambda ids: redirect(URL('testFront',
                'accept_persona', vars=dict(id=ids))),
        formname='persona_grid_form',
        )

    if persona_grid.element('.web2py_table input[type=submit]'):
        persona_grid.element('.web2py_table input[type=submit]'
                             )['_value'] = \
            T('Aceptar Personas Seleccionadas')
    elif persona_grid.element('.web2py_grid input[type=submit]'):
        persona_grid.element('.web2py_grid input[type=submit]')['_value'
                ] = T('Aceptar')

    return dict(persona_grid=persona_grid)


def accept_persona():

    ids_to_accept = request.vars['id']

    names= []
    for a_id in ids_to_accept:
        query = (( db.persona.id == a_id ))
        names.append(query)

    return dict(a='test', nombres = names, b = ids_to_accept)


def display_organizacion():
    label_dict_organizacion = \
        {'tipoOrganizacion.name': T('Tipo Organización')}

    show_fields_organizacion = [db.Organizacion.id,
                                db.tipoOrganizacion.name,
                                db.Organizacion.hasSocialReason,
                                db.Organizacion.alias]

    query = (db.Organizacion.tipoOrg == db.tipoOrganizacion.id) \
        & (db.Organizacion.state_publication == 'draft')
    organizacion_grid = SQLFORM.grid(
        query,
        editable=True,
        details=False,
        user_signature=False,
        fields=show_fields_organizacion,
        headers=label_dict_organizacion,
        create=False,
        csv=False,
        paginate=10,
        searchable=False,
        selectable=lambda ids: redirect(URL('testFront',
                'accept_organizacion', vars=dict(id=ids))),
        formname='organizacion_grid_form',
        )

    if organizacion_grid.element('.web2py_table input[type=submit]'):
        organizacion_grid.element('.web2py_table input[type=submit]'
                                  )['_value'] = \
            T('Aceptar Organizaciones Seleccionadas')
    elif organizacion_grid.element('.web2py_grid input[type=submit]'):
        organizacion_grid.element('.web2py_grid input[type=submit]'
                                  )['_value'] = T('Aceptar')

    # implementa plantilla main

    return dict(organizacion_grid=organizacion_grid)


def publicaciones_general():

    # grilla publicaciones general

    return locals()


def paginas_general():

    # grilla páginas general

    return locals()


def publicaciones_empresas():

    # grilla de publiaciones general

    return locals()


def usuarios_general():

    # lista de usuarios

    return locals()


def publicaciones_casos():

    # grilla de publicaciones casos

    return locals()


def publicaciones_organizaciones():

    # grilla de publicaciones organizaciones

    return locals()


def usuarios_historial():

    # historial de usuarios

    return locals()
