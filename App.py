from typing import Protocol
from flask import Flask, render_template, request, jsonify, redirect, session, url_for
from flask_mysqldb import MySQL
from datetime import timedelta
import MySQLdb.cursors, time


app = Flask(__name__)

# Requerida para la base de datos
app.secret_key = 'dipperkira'

# SQL configiguration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'usersdb'

app.config['SESSION_PERMANENT'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

mysql = MySQL(app)


protocols = {
    "0": "Ninguno",
    "1": "RIP",
    "2": "OSPF",
    "3": "IGRP"
}

# Limpia las variables usadas en el servidor
def clean_user():
    if 'loggedin' in session:
        session.pop('loggedin', None)
        session.pop('user_name', None)

    session.clear()


# Recibe el nombre de susuario y devuelve true si la cuenta existe en la base de datos
def user_exist(user_name):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM Users WHERE user_name = %s", [user_name])
    account = cursor.fetchone()

    return True if account else False


# Recibe la dirección mac y devuelve true si la cuenta existe en la base de datos
def device_exist(device_name):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        "SELECT * FROM Devices WHERE device_name = %s", [device_name])
    device = cursor.fetchone()

    return True if device else False


# Metodo para añadir nuevo dispositivo en la base de datos
def add_device(device_name, device_loop, routing_type):
    if device_exist(device_name):
        return False
    else:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO Devices VALUES (%s, %s, %s)', [
            device_name, device_loop, routing_type])
        mysql.connection.commit()

        return True


# Ruta del formulario de login
@app.route("/", methods=['POST', 'GET'])
@app.route("/index", methods=['POST', 'GET'])
def index():
    clean_user()

    return render_template("login.html")


# Verifica que el usuario exista y la contraseña sea valida, llama a menu para cargar la interfaz principal
@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return redirect(url_for('index'))
    elif request.method == 'POST':
        user_name = request.form['user_name']
        user_pass = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT * FROM Users WHERE user_name = %s AND password = %s", [user_name, user_pass])

        account = cursor.fetchone()

        # Si la cuenta existe crea los datos de sesión
        if account:
            session.clear()
            session['loggedin'] = True
            session['user_name'] = account['user_name']
            session['full_name'] = account['name'] + " " + account['last_name']
            session['admin'] = account['admin']

            return redirect(url_for('menu'))
        else:
            return render_template("login.html", msg="Usuario o contraseña incorrecto")


# Menu al ingresar correctamente, se llama después del login
@app.route("/menu", methods=['POST', 'GET'])
def menu():
    global users, devices
    if not 'loggedin' in session:
        return redirect(url_for('index'))
    else:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM Users")
        users = cursor.fetchall()

        cursor.execute("SELECT * FROM Devices")
        devices = cursor.fetchall()

        return render_template('menu.html', users=users, devices=devices, user_name=session['user_name'])


# Cierre de sesión y limpia llama a clena_user
@app.route('/logout')
def logout():
    clean_user()

    return redirect(url_for('index'))

# Lógica del registro de un nuevo usuario, por defecto seran usuarios estándar


@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'user_name' in request.form and "name" in request.form and 'last_name' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        user_name = request.form['user_name']
        name = request.form['name']
        last_name = request.form['last_name']
        password = request.form['password']
        email = request.form['email']
        is_admin = 0

        # Verifica si la cuenta se encuentra en la base de datos
        if user_exist(user_name):
            msg = "Error! nombre de usuario no disponible"
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO Users VALUES (%s, %s, %s, %s, %s, %s)',
                           [user_name, name, last_name, password, email, is_admin])
            mysql.connection.commit()

            msg = 'Registro exitoso!'

    elif request.method == 'POST':
        msg = 'Llene todos los campos del formulario!'

    return render_template('register.html', msg=msg)


# Lanza el template de Cambiar contraseña
@app.route("/password/template/<user_name>", methods=['POST', 'GET'])
def password_template(user_name):
    return render_template('password.html', user_name=user_name)


# Lógica del cambio de contaseña
@app.route("/password/", methods=['POST', 'GET'])
def change_password():
    if request.method == "GET":
        return redirect(url_for('index'))
    else:
        user_name = request.form['user_name']
        user_pass = request.form['password']

        if user_exist(user_name):
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('UPDATE Users SET password = %s WHERE user_name = %s',
                           [user_pass, user_name])
            mysql.connection.commit()

            msg = "Contresaña actualizada correctamente!"
        else:
            msg = "Error interno"

    return render_template('password.html', user_name=user_name, msg=msg)


