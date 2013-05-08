#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Evolutiva'

def index():
    # Vista principal de sugerencia, contiene actualmente link a sugerencias
    return locals()

################################################################################
################################################################################
# Funciones de Sugerencia de Perfiles

def add_persona():

    # Formulario de ingreso de sugerencia para personas

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

    a_form = SQLFORM(db.persona, labels=label_dict, fields=fields_dict,
                     submit_button=T('Sugerir'))

    if a_form.process().accepted:
        response.flash = 'Sugerencia Aceptada'
    elif a_form.errors:
        my_dict['a_error'] = T('Ocurrió un error en el formulario')
        response.flash = 'Formulario con errores'

    my_dict['form'] = a_form
    return my_dict


def add_organizacion():

    # Formulario de ingreso de sugerencia para organizaciones

    my_dict = dict()

    my_dict['a_error'] = ''

    label_dict = dict(ICN=T('Rut'), firstLastName=T('Apellido Paterno'
                      ), otherLastName=T('Apellido Materno'))
    fields_dict = [
        'hasSocialReason',
        'tipoOrg',
        'alias',
        'birth',
        'shortBio',
        'countryOfResidence',
        'depiction',
        ]

    a_form = SQLFORM(db.Organizacion, fields=fields_dict,
                     submit_button=T('Sugerir'))

    if a_form.process().accepted:
        response.flash = 'Sugerencia Aceptada'
    elif a_form.errors:

        # redirect(URL('accepted'))

        response.flash = 'Formulario con errores'

    my_dict['form'] = a_form
    return my_dict

def add_empresa():

    # Formulario de ingreso de sugerencia para empresas
    db.Organizacion.tipoOrg.default = 2;
    my_dict = dict()

    my_dict['a_error'] = ''

    label_dict = dict(ICN=T('Rut'), firstLastName=T('Apellido Paterno'
                      ), otherLastName=T('Apellido Materno'))
    fields_dict = [
        'hasSocialReason',
        'alias',
        'birth',
        'shortBio',
        'countryOfResidence',
        'depiction',
        ]

    a_form = SQLFORM(db.Organizacion, fields=fields_dict,
                     submit_button=T('Sugerir'))

    if a_form.process().accepted:
        response.flash = 'Sugerencia Aceptada'
    elif a_form.errors:

        # redirect(URL('accepted'))

        response.flash = 'Formulario con errores'

    my_dict['form'] = a_form
    return my_dict

def add_caso():

    # Formulario de ingreso de sugerencia para empresas
    db.Organizacion.tipoOrg.default = 2;
    my_dict = dict()

    my_dict['a_error'] = ''

    label_dict = dict(ICN=T('Rut'), firstLastName=T('Apellido Paterno'
                      ), otherLastName=T('Apellido Materno'))
    fields_dict = [
        'hasSocialReason',
        'alias',
        'birth',
        'shortBio',
        'countryOfResidence',
        'depiction',
        ]

    a_form = SQLFORM(db.Organizacion, fields=fields_dict,
                     submit_button=T('Sugerir'))

    if a_form.process().accepted:
        response.flash = 'Sugerencia Aceptada'
    elif a_form.errors:

        # redirect(URL('accepted'))

        response.flash = 'Formulario con errores'

    my_dict['form'] = a_form
    return my_dict


################################################################################
################################################################################
# Seccion de administracion de los perfiles sugeridos
################################################################################
################################################################################

@auth.requires(auth.has_membership(group_id = 'superadmin') or auth.has_membership(group_id = 'admin') or auth.has_membership(group_id = 'editor'))
def admin_suggestion():

    # Vista para mostrar el listado de personas y organizaciones sugeridas

    if len(request.args) == 0:
        redirect(URL('suggestion','admin_suggestion', args='persona'))

    return locals()

################################################################################
################################################################################
# Funciones para administrar perfiles de personas

