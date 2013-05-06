def index():
    return locals()

@auth.requires(auth.has_membership(group_id = 'superadmin') or auth.has_membership(group_id = 'admin') or auth.has_membership(group_id = 'editor'))
def admin_collaboration():

    # Vista para mostrar el listado de personas y organizaciones sugeridas

    if len(request.args) == 0:
        redirect(URL('editor','admin_collaboration', args='persona'))


    return locals()

@auth.requires(auth.has_membership(group_id = 'superadmin') or auth.has_membership(group_id = 'admin') or auth.has_membership(group_id = 'editor'))
def display_persona():

    # Componente el cual muestra la grilla de personas sugeridas

    label_dict_persona = {'persona.ICN': T('Rut'),
                          'persona.firstLastName': T('Apellido Paterno'
                          ),
                          'persona.otherLastName': T('Apellido Materno'
                          )}

    db.persona.created_by.readable = True
    show_fields_persona = [ db.persona.ICN,
                           db.persona.firstName,
                           db.persona.firstLastName,
                           db.persona.created_by]

    db.persona.created_by.represent=lambda id,row: db.auth_user(id).username
    query = ((db.persona.state_collaboration == 'accepted') & (db.persona.state_publication == 'draft'))

    persona_grid = SQLFORM.grid(  # selectable=lambda ids: redirect(URL('sugerencia',
                                  #         'accept_persona', vars=dict(id=ids))),
        query,
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
               , _href=URL('editor', 'accept_persona',
               vars=dict(id=row.id))), lambda row: A(T('Rechazar'),
               _class='w2p_trap button btn', _href=URL('editor',
               'reject_persona', vars=dict(id=row.id))),
               lambda row: A(T('Programar'), **{'_href':'../load_display_persona#Lightbox_schedulepersona','_class':'w2p_trap button btn programar_persona','_data-toggle':'modal','_id':str(row.id)})]
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
        session.flash = T('Ni una Persona seleccionada')

    # if len(ids_to_accept) == 1:
    a_id = int(ids_to_accept)
    a_persona = db(db.persona.id == a_id).select().first()
    a_persona.state_publication ='published'
    a_persona.update_record()

    session.flash = T('Colaboración Publicada')
    redirect(URL('display_persona'))

    return dict()

@auth.requires(auth.has_membership(group_id = 'superadmin') or auth.has_membership(group_id = 'admin') or auth.has_membership(group_id = 'editor'))
def reject_persona():

    # Funcion que pasa el estado de colaboracion de revision a aceptado
    # para las personas seleccionadas en la grilla

    if 'id' in request.vars:
        ids_to_accept = request.vars['id']
    else:
        session.flash = T('Ni una Persona seleccionada')

    # if len(ids_to_accept) == 1:
    a_id = int(ids_to_accept)
    a_persona = db(db.persona.id == a_id).select().first()
    a_persona.state_collaboration ='rejected'
    a_persona.state_publication ='draft'
    a_persona.update_record()

    session.flash = T('Colaboración Rechazada')
    redirect(URL('display_persona'))

    return dict()

@auth.requires(auth.has_membership(group_id = 'superadmin') or auth.has_membership(group_id = 'admin') or auth.has_membership(group_id = 'editor'))
def schedule_persona():
    # Formulario de programacion para publicacion de personas
    my_dict = dict()
    my_dict['a_error'] = ''
    a_form = ''
    db.persona.id.readable = False
    db.persona.firstName.writable = False
    db.persona.firstLastName.writable  = False
    db.persona.otherLastName.writable  = False
    db.persona.date_publication.writable=True
    label_dict = dict(date_publication=T('Fecha de Publicación'))
    fields_dict = ['firstName','firstLastName','otherLastName','date_publication']

    a_form = SQLFORM(db.persona,request.args(0),labels =label_dict,fields = fields_dict,submit_button=T('Programar Publicación'),_id='schedule_form')
    a_form.vars.state_publication = 'programmed'
    a_form.vars.state_collaboration = 'accepted'
    if a_form.process().accepted:
        response.flash = T('Su publicación se hará pública en la fecha elegida')
        redirect('../admin_collaboration',client_side=True)
    elif a_form.errors:
        my_dict['a_error'] = T('Oops! ocurrió un error')
        response.flash = T('Hay errores en el formulario')
    my_dict['form'] = a_form
    return my_dict

