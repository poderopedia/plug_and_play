#!/usr/bin/python
# -*- coding: utf-8 -*-

@auth.requires_login()
def index():
    return locals()

@auth.requires_login()
def quick_profile_persona():

    my_dict = dict()

    db.persona.state_collaboration.default = 'accepted';

    my_dict['a_error']=''

    label_dict = dict(ICN='Rut', firstLastName='Apellido Paterno',
                      otherLastName='Apellido Materno')
    fields_dict = [
        'ICN',
        'firstName',
        'firstLastName',
        'otherLastName',
        'alias',
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
    db.persona.state_collaboration.default = 'accepted';

    # STEPS: A dict with fields for each step
    mysteps = [dict(title='Datos Básicos',fields=['firstName','firstLastName', 'otherLastName','alias','shortBio','countryofResidence', 'depiction']),
               dict(title='Más Información',fields=['Mainsector','birth','isDead','countryofBirth','city','shortBio']),
               dict(title='Redes Sociales',fields=['web','twitterNick','facebookNick','linkedinNick']),
               dict(title='Perfil Largo',fields=['longBio'])]
    # IMPORT: Import the module
    from plugin_PowerFormWizard import PowerFormWizard
    # CREATE: Create the form object just like the SQLFORM
    form = PowerFormWizard(db.persona, steps=mysteps, options=dict(validate=True))
    if(request.args(0)):
        record=db.persona(request.args(0))
        mysteps = [dict(title='Datos Básicos',fields=['firstName','firstLastName', 'otherLastName','alias','shortBio','countryofResidence', 'depiction']),
                   dict(title='Más Información',fields=['Mainsector','birth','isDead','countryofBirth','city','shortBio']),
                   dict(title='Redes Sociales',fields=['web','twitterNick','facebookNick','linkedinNick']),
                   dict(title='Perfil Largo',fields=['longBio'])
              ]
   
        form = PowerFormWizard(db.persona, steps=mysteps, options=dict(validate=True), record=record)

    
    # VALIDATE: web2py form validation
    if form.accepts(request.vars, session):
        response.flash = "Persona sugerida con éxito"
    elif form.errors:
        form.step_validation() # VERY IMPORTANT FOR VALIDATION!!!!
        response.flash = "Hay errores en el formulario"

    # Enjoy!
    return dict(form=form)



@auth.requires_login()
def quick_profile_organizacion():
    
    db.Organizacion.state_collaboration.default = 'accepted';
    my_dict = dict()


    my_dict['a_error']=''

    label_dict = dict(tipoOrg='Tipo de Organización', hasSocialReason= 'Nombre Legal(Razón Social)',alias= 'Nombre Corto',countryOfResidence= 'País',haslogo= 'Logotipo',shortBio= 'Reseña')
    fields_dict = [
        'tipoOrg',
        'haslogo',
        'hasSocialReason',
        'hasTaxId',
        'alias',
        'countryOfResidence',
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

@auth.requires_login()
def long_profile_organizacion():
    db.Organizacion.state_collaboration.default = 'accepted';

    # STEPS: A dict with fields for each step
    mysteps = [dict(title='Datos Básicos',fields=['tipoOrg', 'hasSocialReason','alias','hasTaxId','haslogo','Mainsector','countryOfResidence', 'depiction','shortBio']),
               dict(title='Fuentes',fields=['hasdocumentation','documentSource','documentCloud']),
               dict(title='Reseña',fields=['longBio','birth','is_active'])
              ]
    # IMPORT: Import the module
    from plugin_PowerFormWizard import PowerFormWizard
    # CREATE: Create the form object just like the SQLFORM
    form = PowerFormWizard(db.Organizacion, steps=mysteps, options=dict(validate=True))
    if(request.args(0)):
        record=db.Organizacion(request.args(0))
        mysteps = [dict(title='Datos Básicos',fields=['tipoOrg', 'hasSocialReason','alias','hasTaxId','haslogo','Mainsector','countryOfResidence', 'depiction','shortBio']),
                   dict(title='Fuentes',fields=['hasdocumentation','documentSource','documentCloud']),
                   dict(title='Reseña',fields=['longBio','birth','is_active'])
                  ]
        form = PowerFormWizard(db.Organizacion, steps=mysteps, options=dict(validate=True), record=record)


    # VALIDATE: web2py form validation
    if form.accepts(request.vars, session):
        response.flash = "Organización sugerida con éxito"
    elif form.errors:
        form.step_validation() # VERY IMPORTANT FOR VALIDATION!!!!
        response.flash = "Hay errores en el formulario"

    # Enjoy!
    return dict(form=form)



