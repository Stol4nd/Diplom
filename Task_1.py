import random
import ipaddress

class Task_1:
    
    field_order = [
        'ip_class',
        'decimal_network', 'binary_network',
        'decimal_first_host', 'binary_first_host',
        'decimal_last_host', 'binary_last_host',
        'broadcast_decimal', 'broadcast_binary',
        'decimal_subnet', 'binary_subnet'
    ]   
    
    field_translations = {
        'ip_class': 'Класс публичного IP-адреса',
        'decimal_network': 'Десятичный IP-адрес сети',
        'binary_network': 'Двоичный IP-адрес сети',
        'decimal_first_host': 'Десятичный адрес первого хоста',
        'binary_first_host': 'Двоичный адрес первого хоста',
        'decimal_last_host': 'Десятичный адрес последнего хоста',
        'binary_last_host': 'Двоичный адрес последнего хоста',
        'broadcast_decimal': 'Десятичный широковещательный адрес',
        'broadcast_binary': 'Двоичный широковещательный адрес',
        'decimal_subnet': 'Десятичная маска подсети',
        'binary_subnet': 'Двоичная маска подсети'
    }
    
    def __init__(self):
        self.ip_address = None
        self.subnet_mask = None
        self.ip_class = None
        
    def generate_task(self):
        # Выбираем случайный класс публичного IP-адреса
        ip_classes = [
            'A',  # 10.0.0.0 - 10.255.255.255
            'B',  # 172.16.0.0 - 172.31.255.255
            'C'   # 192.168.0.0 - 192.168.255.255
        ]
        
        self.ip_class = random.choice(ip_classes)
        
        if self.ip_class == 'A':
            first_octet = 10
            second_octet = random.randint(0, 255)
            third_octet = random.randint(0, 255)
            fourth_octet = random.randint(0, 255)
            subnet_bits = 8
        elif self.ip_class == 'B':
            first_octet = 172
            second_octet = random.randint(16, 31)
            third_octet = random.randint(0, 255)
            fourth_octet = random.randint(0, 255)
            subnet_bits = 12
        else:  # C
            first_octet = 192
            second_octet = 168
            third_octet = random.randint(0, 255)
            fourth_octet = random.randint(0, 255)
            subnet_bits = 16
        
        # Создаем IP-адрес и маску сети
        ip_str = f"{first_octet}.{second_octet}.{third_octet}.{fourth_octet}"
        network = ipaddress.IPv4Network(f"{ip_str}/{subnet_bits}", strict=False)
        
        self.ip_address = ip_str
        self.subnet_mask = str(network.netmask)

    
    def check_answers(self, student_answers):
        network = ipaddress.IPv4Network(f"{self.ip_address}/{self.subnet_mask}", strict=False)
        network_address = network.network_address
        broadcast_address = network.broadcast_address
        first_host = ipaddress.IPv4Address(int(network_address) + 1)
        last_host = ipaddress.IPv4Address(int(broadcast_address) - 1)
        
        correct_answers = {
            'ip_class': str(self.ip_class),
            'decimal_network': str(network_address),
            'binary_network': format(int(network_address), '032b'),
            'decimal_first_host': str(first_host),
            'binary_first_host': format(int(first_host), '032b'),
            'decimal_last_host': str(last_host),
            'binary_last_host': format(int(last_host), '032b'),
            'broadcast_decimal': str(broadcast_address),
            'broadcast_binary': format(int(broadcast_address), '032b'),
            'decimal_subnet': self.subnet_mask,
            'binary_subnet': format(int(ipaddress.IPv4Address(self.subnet_mask)), '032b')
        }
        results = {key: None for key in self.field_order}
        for key, student_value in student_answers.items():
            if key in correct_answers:
                results[key] = (student_value == correct_answers[key])
        return results
