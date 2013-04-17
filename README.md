plug_and_play
=============

Admin Plug_and_Play

Esta guía describe los pasos para la instalación de "Admin Plug_and_Play" en un sistema Ubuntu.

###Requisitos:

Para trabajar con Plug_and_Play se necesitan los siguientes componentes

* Framework Web2py http://web2py.com/
* Repositorio Github https://github.com/
* Motor de bases de datos (MySQL o PostgreSQL) http://www.mysql.com/
 

####Instalación de Web2py:

1. Ingresar a http://www.web2py.com/init/default/download para descargar los archivos necesarios.
2. De acuerdo a la versión de sistema operativo, elegir la opción respectiva para usuarios normales (Normal Users).
3. Después de la descarga, descomprimir el fichero. Se sugiere descomprimir en <code>/opt/webapps/web2py/</code> el cual será utilizado en la guía como el directorio de instalación de web2py.
4. Para ejecutar web2py, desde el directorio de instalación ingresar el comando <code>python2.5 web2py.py</code>
5. Cada vez que se ejecute, Web2py abrirá la aplicación de administración y solicitará escoger una contraseña. Esta contraseña protegerá el acceso a la página de administración, por lo que es importante no omitir este paso.
6. Se puede acceder a la página de administración de web2py desde algun explorador web, escribiendo en la barra de direcciones : <code>http://127.0.0.1:8000</code> o <code>http://localhost:8000</code> e ingresando el password de administración.

####Instalación de Github

1. Ejecutar el siguiente comando en el terminal:
<code> $ sudo apt-get install git </code>
2. Para configurar Git correctamente, siga las instrucciones descritas en: https://help.github.com/articles/set-up-git

####Instalación de MySQL

1. Ejecutar el siguiente comando en el terminal:
<code> $ sudo apt-get install mysql-server mysql-client </code>
Si el comando no realiza la instalación, ejecutar <code> $ sudo apt-get update</code> y volver a intentar.

###Instalación y configuración de Plug_and_Play

1. Hacer un clon del repositorio actual de Plug_and_play dentro de la carpeta /opt/webapps/web2py/applications/. Usar comando <code>$ git clone https://github.com/poderopedia/plug_and_play.git</code>.
2. En la carpeta /opt/webapps/web2py/applications/plug_and_play/models hay un archivo llamado <code>0.py</code> .Este archivo debe modificarse para ajustarse a la configuración local. Nota: Es importante modificar principalmente el parámetro <code>settings.database_uri</code>, el cual debe contener la cadena de conexión a la base de datos. Por ejemplo: <code>settings.database_uri = 'mysql://dbuser:usrpass@localhost/thedatabase'</code>
3. En la carpeta /opt/webapps/web2py/applications/plug_and_play/models hay un archivo llamado <code>db.py</code>. En este archivo deben cambiarse las ocurrencias de <code> migrate=False</code> a <code> migrate=True</code>, y al igual que en "0.py" se debe especificar la cadena de conexión a la base de datos. Ejemplo <code> db = DAL('mysql://dbuser:usrpass@localhost/thedatabase')</code>
4. Editar el archivo "/opt/webapps/web2py/applications/plug_and_play/models/app_config.py", rellenándolo con la información apropiada del proyecto.
5. Si web2py esta siendo ejecutado, se debe terminar el proceso, y ser ejecutado nuevamente para que carguen las nuevas configuraciones.
6. Por defecto, se puede acceder la aplicación Plug_and_Play desde el explorador web, en la dirección: <code>http://127.0.0.1:8000/plug_and_play</code>