# Lanza la vista de dispositivos si se encuentra logeado
@app.route('/devices/', methods=['GET', 'POST'])
def devices_teplate():
    if 'loggedin' in session:
        global devices
        return render_template('/device/devices.html', devices=devices, type=session['admin'])
    else:
        return render_template('error.html')


# Lanza la vista de usuarios si se encuentra logeado
@app.route('/users/', methods=['GET', 'POST'])
def users_template():
    if 'loggedin' in session:
        global users
        return render_template('/user/users.html', users=users, type=session['admin'])
    else:
        return render_template('error.html')


# Lanza la vista de inicio si se encuentra logeado
@app.route('/home/', methods=['GET', 'POST'])
def home_template():
    if 'loggedin' in session:
        global users, devices
        return render_template('home.html', users=users, devices=devices, username=session['full_name'])
    else:
        return render_template('error.html')


# Lanza la vista de protocolos si se encuentra logeado
@app.route('/protocols/', methods=['GET', 'POST'])
def protocols_template():
    if 'loggedin' in session:
        global devices
        return render_template('/protocol/protocols.html', devices=devices)
    else:
        return render_template('error.html')


# Lanza el template para editar usuario, recibe el nombre de usuario
@app.route('/edit/user/template/<user_name>', methods=['GET', 'POST'])
def edit_template(user_name):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Users WHERE user_name = %s', [user_name])
        mysql.connection.commit()

        user = cursor.fetchone()

        data = {
            "user_name": user["user_name"],
            "name": user["name"],
            "last_name": user["last_name"],
            "password": user["password"],
            "email": user["email"],
            "type": user["admin"]
        }

        return render_template('/user/edit-user.html', data=data)
    else:
        return redirect(url_for('index'))


# Lógica para editar usuario, recibe datos de un formulario y devuelve un mensaje informativo
@app.route('/edit/user/', methods=['GET', 'POST'])
def edit_user():
    if request.method == 'GET' or not 'loggedin' in session:
        return redirect(url_for('menu'))
    else:
        name = request.form['name']
        last_name = request.form['last_name']
        user_name = request.form['user_name']
        user_pass = request.form['password']
        user_mail = request.form['email']
        user_type = request.form['type']
        new_user_name = request.form['new_user']

        if user_exist(user_name):
            if new_user_name == user_name:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("UPDATE Users SET name = %s, last_name = %s, password = %s, email = %s, admin = %s WHERE user_name = %s",
                               [name, last_name, user_pass, user_mail, user_type, user_name])

                mysql.connection.commit()
                msg = "Cambios guardados correctamente"
            else:
                if user_exist(new_user_name):
                    msg = "Error! Nombre de usuario no disponible!"
                else:
                    cursor = mysql.connection.cursor(
                        MySQLdb.cursors.DictCursor)
                    cursor.execute("UPDATE Users SET user_name = %s, name = %s, last_name = %s, password = %s, email = %s, admin = %s WHERE user_name = %s",
                                   [new_user_name, name, last_name, user_pass, user_mail, user_type, user_name])
                    user_name = new_user_name
                    mysql.connection.commit()
                    msg = "Cambios guardados correctamente"

            data = {
                "user_name": user_name,
                "name": name,
                "last_name": last_name,
                "password": user_pass,
                "email": user_mail,
                "type": user_type
            }
        else:
            msg = "Cuenta no encontrada"

        return render_template('/user/edit-user.html', data=data, msg=msg)


# Lógica para añadir un nuevo usuario, recibe datos de un formulario
@app.route('/new-user', methods=['GET', 'POST'])
def new_user():
    msg = ''

    if request.method == 'POST' and 'user_name' in request.form and "name" in request.form and 'last_name' in request.form and 'password' in request.form and 'email' in request.form and 'type' in request.form:
        user_name = request.form['user_name']
        name = request.form['name']
        last_name = request.form['last_name']
        password = request.form['password']
        email = request.form['email']
        user_type = request.form['type']

        if user_exist(user_name):
            msg = "Error! nombre de usuario no disponible"
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO Users VALUES (%s, %s, %s, %s, %s, %s)',
                           [user_name, name, last_name, password, email, user_type])
            mysql.connection.commit()

            msg = 'Registro exitoso!'

    elif request.method == 'POST':
        msg = 'Llene todos los campos del formulario!'

    return render_template('/user/new-user.html', msg=msg)


