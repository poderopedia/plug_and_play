#!/usr/bin/python
# -*- coding: utf-8 -*-

@auth.requires_login()
def index():
    pass

@auth.requires_login()
def quick_profile_persona():

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
        'depiction'
    ]

    # hidden_dict = dict(state_publication='draft',date_publication=request.now,
        # state_colaboration=False)

    a_form = SQLFORM(db.persona, labels=label_dict, fields=fields_dict)

    # a_form.vars['state_publication']='draft'
    # a_form.vars['date_publication']=request.now
    # a_form.vars['state_colaboration']=False

    if a_form.process().accepted:
        response.flash = 'Perfil sugerido con éxito'
        #redirect(URL('accepted'))
    elif a_form.errors:
        my_dict['a_error'] = 'Ooops! Ocurrió un error'
        response.flash = 'Hay errores en el formulario'

    my_dict['form']=a_form
    return my_dict



@auth.requires_login()
def long_profile_persona():
    pass



@auth.requires_login()
def quick_profile_organizacion():
    
    my_dict = dict()


    my_dict['a_error']=''

    label_dict = dict(tipoOrg= 'Tipo de Organización', haslogo= 'Logotipo',hasSocialReason= 'Razón Social',mainSector= 'Sector Principal',hasTaxId= 'RUT',alias= 'Nombre Corto',countryOfResidence= 'País de Residencia',depiction= 'Foto',hasDocumentation= 'Documento',documentSource= 'Fuentes',documentCloud= 'Fuentes Document Cloud',shortBio= 'Reseña')
    fields_dict = [
        'tipoOrg',
        'haslogo',
        'hasSocialReason',
        'Mainsector',
        'hasTaxId',
        'alias',
        'countryOfResidence',
        'depiction',
        'hasdocumentation',
        'documentSource',
        'documentCloud',
        'shortBio'
   ]

    # hidden_dict = dict(state_publication='draft',date_publication=request.now,
        # state_colaboration=False)


    #modificar Organizacion para que tambien tenga estado de publicacion
    a_form = SQLFORM(db.Organizacion, labels=label_dict, fields=fields_dict)

    # a_form.vars['state_publication']='draft'
    # a_form.vars['date_publication']=request.now
    # a_form.vars['state_colaboration']=False

    if a_form.process().accepted:
         response.flash = 'Organización Sugerida con éxito'
        #redirect(URL('accepted'))
    elif a_form.errors:
        my_dict['a_error'] = 'Ooops! Ocurrió un error'
        response.flash = 'Hay errores en el formulario'

    my_dict['form']=a_form
    return my_dict


@auth.requires_membership('colaboradores')
def long_profile_organizacion():
    pass
