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


# networks: ["172.16.1.0", "172.16.2.0"]
def rip_protocol(user, password, router_data, networks):
    cisco_router = {
        'device_type': 'cisco_ios',
        'host': router_data["loopback"],
        'username': user,
        'password': password,
    }
    net_connect = ConnectHandler(**cisco_router)
    net_connect.send_command('enable')
    net_connect.send_command('configure terminal')
    if router_data["routing_type"] == "2":
        net_connect.send_command('no router ospf')
    elif router_data["routing_type"] == "3":
        net_connect.send_command('no router eigrp')
    net_connect.send_command('router rip')
    net_connect.send_command('version 2')
    for network in networks:
        net_connect.send_command('network {}'.format(network))
    net_connect.send_command('no auto-sumary')
    net_connect.send_command('exit')


# networks: [
#   {
#       "ip": "172.16.0.0",
#       "wildcard": "0.0.0.255",
#       "area_id": "1",
#   },
# ]
def ospf_protocol(user, password, router_data, networks, process_id):
    cisco_router = {
        'device_type': 'cisco_ios',
        'host': router_data["loopback"],
        'username': user,
        'password': password,
    }
    net_connect = ConnectHandler(**cisco_router)
    net_connect.send_command('enable')
    net_connect.send_command('configure terminal')
    if router_data["routing_type"] == "1":
        net_connect.send_command('no router rip')
    elif router_data["routing_type"] == "3":
        net_connect.send_command('no router eigrp')
    net_connect.send_command('router ospf {}'.format(process_id))
    for network in networks:
        net_connect.send_command('network {} {} area {}'.format(network["ip"], network["wildcard"], network["area_id"]))
    net_connect.send_command('exit')


# networks: ["172.16.1.0", "172.16.2.0"]
def eigrp_protocol(user, password, router_data, networks, process_id):
    cisco_router = {
        'device_type': 'cisco_ios',
        'host': router_data["loopback"],
        'username': user,
        'password': password,
    }
    net_connect = ConnectHandler(**cisco_router)
    net_connect.send_command('enable')
    net_connect.send_command('configure terminal')
    if router_data["routing_type"] == "1":
        net_connect.send_command('no router rip')
    elif router_data["routing_type"] == "2":
        net_connect.send_command('no router ospf')
    net_connect.send_command('router ospf {}'.format(process_id))
    for network in networks:
        net_connect.send_command('network {}'.format(network))
    net_connect.send_command('exit')
