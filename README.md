# networkManager
Proyecto redes 3

## Dependencias

Se requiere de flask y flask-mysqldb se instalan con:

```
pip install flask
pip install flask-mysqldb
```

## Base de datos

Se requiere de una cuenta mysql administrador con:

```
Usuario: root
Contraseña: root
```
 >***Se puede cambiar los ajustes en App.py de la linea 15 y 16***


Para instalar la base de datos estando en la consola de mysql ejecutar:

```
source DIRECCION_DEL_ARCHIVO/usersdb.sql
```

## Aplicación

La base de datos viene con un usuario por defecto de tipo administrador, con la que se puede ingresar a la aplicación web

```
Usuario: admin
Contraseña: admin
```

Para ejecutar la aplicación, estando en la carpeta del proyecto:

```
export FLASK_APP=App
flask run
```
> Para habilitar el depurador ejecutar ***export FLASK_ENV=development***
