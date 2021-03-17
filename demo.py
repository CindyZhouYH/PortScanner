from Scanner import PortScanner

scanner = PortScanner.PostScanner(timeout=10, required_num=100, target=None, thread_num_bound=100)

host_name = '10.136.211.23'

message = 'hello from CindyZhou'

res = scanner.scanning(host_name, message)
