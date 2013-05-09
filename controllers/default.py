# -*- coding: utf-8 -*-
### required - do no delete
def user(): 

    groupadd( ROLE_NAME_SUPER_ADMIN, ROLE_DESCR_SUPER_ADMIN)
    groupadd( ROLE_NAME_ADMIN, ROLE_DESCR_ADMIN)
    groupadd( ROLE_NAME_EDITOR, ROLE_DESCR_EDITOR)
    groupadd( ROLE_NAME_AUTOR, ROLE_DESCR_AUTOR)
    groupadd( ROLE_NAME_COLLABORATOR, ROLE_DESCR_COLLABORATOR)
    if request.args(0) == 'register':
        auth.settings.create_user_groups = False
        auth.settings.register_onaccept=[lambda form:
        auth.add_membership(auth.id_group(ROLE_NAME_COLLABORATOR),form.vars.id)]
    return dict(form=auth())

def download(): return response.download(request,db)
def call(): return service()
### end requires
def index():
    if( auth.user is not None ):
        redirect(URL('inicio'))
    else:
        redirect(URL('user'))
    return dict()

def error():
    return dict()

def inicio():
    return dict()

def groupadd(check_group, description):
    if not db(db.auth_group.role==check_group).count():
     db.auth_group.insert(role=check_group,description = description)

