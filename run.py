import argparse
from Scanner import PortScanner


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="add your parameters")
    # 增加指定的参数
    parser.add_argument('--ip', type=str, default=None, help='target ip address')
    parser.add_argument('--num', type=int, default=100, help='the number of ports with highest usage you want to scan')
    parser.add_argument('--to', type=str, default=10, help='timeout')
    parser.add_argument('--tn', type=str, default=100, help='thread number upperbound')
    parser.add_argument('--p', type=int, default=None, help='target port')
    parser.add_argument('--m', type=str, default="hello from cindy", help='message')

    args = parser.parse_args()
    scanner = PortScanner.PostScanner(timeout=args.to, required_num=args.num, target=args.p, thread_num_bound=args.tn)
    res = scanner.scanning(args.ip, args.m)