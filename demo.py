from Scanner import PortScanner

scanner = PortScanner.PostScanner(timeout=10, required_num=100, target=None, thread_num_bound=100)

# host_name = '49.232.136.182'
# host_name = '47.94.243.9'
host_name = '192.168.75.1'

message = 'hello from CindyZhou'

res = scanner.scanning(host_name, message)
