# -*- coding: utf-8 -*-
### required - do no delete
def user(): return dict(form=auth())
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
