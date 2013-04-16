#!/usr/bin/python
# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

T.force('es')

if not request.env.web2py_runtime_gae:

    # # if NOT running on Google App Engine use SQLite or other DB

    db = DAL(settings.database_uri, check_reserved=['postgres', 'mysql'
             ], migrate_enabled=True, migrate=True)
else:

    # # connect to Google BigTable (optional 'google:datastore://namespace')

    db = DAL('google:datastore')

    # # store sessions and tickets there

    session.connect(request, response, db=db)

    # # or store session in Memcache, Redis, etc.
    # # from gluon.contrib.memdb import MEMDB
    # # from google.appengine.api.memcache import Client
    # # session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'

response.generic_patterns = (['*'] if request.is_local else [])

## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db, hmac_key=Auth.get_or_create_key())
(crud, service, plugins) = (Crud(db), Service(), PluginManager())

## create all tables needed by auth if not custom tables

########################################

db.define_table(
    'auth_user',
    Field('username', type='string', label=T('Username')),
    Field('first_name', type='string', label=T('First Name')),
    Field('last_name', type='string', label=T('Last Name')),
    Field('email', type='string', label=T('Email')),
    Field('password', type='password', readable=False,
          label=T('Password')),
    Field(
        'created_on',
        'datetime',
        default=request.now,
        label=T('Created On'),
        writable=False,
        readable=False,
        ),
    Field(
        'modified_on',
        'datetime',
        default=request.now,
        label=T('Modified On'),
        writable=False,
        readable=False,
        update=request.now,
        ),
    Field('registration_key', default='', writable=False,
          readable=False),
    Field('reset_password_key', default='', writable=False,
          readable=False),
    Field('registration_id', default='', writable=False,
          readable=False),
    format='%(username)s',
    )

db.auth_user.first_name.requires = \
    IS_NOT_EMPTY(error_message=auth.messages.is_empty)
db.auth_user.last_name.requires = \
    IS_NOT_EMPTY(error_message=auth.messages.is_empty)
db.auth_user.password.requires = CRYPT(key=auth.settings.hmac_key)
db.auth_user.username.requires = IS_NOT_IN_DB(db, db.auth_user.username)
db.auth_user.email.requires = \
    (IS_EMAIL(error_message=auth.messages.invalid_email),
     IS_NOT_IN_DB(db, db.auth_user.email))
auth.define_tables(migrate=True)

## configure email

mail = auth.settings.mailer

## configure auth policy

auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
##from gluon.contrib.login_methods.rpx_account import use_janrain
##use_janrain(auth,filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

mail.settings.server = settings.email_server
mail.settings.sender = settings.email_sender
mail.settings.login = settings.email_login

db.rdf_namespaces = \
    {'_xmlns:rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
     '_xmlns:relational': 'http://www.dbs.cs.uni-duesseldorf.de/RDF/relational.owl#',
     '_xmlns:rdfs': 'http://www.w3.org/2000/01/rdf-schema#'}


def select_datewidget(field, value):
    MINYEAR = 1900
    MAXYEAR = 2040
    import datetime
    now = datetime.date.today()
    dtval = value or now.isoformat()
    (year, month, day) = str(dtval).split('-')
    dt = SQLFORM.widgets.string.widget(field, value)
    id = dt['_id']
    dayid = id + '__day'
    monthid = id + '__month'
    yearid = id + '__year'
    wrapperid = id + '__wrapper'
    wrapper = DIV(_id=wrapperid)
    day = SELECT([OPTION(str(i).zfill(2)) for i in range(1, 32)],
                 value=day, _id=dayid)
    month = SELECT([OPTION(datetime.date(2008, i, 1).strftime('%B'),
                   _value=str(i).zfill(2)) for i in range(1, 13)],
                   value=month, _id=monthid)
    year = SELECT([OPTION(i) for i in range(MINYEAR, MAXYEAR)],
                  value=year, _id=yearid)
    jqscr = \
        SCRIPT("""
      jQuery('#%s').hide();
      var curval = jQuery('#%s').val();
      if(curval) {
        var pieces = curval.split('-');
        jQuery('#%s').val(pieces[0]);
        jQuery('#%s').val(pieces[1]);
        jQuery('#%s').val(pieces[2]);
      }
      jQuery('#%s select').change(function(e) {
        jQuery('#%s').val(
           jQuery('#%s').val()+'-'+jQuery('#%s').val()+'-'+jQuery('#%s').val());
      });
    """
               % (
        id,
        id,
        yearid,
        monthid,
        dayid,
        wrapperid,
        id,
        yearid,
        monthid,
        dayid,
        ))
    wrapper.components.extend([day, month, year, dt, jqscr])
    return wrapper


