import pprint
from scapy.all import *
from scapy.config import Conf
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, TCP, UDP
from scapy.layers.http import HTTP
from scapy.utils import hexdump
# Conf.use_bpf = False

def get_net_ifaces():
    # interfaces = [_ for _ in ifaces] # 兼容性有问题，Windows 不可用
    interfaces = [_ for _ in get_working_ifaces()]
    return interfaces

def analyze_packet(packet):
    eth_layer = packet.getlayer(Ether)
    print("Ethernet II:")
    print(eth_layer.summary())
    
    
    if packet.haslayer(IP):
        ip = packet[IP]
        print("[*] Protocol: IP")
        print("\t Src IP:", ip.src, ' Dst IP:', ip.dst)
        ip_layer = packet.getlayer(IP)
        print(ip.summary())
        print(ip_layer.summary())
        
    if packet.haslayer(TCP):
        tcp = packet[TCP]
        print("[*] Protocol: TCP")
        print("\t Src Port:", tcp.sport, ' Dst Port:', tcp.dport)
        
    if packet.haslayer(UDP):
        udp = packet[UDP]
        print("[*] Protocol: UDP")
        print("\t Src Port:", udp.sport, ' Dst Port:', udp.dport)
    
    if packet.haslayer(HTTP):
        http = packet[HTTP]
        print("[*] Protocol: HTTP")
        print("\t Host:", http.host, ' Path:', http.path)
        
    rawhex = hexdump(packet, dump=True)
    print("[*] Raw:")
    print(rawhex)

class Sniffer():
    def __init__(self):
        self.available_ifaces = get_net_ifaces()
        self.iface = None
        self.stop = False
        self.cached_packets = []
        self.max_cache_packets_count = 1

    def get_interfaces(self):
        for interface in self.available_ifaces:
            print(interface.name)
        return self.available_ifaces

    def set_interface(self, interface_name):
        for interface in self.available_ifaces:
            if interface_name == interface.name:
                self.iface = interface
                return True
        return False
        
        # if interface in self.available_ifaces:
        #     self.iface = interface
        #     return True
        # return False

    def start_sniffing(self):
        if self.iface == None:
            return False
        print("--start sniffing--")
        print("[*] sniff on: ", self.iface ,' | name:', self.iface.name)
        cached_packets = sniff(iface=self.iface, count=self.max_cache_packets_count, prn=self.print_callback) # stop_filter=self.stop_filter_callback
        print("--end sniffing--")
        self.cached_packets.extend(cached_packets)
        return True

    def print_callback(self, packet):
        print(packet.summary())

    def stop_filter_callback(self, packet):
        if self.stop:
            return True
        return False

    def pause(self):
        self.stop = True
        
    def reset(self):
        self.stop = False
        self.iface = None
        self.cached_packets = []
        
    def analyze_packets(self):
        for packet in self.cached_packets:
            print("[*] analysis:")
            analyze_packet(packet)
            
if __name__ == "__main__":
    sniffer = Sniffer()
    sniffer.get_interfaces()
    
    sniffer.set_interface('WLAN')
    sniffer.start_sniffing()
    sniffer.analyze_packets()