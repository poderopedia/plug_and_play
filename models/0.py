from gluon.storage import Storage
settings = Storage()

settings.migrate = True
settings.title = 'Poderopedia Plug & Play'
settings.subtitle = 'powered by Poderopedia'
settings.author = 'Poderopedia'
settings.author_email = 'dev@poderopedia.com'
settings.keywords = ''
settings.description = ''
settings.layout_theme = 'Default'
settings.database_uri = 'sqlite://storage.sqlite'
settings.security_key = 'c05fcf75-9979-4291-833e-178cf3e73a37'
settings.email_server = 'localhost'
settings.email_sender = 'you@example.com'
settings.email_login = ''
settings.login_method = 'local'
settings.login_config = ''
settings.plugins = []