@auth.requires(auth.has_membership(group_id = 'superadmin') or auth.has_membership(group_id = 'admin') or auth.has_membership(group_id = 'editor'))
def display_persona():

    # Componente el cual muestra la grilla de personas sugeridas

    label_dict_persona = {'persona.ICN': T('Rut'),
                          'persona.firstLastName': T('Apellido Paterno'
                          ),
                          'persona.otherLastName': T('Apellido Materno'
                          )}

    show_fields_persona = [db.persona.id, db.persona.ICN,
                           db.persona.firstName,
                           db.persona.firstLastName,
                           db.persona.otherLastName]

    persona_grid = SQLFORM.grid(  # selectable=lambda ids: redirect(URL('sugerencia',
                                  #         'accept_persona', vars=dict(id=ids))),
        db.persona.state_collaboration == 'for_revision',
        editable=True,
        details=False,
        deletable=False,
        user_signature=True,
        fields=show_fields_persona,
        create=False,
        headers=label_dict_persona,
        csv=False,
        paginate=10,
        searchable=False,
        formname='persona_grid_form',
        links=[lambda row: A(T('Aceptar'), _class='w2p_trap button btn'
               , _href=URL('suggestion', 'accept_persona',
               vars=dict(id=row.id))), lambda row: A(T('Rechazar'),
               _class='w2p_trap button btn', _href=URL('suggestion',
               'reject_persona', vars=dict(id=row.id)))],
        )

    if persona_grid.element('.web2py_counter'):
        persona_grid.element('.web2py_counter')[0] = ''

    if persona_grid.element('.web2py_table input[type=submit]'):

        persona_grid.element('.web2py_table input[type=submit]'
                             )['_value'] = \
            T('Aceptar Personas Seleccionadas')

        persona_grid.element('.web2py_table input[type=submit]'
                             )['_class'] = 'buttontext button'
    elif persona_grid.element('.web2py_grid input[type=submit]'):

        persona_grid.element('.web2py_grid input[type=submit]')['_value'
                ] = T('Aceptar')

    return dict(persona_grid=persona_grid)

@auth.requires(auth.has_membership(group_id = 'superadmin') or auth.has_membership(group_id = 'admin') or auth.has_membership(group_id = 'editor'))
def accept_persona():

    # Funcion que pasa el estado de colaboracion de revision a aceptado
    # para las personas seleccionadas en la grilla

    if 'id' in request.vars:
        ids_to_accept = request.vars['id']
    else:
        session.flash = T('Ninguna Persona seleccionada')

    # if len(ids_to_accept) == 1:
    a_id = int(ids_to_accept)
    a_persona = db(db.persona.id == a_id).select().first()
    a_persona.state_collaboration ='accepted'
    a_persona.update_record()

    session.flash = T('Sugerencia Aceptada')
    redirect(URL('display_persona'))

    return dict()

@auth.requires(auth.has_membership(group_id = 'superadmin') or auth.has_membership(group_id = 'admin') or auth.has_membership(group_id = 'editor'))
def reject_persona():

    # Funcion que pasa el estado de colaboracion de revision a aceptado
    # para las personas seleccionadas en la grilla

    if 'id' in request.vars:
        ids_to_accept = request.vars['id']
    else:
        session.flash = T('Ninguna Persona seleccionada')

    # if len(ids_to_accept) == 1:
    a_id = int(ids_to_accept)
    a_persona = db(db.persona.id == a_id).select().first()
    a_persona.state_collaboration ='rejected'
    a_persona.update_record()

    session.flash = T('Sugerencia Rechazada')
    redirect(URL('display_persona'))

    return dict()

################################################################################
################################################################################
# Funciones para administrar perfiles de organizaciones

