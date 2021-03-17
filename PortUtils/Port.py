class Port(object):
    def __init__(self, service_name, port_id, protocol_type, usage_frequency):
        self.service_name = service_name
        self.port_id = port_id
        self.protocol_type = protocol_type
        self.usage_frequency = usage_frequency

    def __eq__(self, other):
        return self.usage_frequency == other.usage_frequency and self.port_id == other.port_id

    def __lt__(self, other):
        if self.usage_frequency == other.usage_frequency:
            return self.port_id < other.port_id
        else:
            return self.usage_frequency > other.usage_frequency
