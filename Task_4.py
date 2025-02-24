import random
import ipaddress

class Task_4:
    def __init__(self):
        self.network = None
        self.ip_address_first = None
        self.ip_address_second = None
        self.subnet_mask = None
        
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
    
    def check_answers(self, student_answers):
        
        correct_answers = {
            'decimal_network': str(self.network.network_address),
            'binary_network': format(int(ipaddress.IPv4Address(self.network.network_address)), '032b'),
            'decimal_subnet': str(self.network.netmask),
            'binary_subnet': format(int(ipaddress.IPv4Address(self.network.netmask)), '032b')
        }
        print(correct_answers)
        # for key, value in correct_answers.items():
        #     print(f"{key}: {value}")
        # results = {}
        # for key, value in student_answers.items():
        #     if key in correct_answers:
        #         results[key] = (value == correct_answers[key])
        
        # return results

# Пример использования
generator = Task_4()
generator.generate_task()

print(f"Запишите адрес сети и маску сети, соответствующие указанному диапазону IP адресов: от {generator.ip_address_first} до {generator.ip_address_second}")
generator.check_answers({})