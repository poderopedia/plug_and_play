@auth.requires(auth.has_membership(group_id = ROLE_NAME_SUPER_ADMIN) or auth.has_membership(group_id = ROLE_NAME_ADMIN) or auth.has_membership(group_id = ROLE_NAME_EDITOR))
def index():
    redirect(URL('user_admin','list_users'))
    return locals()

@auth.requires(auth.has_membership(group_id = ROLE_NAME_SUPER_ADMIN) or auth.has_membership(group_id = ROLE_NAME_ADMIN) or auth.has_membership(group_id = ROLE_NAME_EDITOR))
def list_users():

    label_dict_user = {'auth_user.username':T('Nombre de Usuario'),'auth_user.first_name':T('Nombre'),'auth_user.last_name':T('Apellido'),'auth_group.role':T('Rol'),'auth_user.email':T('Email')}
   
    query = ( ((db.auth_user.id == db.auth_membership.user_id)) & ((db.auth_membership.group_id == db.auth_group.id)))

    fields_dict = [db.auth_user.username,
                   db.auth_user.first_name,
                   db.auth_user.last_name,
                   db.auth_group.role,
                   db.auth_user.email]

    grid = SQLFORM.grid(query,
    editable=False,
    details = True,
    deletable = True,
    user_signature = True,
    fields = fields_dict,
    create = True,
    headers = label_dict_user,
    csv = False,
    paginate = 10,
    searchable = True,
    links = [lambda row: A( SPAN(_class='icon pen icon-pencil'), SPAN(T('Editar'), _class='buttontext button',_title=T('Editar')),_class='w2p_trap button btn', _href=URL('manage_user',args=[row.auth_user.id]))]
    )
    

    return dict(table=grid)

@auth.requires(auth.has_membership(group_id = ROLE_NAME_SUPER_ADMIN) or auth.has_membership(group_id = ROLE_NAME_ADMIN) or auth.has_membership(group_id = ROLE_NAME_EDITOR))
def manage_user():
    db.auth_user.id.readable = False
    user_id = request.args(0) or redirect(URL('list_users'))
    
    label_dict_user = dict(username=T('Nombre de Usuario'),first_name=T('Nombre'),last_name=T('Apellido'),email=T('Email'))
    fields_dict = ['username',
                   'first_name',
                   'last_name',
                   'email']


    form = SQLFORM(db.auth_user, user_id,fields = fields_dict, labels = label_dict_user,submit_button = T('Enviar'))
    membership_panel = LOAD(request.controller,
                            'manage_membership.html',
                            args=[user_id],
                            ajax=True)
    form.add_button(T('Atrás'),URL('user_admin','list_users'))
    my_dict = dict(form=form,membership_panel=membership_panel)
    return my_dict 

@auth.requires(auth.has_membership(group_id = ROLE_NAME_SUPER_ADMIN) or auth.has_membership(group_id = ROLE_NAME_ADMIN) or auth.has_membership(group_id = ROLE_NAME_EDITOR))
def manage_membership():
    user_id = request.args(0) or redirect(URL('list_users'))


    db.auth_membership.user_id.default = int(user_id)
    db.auth_membership.user_id.writable = False

    #admin no puede agregar superadmins
    if auth.has_membership("admin"):
        db.auth_membership.group_id.requires = IS_IN_DB(db((db.auth_group.role == 'editor') | (db.auth_group.role == 'autor') | (db.auth_group.role == 'colaborador')),db.auth_group.id,'%(role)s')
        
    #editor no puede agregar ni admin ni superadmin
    if auth.has_membership("editor"):
        db.auth_membership.group_id.requires = IS_IN_DB(db((db.auth_group.role == 'autor') | (db.auth_group.role == 'colaborador')),db.auth_group.id,'%(role)s')
    
    form = SQLFORM.grid(db.auth_membership.user_id == user_id,
                        user_signature = False,
                        args=[user_id],
                        searchable=False,
                        deletable=False,
                        details=False,
                        selectable=False,
                        csv=False)
    return form