@auth.requires(auth.has_membership(group_id = 'superadmin') or auth.has_membership(group_id = 'admin') or auth.has_membership(group_id = 'editor'))
def display_organizacion():

    # Componente el cual muestra la grilla de organizaciones sugeridas

    label_dict_organizacion = \
        {'tipoOrganizacion.name': T('Tipo Organización')}

    show_fields_organizacion = [db.Organizacion.id,
                                db.Organizacion.tipoOrg,
                                # db.tipoOrganizacion.name,
                                db.Organizacion.hasSocialReason,
                                db.Organizacion.alias]

    db.Organizacion.tipoOrg.represent=lambda id,row: db.tipoOrganizacion(id).name

    query = (db.Organizacion.tipoOrg == db.tipoOrganizacion.id) \
        & (db.Organizacion.state_collaboration == 'for_revision')

    organizacion_grid = SQLFORM.grid(
        query,
        editable=True,
        details=False,
        user_signature=True,
        deletable=False,
        fields=show_fields_organizacion,
        headers=label_dict_organizacion,
        create=False,
        csv=False,
        paginate=10,
        searchable=False,
        links=[lambda row: A(T('Aceptar'), _class='w2p_trap button btn'
               , _href=URL('suggestion', 'accept_organizacion',
               vars=dict(id=row.id))), lambda row: A(T('Rechazar'),
               _class='w2p_trap button btn', _href=URL('suggestion',
               'reject_organizacion', vars=dict(id=row.id)))],
        links_in_grid=True,
        formname='organizacion_grid_form',
        )

    if organizacion_grid.element('.web2py_counter'):
        organizacion_grid.element('.web2py_counter')[0] = ''

    if organizacion_grid.element('.web2py_table input[type=submit]'):

        organizacion_grid.element('.web2py_table input[type=submit]'
                                  )['_value'] = \
            T('Aceptar Organizaciones Seleccionadas')
    elif organizacion_grid.element('.web2py_grid input[type=submit]'):
        organizacion_grid.element('.web2py_grid input[type=submit]'
                                  )['_value'] = T('Aceptar')

    return dict(organizacion_grid=organizacion_grid)

@auth.requires(auth.has_membership(group_id = 'superadmin') or auth.has_membership(group_id = 'admin') or auth.has_membership(group_id = 'editor'))
def accept_organizacion():

    # Funcion que pasa el estado de colaboracion de revision a aceptado
    # para las organizaciones seleccionadas en la grilla

    if 'id' in request.vars:
        ids_to_accept = request.vars['id']
    else:
        session.flash = T('Ninguna Organizacion seleccionada')

    # if len(ids_to_accept) == 1:
    a_id = int(ids_to_accept)
    a_org = db(db.Organizacion.id == a_id).select().first()
    a_org.state_collaboration ='accepted'
    a_org.update_record()

    session.flash = T('Sugerencia Aceptada')
    redirect(URL('display_organizacion'))

    return dict()

@auth.requires(auth.has_membership(group_id = 'superadmin') or auth.has_membership(group_id = 'admin') or auth.has_membership(group_id = 'editor'))
def reject_organizacion():

    # Funcion que pasa el estado de colaboracion de revision a aceptado
    # para las organizaciones seleccionadas en la grilla

    if 'id' in request.vars:
        ids_to_accept = request.vars['id']
    else:
        session.flash = T('Ninguna Organización seleccionada')

    # if len(ids_to_accept) == 1:
    a_id = int(ids_to_accept)
    a_org = db(db.Organizacion.id == a_id).select().first()
    a_org.state_collaboration ='rejected'
    a_org.update_record()

    session.flash = T('Sugerencia Rechazada')
    redirect(URL('display_organizacion'))

    return dict()

################################################################################
################################################################################
# Funciones para administrar perfiles de empresas

@auth.requires(auth.has_membership(group_id = 'superadmin') or auth.has_membership(group_id = 'admin') or auth.has_membership(group_id = 'editor'))
def display_empresa():

    # Componente el cual muestra la grilla de empresas sugeridas

    label_dict_empresa = \
        {'tipoOrganizacion.name': T('Tipo Organización')}

    show_fields_empresa = [db.Organizacion.id,
                                db.Organizacion.tipoOrg,
                                # db.tipoOrganizacion.name,
                                db.Organizacion.hasSocialReason,
                                db.Organizacion.alias]

    db.Organizacion.tipoOrg.represent=lambda id,row: db.tipoOrganizacion(id).name

    query = (db.Organizacion.tipoOrg == 2) \
        & (db.Organizacion.state_collaboration == 'for_revision')

    empresa_grid = SQLFORM.grid(
        query,
        editable=True,
        details=False,
        user_signature=True,
        deletable=False,
        fields=show_fields_empresa,
        headers=label_dict_empresa,
        create=False,
        csv=False,
        paginate=10,
        searchable=False,
        links=[lambda row: A(T('Aceptar'), _class='w2p_trap button btn'
               , _href=URL('suggestion', 'accept_organizacion',
               vars=dict(id=row.id))), lambda row: A(T('Rechazar'),
               _class='w2p_trap button btn', _href=URL('suggestion',
               'reject_organizacion', vars=dict(id=row.id)))],
        links_in_grid=True,
        formname='empresa_grid_form',
        )

    if empresa_grid.element('.web2py_counter'):
        empresa_grid.element('.web2py_counter')[0] = ''

    if empresa_grid.element('.web2py_table input[type=submit]'):

        empresa_grid.element('.web2py_table input[type=submit]'
                                  )['_value'] = \
            T('Aceptar Empresas Seleccionadas')
    elif empresa_grid.element('.web2py_grid input[type=submit]'):
        empresa_grid.element('.web2py_grid input[type=submit]'
                                  )['_value'] = T('Aceptar')

    return dict(empresa_grid=empresa_grid)

