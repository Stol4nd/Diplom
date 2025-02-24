import random
import ipaddress

class Task_2:
    def __init__(self):
        self.ip_address = None
        self.subnet_mask = None
        self.network = None    
    
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
        self.network = network
    
    
    def chech_answers(self, student_answers):
        correct_answers = {
            'decimal_network' : str(self.network.network_address),
            'binary_network' : format(int(ipaddress.IPv4Address(self.network.network_address)), '032b'),
            'first_ip_decimal': str(list(self.network.hosts())[0]),
            'first_ip_binary': format(int(ipaddress.IPv4Address(list(self.network.hosts())[0])), '032b'),
            'last_ip_decimal': str(list(self.network.hosts())[-1]),
            'last_ip_binary': format(int(ipaddress.IPv4Address(list(self.network.hosts())[-1])), '032b'),
            'broadcast_decimal': str(self.network.broadcast_address),
            'broadcast_binary': format(int(ipaddress.IPv4Address(self.network.broadcast_address)), '032b')
        } 
        print(correct_answers)
        results = {}
        for key, value in student_answers.items():
            if key in correct_answers:
                results[key] = (value == correct_answers[key])
        
        return results
    
task = Task_2()
task.generate_task()
print(f"Запишите адрес сети, адреса первого и последнего хостов, а также широковещательный адрес для IP-адреса {task.ip_address} с маской {task.subnet_mask}")
task.chech_answers({})

        