# Lógica para añadir un nuevo dispostivo
@app.route('/new-device', methods=['GET', 'POST'])
def new_device():
    msg = ''
    if request.method == 'POST' and 'loopback' in request.form and "device_name" in request.form and 'routing_type' in request.form:
        device_name = request.form['device_name']
        device_loop = request.form['loopback']
        routing_type = request.form['routing_type']

        if device_exist(device_name):
            msg = "Error! Dispositivo ya registrado"
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO Devices VALUES (%s, %s, %s)', [
                           device_name, device_loop, routing_type])
            mysql.connection.commit()

            msg = 'Registro exitoso!'

    elif request.method == 'POST':
        msg = 'Llene todos los campos del formulario!'

    return render_template('/device/new-device.html', msg=msg)


# Lanza el template para editar dispositivo,j recibe la dirección mac del dispositivo a editar
@app.route('/edit/device/template/<device_name>', methods=['GET', 'POST'])
def edit_device_template(device_name):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        'SELECT * FROM Devices WHERE device_name = %s', [device_name])
    mysql.connection.commit()

    device = cursor.fetchone()

    data = {
        "device_name": device["device_name"],
        "loopback": device["loopback"],
        "routing_type": device["routing_type"]
    }

    return render_template('/device/edit-device.html', data=data)


# Lógica para guardar cambios en el dispositivo editado
@app.route('/edit/device/', methods=['GET', 'POST'])
def edit_device():
    if request.method == 'GET':
        return redirect(url_for('menu'))
    else:
        device_name = request.form['device_name']
        loopback = request.form['loopback']
        routing_type = request.form['routing_type']
        new_name = request.form['new_name']

        if device_exist(device_name):
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            if device_name == new_name:
                cursor.execute("UPDATE Devices SET loopback = %s, routing_type = %s WHERE device_name = %s",
                               [loopback, routing_type, device_name])
                mysql.connection.commit()

                msg = "Cambios guardados correctamente"
            else:
                if device_exist(new_name):
                    msg = "Nombre de dispositivo ya registrado."

                else:
                    cursor.execute("UPDATE Devices SET device_name = %s, loopback = %s, routing_type = %s WHERE device_name = %s",
                                   [new_name, loopback, routing_type, device_name])
                    mysql.connection.commit()
                    msg = "Cambios guardados correctamente"
                    device_name = new_name

            data = {
                "device_name": device_name,
                "loopback": loopback,
                "routing_type": routing_type
            }
        else:
            msg = "Dispositivo no encontrado"

        return render_template('/device/edit-device.html', data=data, msg=msg)


# Lógica para elilminar usuarios, recibe el nombre de usuario del usuario a eliminar
@app.route('/delete/user/', methods=['GET', 'POST'])
def delete_user():
    if request.method == 'GET':
        return jsonify({'status': "FAIL"})
    else:
        user_name = request.get_data().decode("utf-8")

        if user_exist(user_name):
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                "DELETE FROM Users WHERE user_name = %s", [user_name])
            mysql.connection.commit()

            status = "SUCCESS"
            msg = ""
        else:
            status = "FAIL"
            msg = "Usuario no encontrado"

        return jsonify({'status': status, 'msg': msg})


# Lógica para elilminar usuarios, recibe el nombre de usuario del usuario a eliminar
@app.route('/delete/device/', methods=['GET', 'POST'])
def delete_device():
    if request.method == 'GET':
        return jsonify({'status': "FAIL"})
    else:
        device_name = request.get_data().decode("utf-8")

        if device_exist(device_name):
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                "DELETE FROM Devices WHERE device_name = %s", [device_name])
            mysql.connection.commit()

            status = "SUCCESS"
            msg = ""
        else:
            status = "FAIL"
            msg = "Usuario no encontrado"

        return jsonify({'status': status, 'msg': msg})


#Recibe las redes y el protocolo a usar
@app.route('/change/protocol', methods=['GET', 'POST'])
def change_protocol():
    global protocols

    msg = "" 

    if request.method == "POST":
        protocol_data = request.get_json()

        protocol = protocol_data['protocol']
        networks = protocol_data['networks']

        print(protocols[protocol])
        print(networks)

        for net in networks:
            print(net)

        msg = "SUCCESS"
    else:
        msg = "FAIL"

    time.sleep(5)

    return jsonify({'msg': msg})