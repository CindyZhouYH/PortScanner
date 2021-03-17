import concurrent.futures
import socket
import time
from collections import deque
from socket import error as socket_error

from PortUtils.parse_ports import parse_ports


class PostScanner:
    def __init__(self, timeout=10, required_num=None, target=None, thread_num_bound=10):
        self.all_ports = parse_ports()
        self.timeout = timeout
        self.thread_num_bound = thread_num_bound
        if target is not None:
            self.target_ports = []
            self.target_ports.append(target)
        else:
            self.target_ports = self.all_ports.keys()
            self.target_ports = self.get_required_ports(required_num)

    def get_required_ports(self, required_num):
        sorted_ports = sorted(self.all_ports.values())
        port_id_list = []
        for ele in sorted_ports:
            port_id_list.append(ele.port_id)
            if len(port_id_list) == required_num:
                break
        return sorted(port_id_list)

    def scanning(self, host_name=None, message=''):
        ip = self.preparing(host_name)
        start_time = time.time()
        results = self.scanning_ports(ip, message)
        stop_time = time.time()
        print('Target {} scanned in  {} seconds'.format(host_name, stop_time - start_time))
        return results

    def preparing(self, ip):
        try:
            socket.inet_aton(ip)
        except OSError or socket_error:
            raise ValueError(
                'Invalid input host name: {}.'.format(ip)
            )
        print('Start scanning target ip address: {}'.format(ip))
        try:
            server_ip = socket.gethostbyname(ip)
            print('Target IP is: {}'.format(str(server_ip)))
        except Exception:
            raise ValueError(
                'Cannot find ip address of host name: {}.'.format(ip)
            )
        return server_ip

    def scanning_ports(self, ip, message):
        results = dict()
        for port in self.target_ports:
            results[port] = "CLOSED"

        futures = deque()
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.thread_num_bound) as executor:
            for port in self.target_ports:
                future = executor.submit(self.try_TCP_connection, ip, port, message)
                futures.append(future)
                while len(futures) >= self.thread_num_bound:
                    self.get_answer(results, futures)
                    time.sleep(0.01)
            while futures:
                self.get_answer(results, futures)
            time.sleep(0.01)
        return results

    def get_answer(self, results, futures):
        for i in range(len(futures)):
            future = futures.popleft()
            if future.done():
                id, ans = future.result()
                results[id] = ans
                if ans == "OPEN":
                    port_info = '{}/{}'.format(str(id), self.all_ports[id].protocol_type.upper())
                    print("{:10}: {:>10}\n".format(port_info, ans))
            else:
                futures.append(future)


    def try_TCP_connection(self, ip, port_id, message):
        TCP_socket = None
        UCP_socket = None
        TCP_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        TCP_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        TCP_socket.settimeout(self.timeout)
        message = message.encode('utf-8', errors='replace')
        try:
            if message:
                UDP_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                UDP_socket.sendto(message, (ip, int(port_id)))

            result = TCP_socket.connect_ex((ip, int(port_id)))
            if message and result == 0:
                TCP_socket.sendall(message)

            if result == 0:
                return port_id, 'OPEN'
            else:
                return port_id, 'CLOSE'

        except socket_error as e:
            return port_id, 'CLOSE'
        finally:
            if UDP_socket is not None:
                UDP_socket.close()
            TCP_socket.close()
