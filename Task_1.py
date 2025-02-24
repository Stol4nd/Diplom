import random
import ipaddress

class Task_1:
    def __init__(self):
        self.ip_address = None
        self.subnet_mask = None
        self.network = None
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
        self.network = network
    
    def check_answers(self, student_answers):
        correct_answers = {
            'ip_class': str(self.ip_class),
            'decimal_network': str(self.network.network_address),
            'binary_network': format(int(ipaddress.IPv4Address(self.network.network_address)), '032b'),
            'decimal_first_host': str(list(self.network.hosts())[0]),
            'binary_first_host': format(int(ipaddress.IPv4Address(list(self.network.hosts())[0])), '032b'),
            'decimal_last_host': str(list(self.network.hosts())[-1]),
            'binary_last_host': format(int(ipaddress.IPv4Address(list(self.network.hosts())[-1])), '032b'),
            'broadcast_decimal': str(self.network.broadcast_address),
            'broadcast_binary': format(int(ipaddress.IPv4Address(self.network.broadcast_address)), '032b'),
            'decimal_subnet': self.subnet_mask,
            'binary_subnet': format(int(ipaddress.IPv4Address(self.subnet_mask)), '032b')
        }
        for key, value in correct_answers.items():
            print(f"{key}: {value}")
        # results = {}
        # for key, value in student_answers.items():
        #     if key in correct_answers:
        #         results[key] = (value == correct_answers[key])
        
        # return results

# Пример использования
generator = Task_1()
generator.generate_task()

print(f"Запишите класс, адрес сети, первого и последнего хостов в данной сети, а также маску сети и широковещательный адрес, используя классы, для IP-адреса: {generator.ip_address}")
generator.check_answers({})
