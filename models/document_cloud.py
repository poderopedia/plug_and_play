__author__ = 'Evolutiva'

#document Cloud Table


entityList=['persona','empresa','organizacion']
accessList=['public','private','organization']
db.define_table('documentCloud',
    Field('dc_id','string'),
    Field('file', 'upload'),
    Field('title', 'string', required=True,requires=IS_ALPHANUMERIC(), label=T('Titulo Documento')),
    Field('source', 'string', label=T('Fuente del Documento')),
    Field('description', 'text',label=T('Descripción del Documento')),
    Field('related_article', 'string',label=T('URL'),comment=T('the URL of the article associated with the document')),
    Field('published_url', 'string',label=T('URL'),comment=T('the URL of the page on which the document will be embedded')),
    Field('access', 'string'),
    Field('project', 'integer'),
    Field('data', 'string',default='{"date":'+str(request.now)+', "auth_user":'+str(me)+'}'),
    Field('secure', 'string',default='false'),
    auth.signature,
    format='%(title)s'
)
