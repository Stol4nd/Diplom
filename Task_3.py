import random
import ipaddress

class Task_3:
    def __init__(self):
        self.ip_address = None
        self.subnet_mask = None
        self.subnets = None
        self.network = None
        
    def generate_task(self):
        # Выбираем случайный класс публичного IP-адреса
        ip_classes = [
            'A',  # 10.0.0.0 - 10.255.255.255
            'B',  # 172.16.0.0 - 172.31.255.255
            'C'   # 192.168.0.0 - 192.168.255.255
        ]
        
        ip_class = random.choice(ip_classes)
        
        if ip_class == 'A':
            first_octet = 10
            second_octet = random.randint(0, 255)
            third_octet = random.randint(0, 255)
            fourth_octet = random.randint(0, 255)
            subnet_bits = 8
        elif ip_class == 'B':
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

        self.subnets = random.randint(1, 4)
        subnet_bits += self.subnets
        # Создаем IP-адрес и маску сети
        ip_str = f"{first_octet}.{second_octet}.{third_octet}.{fourth_octet}"
        network = ipaddress.IPv4Network(f"{ip_str}/{subnet_bits}", strict=False)
        
        self.ip_address = ip_str
        self.subnet_mask = str(network.netmask)
    
    def check_answers(self, student_answers):
        network = ipaddress.IPv4Network(f"{self.ip_address}/{self.subnet_mask}", strict=False)
        correct_answers = {
            'decimal_network': str(network.network_address),
            'binary_network': format(int(ipaddress.IPv4Address(network.network_address)), '032b'),
            'decimal_first_host': str(list(network.hosts())[0]),
            'binary_first_host': format(int(ipaddress.IPv4Address(list(network.hosts())[0])), '032b'),
            'decimal_last_host': str(list(network.hosts())[-1]),
            'binary_last_host': format(int(ipaddress.IPv4Address(list(network.hosts())[-1])), '032b'),
            'broadcast_decimal': str(network.broadcast_address),
            'broadcast_binary': format(int(ipaddress.IPv4Address(network.broadcast_address)), '032b'),
            'decimal_subnet': self.subnet_mask,
            'binary_subnet': format(int(ipaddress.IPv4Address(self.subnet_mask)), '032b')
        }
        results = {}
        for key, value in student_answers.items():
            if key in correct_answers:
                results[key] = (value == correct_answers[key])
        
        return results