# a table to store mapas

db.define_table('mapas', Field('label', 'text',
                requires=IS_NOT_EMPTY(), label='Nombre?'),
                Field('posted_on', 'datetime', readable=False,
                writable=False), Field('graph', 'text', readable=False,
                writable=False), auth.signature)

# a table to store casos

db.define_table('casos', Field('label', 'string',
                requires=IS_NOT_EMPTY(), label='Nombre'),
                Field('posted_on', 'datetime', readable=False,
                writable=False), Field('graph', 'text', readable=False,
                writable=False), auth.signature)

# a table for Country

db.define_table('country', Field('name', 'string', required=True),
                Field('iso2', 'string', required=True), Field('iso3',
                'string', required=True), Field('iso_id', 'integer',
                required=False))

db.country.rdf = {'type': 'poder:Country',
                  'namespaces': {'_xmlns:foaf': 'http://xmlns.com/foaf/0.1/',
                  '_xmlns:poder': 'http://poderopedia.com/vocab/'},
                  'references': {'persona': 'countryOfResidence'}}

db.country.name.rdf = 'poder:'

# a table for place

db.define_table('place', Field('lugar', 'string', requires=True),
                Field('fecha', 'date', requires=IS_DATE(),
                required=True), Field('country', db.country,
                label='País', requires=False))

# a teble for sector

db.define_table('sector', Field('parent', 'integer', required=True,
                default=0), Field('name', 'string', required=True),
                Field('labelOtro', 'string', readable=False,
                writable=False))

# from plugin_anytime_widget import anytime_widget, anydate_widget, \
 #   anydatetime_widget

# a table document

db.define_table(
    'document',
    Field('name', 'string', label=T('Descripción')),
    Field('documentURL', 'string', requires=IS_URL(), label=T('URL'),
          required=True),
    Field('fecha', 'string', label=T('Fecha Documento')),
    Field('tipoDoc', 'string', required=False, readable=False,
          writable=False),
    Field(
        'source_from',
        db.auth_user,
        readable=True,
        writable=False,
        required=True,
        default=auth.user_id,
        ),
    auth.signature,
    format='%(name)s',
    )
requiere = db(db.document.is_active == True)

# a table to store personas