@auth.requires(auth.has_membership(group_id = 'superadmin') or auth.has_membership(group_id = 'admin') or auth.has_membership(group_id = 'editor'))
def display_organizacion():

    # Componente el cual muestra la grilla de organizaciones sugeridas

    label_dict_organizacion = \
        {'tipoOrganizacion.name': T('Tipo Organización')}

    show_fields_organizacion = [db.Organizacion.tipoOrg,
                                # db.tipoOrganizacion.name,
                                db.Organizacion.hasSocialReason,
                                db.Organizacion.alias,
                                db.Organizacion.created_by]

    db.Organizacion.created_by.readable=True
    db.Organizacion.tipoOrg.represent=lambda id,row: db.tipoOrganizacion(id).name
    db.Organizacion.created_by.represent=lambda id,row: db.auth_user(id).username

    query = ((db.Organizacion.tipoOrg == db.tipoOrganizacion.id) \
        & (db.Organizacion.state_collaboration == 'accepted') & (db.Organizacion.state_publication == 'draft'))

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
               , _href=URL('editor', 'accept_organizacion',
               vars=dict(id=row.id))), lambda row: A(T('Rechazar'),
               _class='w2p_trap button btn', _href=URL('editor',
               'reject_organizacion', vars=dict(id=row.id))),
               lambda row: A(T('Programar'), **{'_href':'../load_display_organizacion#Lightbox_scheduleorganizacion','_class':'w2p_trap button btn programar_organizacion','_data-toggle':'modal','_id':str(row.id)})],
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
    a_org.state_publication ='published'
    a_org.state_collaboration ='accepted'
    a_org.update_record()

    session.flash = T('Colaboración Aceptada')
    redirect(URL('display_organizacion'))

    return dict()

@auth.requires(auth.has_membership(group_id = 'superadmin') or auth.has_membership(group_id = 'admin') or auth.has_membership(group_id = 'editor'))
def reject_organizacion():

    # Funcion que pasa el estado de colaboracion de revision a aceptado
    # para las organizaciones seleccionadas en la grilla

    if 'id' in request.vars:
        ids_to_accept = request.vars['id']
    else:
        session.flash = T('Ni una Organizacion seleccionada')

    # if len(ids_to_accept) == 1:
    a_id = int(ids_to_accept)
    a_org = db(db.Organizacion.id == a_id).select().first()
    a_org.state_collaboration ='rejected'
    a_org.state_publication ='draft'

    a_org.update_record()

    session.flash = T('Colaboración Rechazada')
    redirect(URL('display_organizacion'))

    return dict()

@auth.requires(auth.has_membership(group_id = 'superadmin') or auth.has_membership(group_id = 'admin') or auth.has_membership(group_id = 'editor'))
def schedule_organizacion():
    # Formulario de programacion de publicacion para organizaciones
    my_dict = dict()
    my_dict['a_error'] = ''
    a_form = ''
    db.Organizacion.id.readable = False
    db.Organizacion.hasSocialReason.writable = False
    db.Organizacion.date_publication.writable=True
    label_dict = dict(date_publication=T('Fecha de Publicación'))
    fields_dict = ['hasSocialReason','date_publication']

    a_form = SQLFORM(db.Organizacion,request.args(0),labels =label_dict,fields = fields_dict,submit_button=T('Programar Publicación'),_id='schedule_form')
    a_form.vars.state_publication = 'programmed'
    a_form.vars.state_collaboration = 'accepted'
    if a_form.process().accepted:
        response.flash = T('Su publicación se hará pública en la fecha elegida')
        redirect('../admin_collaboration/organizacion',client_side=True)
    elif a_form.errors:
        my_dict['a_error'] = T('Oops! ocurrió un error')
        response.flash = T('Hay errores en el formulario')
    my_dict['form'] = a_form
    return my_dict

@auth.requires(auth.has_membership(group_id = 'superadmin') or auth.has_membership(group_id = 'admin') or auth.has_membership(group_id = 'editor'))
def display_empresa():

    label_dict_empresa = \
        {'tipoOrganizacion.name': T('Tipo Organización')}



    # Componente el cual muestra la grilla de empresas sugeridas

    show_fields_empresa = [db.Organizacion.tipoOrg,
                                # db.tipoOrganizacion.name,
                                db.Organizacion.hasSocialReason,
                                db.Organizacion.alias,
                                db.Organizacion.created_by]

    db.Organizacion.created_by.readable=True
    db.Organizacion.tipoOrg.represent=lambda id,row: db.tipoOrganizacion(id).name
    db.Organizacion.created_by.represent=lambda id,row: db.auth_user(id).username

    query = ((db.Organizacion.tipoOrg == 2) \
        & (db.Organizacion.state_collaboration == 'accepted') & (db.Organizacion.state_publication == 'draft'))

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
               , _href=URL('editor', 'accept_organizacion',
               vars=dict(id=row.id))), lambda row: A(T('Rechazar'),
               _class='w2p_trap button btn', _href=URL('editor',
               'reject_organizacion', vars=dict(id=row.id))),
               lambda row: A(T('Programar'), **{'_href':'../load_display_empresa#Lightbox_scheduleempresa#Lightbox_scheduleempresa','_class':'w2p_trap button btn programar_empresa','_data-toggle':'modal','_id':str(row.id)})],
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

