
import random
import ipaddress

class Task_4:
    
    field_order = [
        'decimal_network', 'binary_network',
        'decimal_subnet', 'binary_subnet'
    ]
    
    field_translations = {
        'decimal_network': 'Десятичный IP-адрес сети',
        'binary_network': 'Двоичный IP-адрес сети',
        'decimal_subnet': 'Десятичная маска подсети',
        'binary_subnet': 'Двоичная маска подсети'
    }
    
    def __init__(self):
        self.network = None
        self.ip_address_first = None
        self.ip_address_second = None
        
    def generate_task(self):
        first_octet = random.randint(100, 255)
        second_octet = random.randint(100, 255)
        third_octet = random.randint(1, 255)
        fourth_octet = random.randint(1, 255)
        subnet = random.randint(16, 24)
        
        ip_str = ipaddress.IPv4Address(f"{first_octet}.{second_octet}.{third_octet}.{fourth_octet}")
        self.network = ipaddress.IPv4Network((ip_str, subnet), strict=False)
        self.ip_address_first = str(list(self.network.hosts())[0])
        self.ip_address_second = str(list(self.network.hosts())[-1])
        self.network = str(self.network)
        
    def check_answers(self, student_answers):
        network = ipaddress.IPv4Network(self.network, strict=False)
        correct_answers = {
            'decimal_network': str(network.network_address),
            'binary_network': format(int(ipaddress.IPv4Address(network.network_address)), '032b'),
            'decimal_subnet': str(network.netmask),
            'binary_subnet': format(int(ipaddress.IPv4Address(network.netmask)), '032b')
        }
        results = {key: None for key in self.field_order}
        for key, student_value in student_answers.items():
            if key in correct_answers:
                if student_value == correct_answers[key]:
                    results[key] = f"{key}: Правильно"
                else:
                    results[key] = f"{key}: Неправильно. Ответ студента: {student_value}"
        results = {k: v for k, v in results.items() if v is not None}
        return results