db.define_table(  # #Field('birth', db.birthEvent, label='Fecha de Nacimiento', required=False),
                  # #Field('depiction',db.document, label=T('Foto')),
                  # #Field('hasAlternativeMainSector','string',readable=False, writable=False, label=T('Sector Principal Alternativo')),
                  # #Field('hasAlternativeOtherSector','string',readable=False, writable=False, label=T('Otro Sector Alternativo')),
                  # # state_publication indica el estado de la publicacion. Esta puede estar programada para una fecha, publicada o ser un borrador.
                  # # date_publication indica la fecha de publicacion
                  # #Field('hasdocumentation',db.document, label=T('Documento')),
                  # #Field('hasdocumentation','upload', label=T('Documento')),
                  # #Field('hasUrl',db.document, label=T('Redes Sociales')),
    'persona',
    Field('ICN', 'string', label=T('rut'), required=False),
    Field('firstName', 'string', readable=True, writable=True,
          label=T('Nombres')),
    Field('firstLastName', 'string', requires=IS_NOT_EMPTY(),
          label=T('Apellido Paterno')),
    Field('otherLastName', 'string', readable=True, writable=True,
          label=T('Apellido Materno')),
    Field(
        'alias',
        'string',
        requires=IS_NOT_EMPTY(),
        readable=True,
        writable=True,
        label=T('Nombre Corto'),
        ),
    Field('birth', 'string', label='Fecha de Nacimiento',
          required=False),
    Field('countryofResidence', db.country, label='País de Residencia',
          requires=IS_IN_DB(db, 'country.id', 'country.name')),
    Field('countryofBirth', db.country, label='País de Nacimiento',
          requires=IS_EMPTY_OR(IS_IN_DB(db, 'country.id', 'country.name'
          )), required=False),
    Field('city', 'string', readable=True, writable=True,
          label=T('Ciudad')),
    Field('Mainsector', 'list:reference sector', label=T('Main Sector'
          ), requires=IS_IN_DB(db, 'sector.id', 'db.sector.name',
          multiple=True)),
    Field('depiction', 'upload', label=T('Foto'), required=False),
    Field('shortBio', 'text', label=T('Reseña')),
    Field('longBio', 'text', requires=IS_LENGTH(65536),
          label=T('Perfil largo')),
    Field('documentSource', 'list:reference document', required=False,
          requires=IS_IN_DB(requiere, 'document.id', '%(name)s',
          multiple=True), label=T('Fuentes')),
    Field('documentCloud', 'list:reference documentCloud',
          required=False, requires=IS_IN_DB(db, 'documentCloud.id',
          '%(title)s', multiple=True), label=T('Fuentes Document Cloud'
          )),
    Field('isDead', 'boolean', label=T('Ha Fallecido')),
    Field('web', 'string', label=T('Web')),
    Field('twitterNick', 'string', label=T('Twitter')),
    Field('facebookNick', 'string', label=T('Facebook')),
    Field('linkedinNick', 'string', label=T('Linkedin')),
    Field(
        'state_publication',
        'string',
        label=T('Estado Publicacion'),
        readable=True,
        writable=False,
        requires=IS_IN_SET(('programmed', 'published', 'draft')),
        default='draft',
        ),
    Field(
        'date_publication',
        'date',
        label=T('Fecha Publicacion'),
        readable=True,
        writable=False,
        default=request.now,
        ),
    Field(
        'state_collaboration',
        'string',
        label=T('Estado Colaboracion'),
        readable=True,
        writable=False,
        requires=IS_IN_SET(('accepted', 'rejected', 'for_revision')),
        default='for_revision',
        ),
    auth.signature,
    )

    # migrate='persona.table'

db.persona.firstName.rdf = 'foaf:firstName'
db.persona.firstLastName.rdf = 'poder:firstLastName'
db.persona.otherLastName.rdf = 'poder:otherLastName'
db.persona.alias.rdf = 'poder:alias'

##db.persona.countryofResidence.rdf= {
##    'name':'poder:countryOfResidence',
##   '_rdf:resource':'$VALUE'
##}

##TODO resolve anti-simetric connections

db.persona.rdf = {'type': 'foaf:Person',
                  'namespaces': {'_xmlns:foaf': 'http://xmlns.com/foaf/0.1/',
                  '_xmlns:poder': 'http://poderopedia.com/vocab/'}}

# a table to store perfiles

db.define_table(
    'perfiles',
    Field('label', 'string', requires=IS_NOT_EMPTY(), label='Nombre?'),
    Field('postedon', 'datetime', readable=False, writable=False),
    Field('dueno', 'reference auth_user', readable=False,
          writable=False),
    Field('graph', 'text', readable=False, writable=False),
    Field('person', 'reference persona', readable=False,
          writable=False),
    )

# a table for sectorMain2Pers

db.define_table('sectorMain2Pers', Field('origenP', db.persona),
                Field('destinoSector', db.sector))

# table for tipoParentesco

db.define_table('tipoParentesco', Field('name', 'string',
                required=True, label=T('Parentesco')),
                Field('nameInverso', 'string', required=False),
                Field('description', 'text', required=False))

# table for tipoRelacionP2P

db.define_table('tipoRelacionP2P', Field('parent', 'integer',
                required=True, default=0), Field('name', 'string',
                required=True), Field('description', 'text',
                required=False))

# table for tipoOrganizacion

db.define_table('tipoOrganizacion', Field('name', 'string',
                required=True, label=T('Nombre')),
                Field('generalizacion', 'integer'))

# table for Organización