@auth.requires(auth.has_membership(group_id = 'superadmin') or auth.has_membership(group_id = 'admin') or auth.has_membership(group_id = 'editor'))
def schedule_empresa():
    # Formulario de programacion de publicacion para empresas
    my_dict = dict()
    my_dict['a_error'] = ''
    a_form = ''
    db.Organizacion.id.readable=False
    db.Organizacion.hasSocialReason.writable=False
    db.Organizacion.date_publication.writable=True
    label_dict = dict(date_publication=T('Fecha de Publicación'))
    fields_dict = ['hasSocialReason','date_publication']

    a_form = SQLFORM(db.Organizacion,request.args(0),labels =label_dict,fields = fields_dict,submit_button=T('Programar Publicación'),_id='schedule_form')
    a_form.vars.state_publication = 'programmed'
    a_form.vars.state_collaboration = 'accepted'
    if a_form.process().accepted:
        response.flash = T('Su publicación se hará pública en la fecha elegida')
        redirect('../admin_collaboration/empresa',client_side=True)
    elif a_form.errors:
        my_dict['a_error'] = T('Oops! ocurrió un error')
        response.flash = T('Hay errores en el formulario')
    my_dict['form'] = a_form
    return my_dict



@auth.requires(auth.has_membership(group_id = 'superadmin') or auth.has_membership(group_id = 'admin') or auth.has_membership(group_id = 'editor'))
def display_caso():

    label_dict_empresa = \
        {'tipoOrganizacion.name': T('Tipo Organización')}



    # Componente el cual muestra la grilla de empresas sugeridas

    show_fields_caso = [db.caso.id,
                                db.caso.name,
                                db.caso.country,
                                db.caso.city]

    # db.Organizacion.tipoOrg.represent=lambda id,row: db.tipoOrganizacion(id).name

    query = ((db.caso.state_collaboration == 'accepted') & (db.caso.state_publication == 'draft'))

    caso_grid = SQLFORM.grid(
        query,
        editable=True,
        details=False,
        user_signature=True,
        deletable=False,
        fields=show_fields_caso,
        # headers=label_dict_empresa,
        create=False,
        csv=False,
        paginate=10,
        searchable=False,
        links=[lambda row: A(T('Aceptar'), _class='w2p_trap button btn'
               , _href=URL('editor', 'accept_caso',
               vars=dict(id=row.id))), lambda row: A(T('Rechazar'),
               _class='w2p_trap button btn', _href=URL('editor',
               'reject_caso', vars=dict(id=row.id))),
               lambda row: A(T('Programar'), **{'_href':'../load_display_caso#Lightbox_schedulecaso#Lightbox_schedulecaso','_class':'w2p_trap button btn programar_caso','_data-toggle':'modal','_id':str(row.id)})],
        links_in_grid=True,
        formname='caso_grid_form',
        )

    if caso_grid.element('.web2py_counter'):
        caso_grid.element('.web2py_counter')[0] = ''

    if caso_grid.element('.web2py_table input[type=submit]'):

        caso_grid.element('.web2py_table input[type=submit]'
                                  )['_value'] = \
            T('Aceptar Empresas Seleccionadas')
    elif caso_grid.element('.web2py_grid input[type=submit]'):
        caso_grid.element('.web2py_grid input[type=submit]'
                                  )['_value'] = T('Aceptar')

    return dict(caso_grid=caso_grid)

@auth.requires(auth.has_membership(group_id = 'superadmin') or auth.has_membership(group_id = 'admin') or auth.has_membership(group_id = 'editor'))
def schedule_caso():
    # Formulario de programacion de publicacion para casos
    my_dict = dict()
    my_dict['a_error'] = ''
    a_form = ''
    db.caso.id.readable = False
    db.caso.name.writable= False
    db.caso.date_publication.writable=True
    label_dict = dict(date_publication=T('Fecha de Publicación'))
    fields_dict = ['name','date_publication']

    a_form = SQLFORM(db.caso,request.args(0),labels =label_dict,fields = fields_dict,submit_button=T('Programar Publicación'),_id='schedule_form')
    a_form.vars.state_publication = 'programmed'
    a_form.vars.state_collaboration = 'accepted'
    if a_form.process().accepted:
        response.flash = T('Su publicación se hará pública en la fecha elegida')
        redirect('../admin_collaboration/caso',client_side=True)
    elif a_form.errors:
        my_dict['a_error'] = T('Oops! ocurrió un error')
        response.flash = T('Hay errores en el formulario')
    my_dict['form'] = a_form
    return my_dict


#funcion auxiliar usada para mostrar el ajax sin que se recargue la pagina completa dentro del div
@auth.requires(auth.has_membership(group_id = 'superadmin') or auth.has_membership(group_id = 'admin') or auth.has_membership(group_id = 'editor'))
def load_display_persona():
    return locals()

#funcion auxiliar usada para mostrar el ajax sin que se recargue la pagina completa dentro del div
@auth.requires(auth.has_membership(group_id = 'superadmin') or auth.has_membership(group_id = 'admin') or auth.has_membership(group_id = 'editor'))
def load_display_organizacion():
    return locals()

#funcion auxiliar usada para mostrar el ajax sin que se recargue la pagina completa dentro del div
@auth.requires(auth.has_membership(group_id = 'superadmin') or auth.has_membership(group_id = 'admin') or auth.has_membership(group_id = 'editor'))
def load_display_empresa():
    return locals()

#funcion auxiliar usada para mostrar el ajax sin que se recargue la pagina completa dentro del div
@auth.requires(auth.has_membership(group_id = 'superadmin') or auth.has_membership(group_id = 'admin') or auth.has_membership(group_id = 'editor'))
def load_display_caso():
    return locals()
