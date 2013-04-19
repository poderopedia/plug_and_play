response.title = settings.title
response.subtitle = settings.subtitle
response.meta.author = '%(author)s <%(author_email)s>' % settings
response.meta.keywords = settings.keywords
response.meta.description = settings.description
response.menu = [
(T('Index'),URL('default','index')==URL(),URL('default','index'),[]),
(T('Testing Front'),URL('testFront','index')==URL(),URL('testFront','index'),[]),
(T('Crear'),False,[],[
    T('Sugerir Persona'),False,URL('sugerencia','persona'),
    T('Sugerir Persona'),False,URL('sugerencia','persona')]),
]