db.define_table(
    'Organizacion',
    Field(
        'name',
        'string',
        required=False,
        label=T('Nombre'),
        writable=False,
        readable=False,
        ),
    Field('tipoOrg', db.tipoOrganizacion, requires=IS_IN_DB(db,
          'tipoOrganizacion.id', 'tipoOrganizacion.name'),
          label=T('Tipo Organizacion'), default=12),
    Field('haslogo', 'upload', uploadfield=True, label=T('Logo')),
    Field('hasSocialReason', 'string', label=T('Razón Social')),
    Field('Mainsector', 'list:reference sector', label=T('Main Sector'
          ), requires=IS_IN_DB(db, 'sector.id', 'db.sector.name',
          multiple=True)),
    Field('hasTaxId', 'string', label=T('RUT')),
    Field('alias', 'string', label=T('Nombre Fantasía'), required=True,
          requires=IS_NOT_EMPTY(T('Ingresar nombre'))),
    Field('countryOfResidence', db.country, requires=IS_IN_DB(db,
          'country.id', 'country.name', T('Seleccionar Pais')),
          label='País de Residencia'),
    Field('depiction', 'upload', label='Foto'),
    Field('hasdocumentation', 'upload', label='Documento'),
    Field('documentSource', 'list:reference document', required=False,
          requires=IS_IN_DB(requiere, 'document.id', '%(name)s',
          multiple=True), label=T('Fuentes')),
    Field('documentCloud', 'list:reference documentCloud',
          required=False, requires=IS_IN_DB(db, 'documentCloud.id',
          '%(title)s', multiple=True), label=T('Fuentes Document Cloud'
          )),
    Field('shortBio', 'text', label='Reseña'),
    Field('longBio', 'text', requires=IS_LENGTH(65536),
          label='Perfil largo'),
    Field('birth', 'string', label='Fecha de Fundación'),
    Field(
        'state_publication',
        'string',
        label=T('Estado Publicacion'),
        readable=True,
        writable=False,
        requires=IS_IN_SET(('programmed', 'published', 'draft')),
        default='draft',
        ),
    Field(
        'date_publication',
        'date',
        label=T('Fecha Publicacion'),
        readable=True,
        writable=False,
        default=request.now,
        ),
    Field(
        'state_collaboration',
        'string',
        label=T('Estado Colaboracion'),
        readable=True,
        writable=False,
        requires=IS_IN_SET(('accepted', 'rejected', 'for_revision')),
        default='for_revision',
        ),
    auth.signature,
    )

# table for RelPersona

db.define_table(
    'relPersona',
    Field('relacion', db.tipoRelacionP2P, required=True,
          requires=IS_IN_DB(db, 'tipoRelacionP2P.id',
          'tipoRelacionP2P.name')),
    Field('origenP', db.persona, requires=IS_IN_DB(db, 'persona.id',
          'persona.alias')),
    Field('destinoP', db.persona,
          widget=SQLFORM.widgets.autocomplete(request,
          db.persona.alias, id_field=db.persona.id,
          keyword='_autocomplete_destinoP_%(fieldname)s',
          db=db(db.persona.is_active == True))),
    Field('extraO', db.Organizacion,
          widget=SQLFORM.widgets.autocomplete(request,
          db.Organizacion.alias, id_field=db.Organizacion.id,
          db=db(db.Organizacion.is_active == True)), requires=False,
          label=T('Organizacion/Empresa')),
    Field('extraLabel', 'string', required=False, label=T('Sub Grupo'
          )),
    Field('fdesde', 'string', required=False, label=T('Desde')),
    Field('fhasta', 'string', required=False, label=T('Hasta')),
    Field('isPast', 'boolean', required=False, label=T('es pasado')),
    Field('documentSource', 'list:reference document', required=False,
          requires=IS_IN_DB(requiere, 'document.id', '%(name)s',
          multiple=True), label=T('Fuentes')),
    Field('ini', 'date', readable=False, writable=False),
    Field('fin', 'date', readable=False, writable=False),
    Field(
        'iniDay',
        'string',
        requires=IS_IN_SET(day_list, zero=T('Sin Fecha')),
        default='Sin Fecha',
        writable=True,
        readable=True,
        ),
    Field(
        'iniMonth',
        'string',
        requires=IS_IN_SET(month_list, zero=T('Sin Fecha')),
        default='Sin Fecha',
        writable=True,
        readable=True,
        ),
    Field(
        'iniYear',
        'string',
        requires=IS_IN_SET(year_list, zero=T('Sin Fecha')),
        default='Sin Fecha',
        writable=True,
        readable=True,
        ),
    Field(
        'finDay',
        'string',
        requires=IS_IN_SET(day_list, zero=T('Sin Fecha')),
        default='Sin Fecha',
        writable=True,
        readable=True,
        ),
    Field(
        'finMonth',
        'string',
        requires=IS_IN_SET(month_list, zero=T('Sin Fecha')),
        default='Sin Fecha',
        writable=True,
        readable=True,
        ),
    Field(
        'finYear',
        'string',
        requires=IS_IN_SET(year_list, zero=T('Sin Fecha')),
        default='Sin Fecha',
        writable=True,
        readable=True,
        ),
    auth.signature,
    )

