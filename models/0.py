from gluon.storage import Storage
settings = Storage()

settings.migrate = True
settings.title = 'Poderopedia'
settings.subtitle = 'powered by Poderopedia'
settings.author = 'Team'
settings.author_email = 'dev@poderopedia.com'
settings.keywords = ''
settings.description = ''
settings.layout_theme = 'default'
settings.login_config = ''
settings.plugins = []
TEXT_EDITOR = 'amy'

response.title = request.application
response.subtitle = T('Redes de Poder en la Política y Negocios')
response.meta.author = 'Equipo Poderopedia'
response.meta.description = T('Redes de Poder en la Política y Negocios')
response.meta.keywords = 'Redes, Poder, Negocios, Política'

endYear=int(request.now.strftime('%Y'))
day_list=[x for x in range(1,32)]
day_list.append('Sin Fecha')
day_list.append('')
month_list=[x for x in range(1,13)]
month_list.append('Sin Fecha')
month_list.append('')
year_list=[x for x in range(1900,endYear+10)]
year_list.append('Sin Fecha')
year_list.append('')

