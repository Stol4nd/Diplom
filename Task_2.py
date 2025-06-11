import random
import ipaddress

class Task_2:
    
    field_order = [
        'decimal_network', 'binary_network',
        'decimal_first_host', 'binary_first_host',
        'decimal_last_host', 'binary_last_host',
        'broadcast_decimal', 'broadcast_binary',
        'decimal_subnet', 'binary_subnet'
    ]  
    
    field_translations = {
        'decimal_network': 'Десятичный IP-адрес сети',
        'binary_network': 'Двоичный IP-адрес сети',
        'decimal_first_host': 'Десятичный первый IP-адрес',
        'binary_first_host': 'Двоичный первый IP-адрес',
        'decimal_last_host': 'Десятичный последний IP-адрес',
        'binary_last_host': 'Двоичный последний IP-адрес',
        'broadcast_decimal': 'Десятичный широковещательный адрес',
        'broadcast_binary': 'Двоичный широковещательный адрес'
    }
    
    def __init__(self):
        self.ip_address = None
        self.subnet_mask = None   
    
    def generate_task(self):
        first_octet = random.randint(1, 255)
        second_octet = random.randint(1, 255)
        third_octet = random.randint(1, 255)
        fourth_octet = random.randint(1, 255)
        subnetbits = random.randint(8, 30)
        
        ip_str = f"{first_octet}.{second_octet}.{third_octet}.{fourth_octet}"
        network = ipaddress.IPv4Network(f"{ip_str}/{subnetbits}", strict=False)
        
        self.ip_address = ip_str
        self.subnet_mask = str(network.netmask)
    
    
    def check_answers(self, student_answers):
        
        network = ipaddress.IPv4Network(f"{self.ip_address}/{self.subnet_mask}", strict=False)
        network_address = network.network_address
        broadcast_address = network.broadcast_address
        first_host = ipaddress.IPv4Address(int(network_address) + 1)
        last_host = ipaddress.IPv4Address(int(broadcast_address) - 1)
        
        correct_answers = {
            'decimal_network' : str(network_address),
            'binary_network' : format(int(network_address), '032b'),
            'decimal_first_host': str(first_host),
            'binary_first_host': format(int(first_host), '032b'),
            'decimal_last_host': str(last_host),
            'binary_last_host': format(int(last_host), '032b'),
            'broadcast_decimal': str(broadcast_address),
            'broadcast_binary': format(int(broadcast_address), '032b')
        } 
        results = {key: None for key in self.field_order}
        for key, student_value in student_answers.items():
            if key in correct_answers:
                results[key] = (student_value == correct_answers[key])
        results = {k: v for k, v in results.items() if v is not None}
        return results
   