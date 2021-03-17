from PortUtils.Port import Port


def parse_ports():
    port_dict = dict()
    with open("PortUtils/nmap-services.dat", "r", encoding='utf-8') as f:
        for line in f:
            if line.startswith("#"):
                continue
            s = line.strip().split("\t")
            service_name = s[0]
            port_id = int((s[1].split("/"))[0])
            protocol_type = (s[1].split("/"))[1]
            usage_frequency = s[2]
            if port_id in port_dict:
                if port_dict[port_id].usage_frequency >= usage_frequency:
                    continue
            new_port = Port(service_name, port_id, protocol_type, usage_frequency)
            port_dict[port_id] = new_port
    return port_dict