# table type of relation Org2Org

db.define_table('tipoRelacionOrg2Org', Field('parent', 'integer',
                label='Padre', required=True, default=0), Field('name',
                'string', label='Nombre', required=True),
                Field('inverse', 'string'))

# table relation Organization to Organization

db.define_table(
    'relOrg2Org',
    Field('origenO', db.Organizacion, label='Origen', required=True,
          requires=IS_IN_DB(db, 'Organizacion.id',
          'db.Organizacion.alias')),
    Field('relationOrg', db.tipoRelacionOrg2Org, required=True),
    Field('destinoO', db.Organizacion, label='Destino', required=True),
    Field('extraLabel', 'string', required=False, label=T('Sub Grupo'
          )),
    Field('fdesde', 'string', required=False, notnull=False,
          label=T('Desde')),
    Field('fhasta', 'string', required=False, notnull=False,
          label=T('Hasta')),
    Field('isPast', 'boolean', label='es pasado'),
    Field('documentSource', 'list:reference document', required=False,
          requires=IS_IN_DB(requiere, 'document.id', '%(name)s',
          multiple=True), label=T('Fuentes')),
    Field('ini', 'date', readable=False, writable=False),
    Field('fin', 'date', readable=False, writable=False),
    Field(
        'iniDay',
        'string',
        requires=IS_IN_SET(day_list, zero=T('Sin Fecha')),
        default='Sin Fecha',
        writable=True,
        readable=True,
        ),
    Field(
        'iniMonth',
        'string',
        requires=IS_IN_SET(month_list, zero=T('Sin Fecha')),
        default='Sin Fecha',
        writable=True,
        readable=True,
        ),
    Field(
        'iniYear',
        'string',
        requires=IS_IN_SET(year_list, zero=T('Sin Fecha')),
        default='Sin Fecha',
        writable=True,
        readable=True,
        ),
    Field(
        'finDay',
        'string',
        requires=IS_IN_SET(day_list, zero=T('Sin Fecha')),
        default='Sin Fecha',
        writable=True,
        readable=True,
        ),
    Field(
        'finMonth',
        'string',
        requires=IS_IN_SET(month_list, zero=T('Sin Fecha')),
        default='Sin Fecha',
        writable=True,
        readable=True,
        ),
    Field(
        'finYear',
        'string',
        requires=IS_IN_SET(year_list, zero=T('Sin Fecha')),
        default='Sin Fecha',
        writable=True,
        readable=True,
        ),
    auth.signature,
    )

db.relOrg2Org.destinoO.widget = SQLFORM.widgets.autocomplete(request,
        db.Organizacion.alias, id_field=db.Organizacion.id,
        db=db(db.Organizacion.is_active == True))
db.relOrg2Org.documentSource.widget = SQLFORM.widgets.multiple.widget

# table tipoRelacionP20

db.define_table(
    'tipoRelacionP20',
    Field('parent', 'integer', required=True, default=0),
    Field('relationship', 'string', required=True),
    Field('generalizacion', 'string'),
    Field('inverse', 'string'),
    Field('orden', 'integer'),
    )

# table RelPersOrg