################################################################################
################################################################################
# Funciones para administrar perfiles de casos

@auth.requires(auth.has_membership(group_id = 'superadmin') or auth.has_membership(group_id = 'admin') or auth.has_membership(group_id = 'editor'))
def display_caso():

    # Componente el cual muestra la grilla de casos sugeridos

    show_fields_caso = [db.caso.id,
                        db.caso.name,
                        db.caso.country,
                        db.caso.city]

    db.caso.created_by.readable=True

    caso_grid = SQLFORM.grid(  # selectable=lambda ids: redirect(URL('sugerencia',
                                  #         'accept_persona', vars=dict(id=ids))),
        db.caso.state_collaboration == 'for_revision',
        editable=True,
        details=False,
        deletable=False,
        user_signature=True,
        fields=show_fields_caso,
        create=False,
        csv=False,
        paginate=10,
        searchable=False,
        formname='persona_grid_form',
        links=[lambda row: A(T('Aceptar'), _class='w2p_trap button btn'
               , _href=URL('suggestion', 'accept_caso',
               vars=dict(id=row.id))), lambda row: A(T('Rechazar'),
               _class='w2p_trap button btn', _href=URL('suggestion',
               'reject_caso', vars=dict(id=row.id)))],
        )

    if caso_grid.element('.web2py_counter'):
        caso_grid.element('.web2py_counter')[0] = ''

    if caso_grid.element('.web2py_table input[type=submit]'):

        caso_grid.element('.web2py_table input[type=submit]'
                             )['_value'] = \
            T('Aceptar Casos Seleccionadas')

        caso_grid.element('.web2py_table input[type=submit]'
                             )['_class'] = 'buttontext button'
    elif caso_grid.element('.web2py_grid input[type=submit]'):

        caso_grid.element('.web2py_grid input[type=submit]')['_value'
                ] = T('Aceptar')

    return dict(caso_grid=caso_grid)

@auth.requires(auth.has_membership(group_id = 'superadmin') or auth.has_membership(group_id = 'admin') or auth.has_membership(group_id = 'editor'))
def accept_caso():

    # Funcion que pasa el estado de colaboracion de revision a aceptado
    # para las personas seleccionadas en la grilla

    if 'id' in request.vars:
        ids_to_accept = request.vars['id']
    else:
        session.flash = T('Ningún Caso seleccionado')

    # if len(ids_to_accept) == 1:
    a_id = int(ids_to_accept)
    a_caso = db(db.caso.id == a_id).select().first()
    a_caso.state_collaboration ='accepted'
    a_caso.update_record()

    session.flash = T('Sugerencia Aceptada')
    redirect(URL('display_caso'))

    return dict()

@auth.requires(auth.has_membership(group_id = 'superadmin') or auth.has_membership(group_id = 'admin') or auth.has_membership(group_id = 'editor'))
def reject_caso():

    # Funcion que pasa el estado de colaboracion de revision a aceptado
    # para las personas seleccionadas en la grilla

    if 'id' in request.vars:
        ids_to_accept = request.vars['id']
    else:
        session.flash = T('Ningún Caso seleccionado')

    a_id = int(ids_to_accept)
    a_caso = db(db.caso.id == a_id).select().first()
    a_caso.state_collaboration ='rejected'
    a_caso.update_record()

    session.flash = T('Sugerencia Rechazada')
    redirect(URL('display_caso'))

    return dict()

