#Módulo de configuación inicial.


#!/usr/bin/env python
# coding: utf8
from gluon import *

def agregar_rol_autor():
    id = None
    rol_autor = db(db.auth_group.role=='autor').select().first()
    if not rol_autor:
        id = db.auth_group.insert(role='autor',description='Este tipo de usuario  es el que crea colaboraciones. Requiere invitación.')
    return id

def agregar_rol_colaborador():
    id = None
    rol_autor = db(db.auth_group.role=='colaborador').select().first()
    if not rol_autor:
        id = db.auth_group.insert(role='colaborador',description='Este tipo de usuario  es el que crea colaboraciones. No requiere invitación.')
        auth = Auth(db)        
        auth.settings.everybody_group_id = id #todo usuario nuevo tiene grupo colaborador
    return id

def agregar_rol_editor():
    id = None
    rol_autor = db(db.auth_group.role=='editor').select().first()
    if not rol_autor:
        id = db.auth_group.insert(role='editor',description='Este tipo de usuario  es el que valida las colaboraciones.')
    return id
    
#agregar_rol_autor()
#agregar_rol_colaborador()
#agregar_rol_editor()
