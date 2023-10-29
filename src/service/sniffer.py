from scapy.all import *
# from scapy.all import sniff, Packet, ShortField, StrField, IPField, show_interfaces
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, TCP, UDP
from scapy.layers.http import HTTP
from scapy.config import Conf
from scapy.utils import hexdump

def analyze_packet(packet):
    analyzed_result = {
        "time": packet.time,
        "summary": packet.summary(),
        "protocol": "",
        "src": "",
        "dst": "",
        "length": len(packet),
        "Info": "",
        "layers": [
            # Ethernet II
            # IP
            # ICP/UDP
            # ...
        ],
        "raw": ""
    }
    
    # 数据链路层 Ethernet II
    eth_layer_packet = packet.getlayer(Ether)
    layer_data = {}
    layer_data['src'] = eth_layer_packet.src
    layer_data['dst'] = eth_layer_packet.dst
    layer_data['type'] = eth_layer_packet.type
    layer_data['summary'] = "Ethernet II, Src: {}, Dst: {}".format(layer_data['src'], layer_data['dst'])
    analyzed_result['layers'].append(layer_data)
    analyzed_result['src'] = layer_data['src']
    analyzed_result['dst'] = layer_data['dst']
    analyzed_result['protocol'] = "Ether"
    
    # IP层 Internet Protocol Version 4 
    if packet.haslayer(IP):
        ip_layer_packet = packet.getlayer(IP)
        layer_data = {}
        layer_data['version'] = ip_layer_packet.version
        layer_data['ihl'] = ip_layer_packet.ihl
        layer_data['tos'] = ip_layer_packet.tos
        layer_data['len'] = ip_layer_packet.len
        layer_data['id'] = ip_layer_packet.id
        # layer_data['flags'] = ip_layer_packet.flags
        layer_data['frag'] = ip_layer_packet.frag
        layer_data['ttl'] = ip_layer_packet.ttl
        layer_data['proto'] = ip_layer_packet.proto
        layer_data['chksum'] = ip_layer_packet.chksum
        layer_data['src'] = ip_layer_packet.src
        layer_data['dst'] = ip_layer_packet.dst
        # layer_data['options'] = ip_layer_packet.options
        
        layer_data['summary'] = "Internet Protocol Version 4, Src: {}, Dst: {}, Len: {}".format(layer_data['src'], layer_data['dst'], layer_data['len'])
        analyzed_result['layers'].append(layer_data)
        
        analyzed_result['src'] = layer_data['src']
        analyzed_result['dst'] = layer_data['dst']
    
    if packet.haslayer(TCP):
        tcp_layer_packet = packet.getlayer(TCP)
        layer_data = {}
        layer_data['sport'] = tcp_layer_packet.sport
        layer_data['dport'] = tcp_layer_packet.dport
        layer_data['seq'] = tcp_layer_packet.seq
        layer_data['ack'] = tcp_layer_packet.ack
        layer_data['dataofs'] = tcp_layer_packet.dataofs
        layer_data['reserved'] = tcp_layer_packet.reserved
        # layer_data['flags'] = tcp_layer_packet.flags
        layer_data['window'] = tcp_layer_packet.window
        layer_data['chksum'] = tcp_layer_packet.chksum
        layer_data['urgptr'] = tcp_layer_packet.urgptr
        # layer_data['options'] = tcp_layer_packet.options
        
        layer_data['summary'] = "Transmission Control Protocol, Src Port: {}, Dst Port: {}, Seq: {}, Ack: {}".format(layer_data['sport'], layer_data['dport'], layer_data['seq'], layer_data['ack'])
        analyzed_result['layers'].append(layer_data)
        
        analyzed_result['protocol'] = "TCP"
        
    if packet.haslayer(UDP):
        ucp_layer_packet = packet.getlayer(UDP)
        layer_data = {}
        layer_data['sport'] = ucp_layer_packet.sport
        layer_data['dport'] = ucp_layer_packet.dport
        layer_data['len'] = ucp_layer_packet.len
        # layer_data['chksum'] = ucp_layer_packet.len
        
        layer_data['summary'] = "User Datagram Protocol, Src Port: {}, Dst Port: {}".format(layer_data['sport'], layer_data['dport'])
        analyzed_result['layers'].append(layer_data)

        analyzed_result['protocol'] = "UDP"
    
    # 应用层协议: TODO
    
    analyzed_result['raw'] = hexdump(packet, dump=True)
    return analyzed_result

class Sniffer:
    def __init__(self) -> None:
        self._available_ifaces = get_working_ifaces()
        self._iface = None
        self._stop = True
        self._cached_packets = []
        self._max_cache_packets_count = 1
        self._analyzed_packets = []
        self._filter_expression = ""
    
    def get_network_interfaces(self):
        net_ifaces = [_.name for _ in self._available_ifaces]
        return net_ifaces

    def get_analyzed_packets(self):
        return self._analyzed_packets
    
    def set_network_interface(self, interface_name):
        for interface in self._available_ifaces:
            if interface_name == interface.name:
                self.iface = interface
                return True
        return False
    
    def set_filter_expression(self, filter_exp):
        # TODO: check exp is valid
        self._filter_expression = filter_exp
        return True

    def start_online_sniffing(self):
        if self.iface == None:
            return False
        self._stop = False
        cached_packets = sniff(iface=self.iface, count=self._max_cache_packets_count, prn=self.print_callback, timeout=5) 
        # stop_filter=self.stop_filter_callback
        self._stop = True
        self._cached_packets.extend(cached_packets)
        return True
    
    def print_callback(self, packet):
        self._analyzed_packets.append(analyze_packet(packet))
        
