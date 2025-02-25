import random 
import ipaddress
import math

class Task_5:
    def __init__(self):
        self.network = None
        self.ip_address = None
        self.network_mask = None
        self.subnets = None
        
    def generate_task(self):
        first_octet = random.randint(100, 255)
        second_octet = random.randint(100, 255)
        third_octet = random.randint(1, 255)
        fourth_octet = random.randint(1, 255)
        ip_str = f"{first_octet}.{second_octet}.{third_octet}.{fourth_octet}"    
        
        self.network_mask = random.randint(16, 28)  
        network = ipaddress.IPv4Network((ip_str, self.network_mask), strict=False)
        self.ip_address = str(network.network_address)
        self.network = str(network)
        
        self.subnets = random.randint(2, 4)  
        self.subnet_bits = math.ceil(self.subnets / 2)
    
    def check_answers(self, student_answers):
        new_prefix = self.network_mask + self.subnet_bits
        network = ipaddress.IPv4Network(self.network, strict=False)
        subnets = list(network.subnets(new_prefix=new_prefix))
        correct_answers = []
        for i, subnet in enumerate(subnets):
            if i >= self.subnets:
                break
            correct_answers.append(
                {'first_host_decimal': str(list(subnet.hosts())[0]),
                 'first_host_binary': format(int(list(subnet.hosts())[0]), '032b'),
                 'last_host_decimal': str(list(subnet.hosts())[-1]),
                 'last_host_binary': format(int(list(subnet.hosts())[-1]), '032b'),
                 'subnet_decimal': str(subnet.network_address),
                 'subnet_binary': format(int(subnet.network_address), '032b'),
                 'subnet_mask_decimal': str(subnet.netmask),
                 'subnet_mask_binary': format(int(subnet.netmask), '032b')
                }
            )
        results = []
        for i in range(self.subnets):
            results_i = {}
            for key, value in student_answers[i].items():
                if key in correct_answers[i]:
                    results_i[key] = (value == correct_answers[i][key])
            results.append(results_i)
            print(results_i)
task_5 = Task_5()
task_5.generate_task()
print(task_5.__dict__)