db.define_table(
    'RelPersOrg',
    Field('specificRelation', db.tipoRelacionP20, required=True,
          requires=IS_IN_DB(db, 'tipoRelacionP20.id',
          'tipoRelacionP20.relationship'), label='Conexion'),
    Field('origenP', db.persona, required=True, requires=IS_IN_DB(db,
          'persona.id', 'persona.alias')),
    Field('destinoO', db.Organizacion),
    Field('fdesde', 'string', required=False, notnull=False,
          label=T('Desde')),
    Field('fhasta', 'string', required=False, notnull=False,
          label=T('Hasta')),
    Field('isPast', 'boolean', label='es pasado'),
    Field('extraLabel', 'string', required=False, label=T('Sub Grupo'
          )),
    Field('documentSource', 'list:reference document', required=False,
          requires=IS_IN_DB(requiere, 'document.id', '%(name)s',
          multiple=True), label=T('Fuentes')),
    Field('transitive', 'integer', required=False, readable=False,
          writable=False),
    Field('transitiveP2P', 'integer', required=False, readable=False,
          writable=False),
    Field('ini', 'date', readable=False, writable=False),
    Field('fin', 'date', readable=False, writable=False),
    Field(
        'iniDay',
        'string',
        requires=IS_IN_SET(day_list, zero=T('Sin Fecha')),
        default='Sin Fecha',
        writable=True,
        readable=True,
        ),
    Field(
        'iniMonth',
        'string',
        requires=IS_IN_SET(month_list, zero=T('Sin Fecha')),
        default='Sin Fecha',
        writable=True,
        readable=True,
        ),
    Field(
        'iniYear',
        'string',
        requires=IS_IN_SET(year_list, zero=T('Sin Fecha')),
        default='Sin Fecha',
        writable=True,
        readable=True,
        ),
    Field(
        'finDay',
        'string',
        requires=IS_IN_SET(day_list, zero=T('Sin Fecha')),
        default='Sin Fecha',
        writable=True,
        readable=True,
        ),
    Field(
        'finMonth',
        'string',
        requires=IS_IN_SET(month_list, zero=T('Sin Fecha')),
        default='Sin Fecha',
        writable=True,
        readable=True,
        ),
    Field(
        'finYear',
        'string',
        requires=IS_IN_SET(year_list, zero=T('Sin Fecha')),
        default='Sin Fecha',
        writable=True,
        readable=True,
        ),
    auth.signature,
    )

db.RelPersOrg.destinoO.widget = SQLFORM.widgets.autocomplete(request,
        db.Organizacion.alias, id_field=db.Organizacion.id,
        db=db(db.Organizacion.is_active == True))
db.RelPersOrg.documentSource.widget = SQLFORM.widgets.multiple.widget

# table for relFamiliar

db.define_table(
    'relFamiliar',
    Field('parentesco', db.tipoParentesco, required=True,
          requires=IS_IN_DB(db, 'tipoParentesco.id',
          'tipoParentesco.name'), label='Relacion'),
    Field('origenP', db.persona, required=True,
          requires=IS_IN_DB(db(db.persona.is_active == True),
          'persona.id', 'persona.alias'), label='Persona'),
    Field('destinoP', db.persona,
          widget=SQLFORM.widgets.autocomplete(request,
          db.persona.alias, id_field=db.persona.id,
          keyword='_autocomplete_destinoP_%(fieldname)s',
          db=db(db.persona.is_active == True))),
    Field('documentSource', 'list:reference document', required=False,
          requires=IS_IN_DB(requiere, 'document.id', '%(name)s',
          multiple=True), label=T('Fuentes')),
    auth.signature,
    )

# a table birthEvent

db.define_table('birthEvent', Field('hasSource', db.document,
                label=T('Fuente'), requires=False), Field('place',
                db.place, requires=False), Field('fecha', 'date',
                requires=IS_DATE(), required=True), auth.signature)

db.define_table(
    'companeros',
    Field(
        'relacionP2O',
        db.RelPersOrg,
        label=T('Estudios'),
        required=True,
        readable=False,
        writable=False,
        ),
    Field('nexo', 'string', label=T('Nexo'), required=False),
    Field('relationComp', 'integer', required=True, readable=False,
          writable=False),
    Field('destinoP', db.persona, label=T('Persona'), required=True,
          widget=SQLFORM.widgets.autocomplete(request,
          db.persona.alias, id_field=db.persona.id,
          keyword='_autocomplete_destinoP_%(fieldname)s',
          db=db(db.persona.is_active == True))),
    Field('fechaI', 'string', required=False, label=T('Fecha Inicio')),
    Field('fechaF', 'string', required=False, label=T('Fecha Final')),
    Field('fuente', 'list:reference document', label=T('Fuente'),
          requires=IS_IN_DB(requiere, 'document.id',
          '%(name)s/%(documentURL)s', multiple=True)),
    auth.signature,
    )

db.define_table('importer', Field('filename', 'upload',
                autodelete=True), auth.signature)

me = auth.user_id
