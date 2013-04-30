@auth.requires(auth.has_membership(group_id = 'superadmin') or auth.has_membership(group_id = 'admin') or auth.has_membership(group_id = 'editor'))
def index():
    redirect(URL('user_admin','list_users'))
    return locals()

@auth.requires(auth.has_membership(group_id = 'superadmin') or auth.has_membership(group_id = 'admin') or auth.has_membership(group_id = 'editor'))
def list_users():
    btn = lambda row: A("Edit", _href=URL('manage_user', args=row.auth_user.id))
    db.auth_user.edit = Field.Virtual(btn)
    rows = db(db.auth_user).select()
    headers = ["ID", "Name", "Last Name", "Email", "Edit"]
    fields = ['id', 'first_name', 'last_name', "email","edit"]
    table = TABLE(THEAD(TR(*[B(header) for header in headers])),
        TBODY(*[TR(*[TD(row[field]) for field in fields]) \
                    for row in rows]))
    table["_class"] = "table table-striped table-bordered table-condensed"

    return dict(table=table)

@auth.requires(auth.has_membership(group_id = 'superadmin') or auth.has_membership(group_id = 'admin') or auth.has_membership(group_id = 'editor'))
def manage_user():
    user_id = request.args(0) or redirect(URL('list_users'))
    form = SQLFORM(db.auth_user, user_id)
    membership_panel = LOAD(request.controller,
                            'manage_membership.html',
                            args=[user_id],
                            ajax=True)
    return dict(form=form,membership_panel=membership_panel)

@auth.requires(auth.has_membership(group_id = 'superadmin') or auth.has_membership(group_id = 'admin') or auth.has_membership(group_id = 'editor'))
def manage_membership():
    user_id = request.args(0) or redirect(URL('list_users'))
    db.auth_membership.user_id.default = int(user_id)
    db.auth_membership.user_id.writable = False
    
    #admin no puede agregar superadmins
    if auth.has_membership("admin"):
        db.auth_membership.group_id.requires = IS_IN_DB(db, db.auth_group.id > 2 ,'%(group_id)s')
        
    #editor no puede agregar ni admin ni superadmin
    if auth.has_membership("editor"):
        db.auth_membership.group_id.requires = IS_IN_DB(db, db.auth_group.id > 3,'%(group_id)s')
    

    form = SQLFORM.grid(db.auth_membership.user_id == user_id,
                        user_signature = False,
                        args=[user_id],
                        searchable=False,
                        deletable=False,
                        details=False,
                        selectable=False,
                        csv=False)
    return form
