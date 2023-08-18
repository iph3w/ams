import socket
import fcntl
import struct


class Utility:
    def get_ip_address_info(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip_address_info = {}
        for idx in socket.if_nameindex():
            if idx[1] != 'lo':
                interface = idx[1]
                ip = socket.inet_ntoa(
                    fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', bytes(interface, 'utf-8')))[20:24]
                )
                netmask = socket.inet_ntoa(
                    fcntl.ioctl(s.fileno(), 0x891b, struct.pack('256s', bytes(interface, 'utf-8')))[20:24]
                )
                ip_address_info[ip] = netmask
        return ip_address_info
