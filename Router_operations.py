from netmiko import ConnectHandler


# Obtiene una lista de interfaces del router
def get_router_interfaces(user, password, ip_address):
    cisco_router = {
        'device_type': 'cisco_ios',
        'host': ip_address,
        'username': user,
        'password': password,
    }
    net_connect = ConnectHandler(**cisco_router)
    output = net_connect.send_command('show ip int brief', use_textfms=True)
    return output


# Obtiene la tabla de ruteo
def get_router_table(user, password, ip_address):
    cisco_router = {
        'device_type': 'cisco_ios',
        'host': ip_address,
        'username': user,
        'password': password,
    }
    net_connect = ConnectHandler(**cisco_router)
    output = net_connect.send_command('show ip route', use_textfsm=True)
    return output


# Agrega una o varias interfaces al router
# Body:
# 	interface_id
# 	ip_address
# 	mascara_red
def add_new_interfaces(user, password, ip_address, interfaces_data):
    cisco_router = {
        'device_type': 'cisco_ios',
        'host': ip_address,
        'username': user,
        'password': password,
    }
    net_connect = ConnectHandler(**cisco_router)
    net_connect.send_command('enable')
    net_connect.send_command('configure terminal')
    for value in interfaces_data:
        net_connect.send_command('interface {}'.format(value["interface_id"]))
        net_connect.send_command('ip address {} {}'.format(value["ip_address"], value["mascara_red"]))
        net_connect.send_command('no shutdown')
        net_connect.send_command('exit')
    return True


# Elimina una o varias interfaces del router
# Body:
# 	interface_id, ej. fa0/0
def delete_interfaces(user, password, ip_address, interfaces_data):
    cisco_router = {
        'device_type': 'cisco_ios',
        'host': ip_address,
        'username': user,
        'password': password,
    }
    net_connect = ConnectHandler(**cisco_router)
    net_connect.send_command('enable')
    net_connect.send_command('configure terminal')
    for value in interfaces_data:
        net_connect.send_command('no interface {}'.format(value["interface_id"]))
    return True
