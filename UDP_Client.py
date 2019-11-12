import binascii
import socket
import struct
import sys
import hashlib


UDP_IP = "127.0.0.1"
UDP_PORT = 5005

ack=0
received_ack=-1

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)

data_to_send = ('NCC-1701','NCC-1422','NCC-1017')

for data in data_to_send:

    data_bytes = data.encode("utf-8")
    
    #Create the Checksum
    values = (0,seq,data_bytes)
    UDP_Data = struct.Struct('I I 8s')
    packed_data = UDP_Data.pack(*values)
    chksum =  bytes(hashlib.md5(packed_data).hexdigest(), encoding="UTF-8")

    #Build the UDP Packet
    values = (0,seq,bytes_data,chksum)
    UDP_Packet_Data = struct.Struct('I I 8s 32s')
    UDP_Packet = UDP_Packet_Data.pack(*values)

    #Send the UDP Packet
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.sendto(UDP_Packet, (UDP_IP, UDP_PORT))
    
    print("Packet sent:", values)

    resp, addr = sock.recvfrom(4096)
    packet_received = unpacker.unpack(resp)
    print("Packet received:",packet_received)

    received_ack =packet_received[0]

    while received_ack != ack:
        print("Packet Corrupted: ACKs do not match")

        sock.sendto(UDP_Packet,(UDP_IP,UDP_PORT))

        print("Resending Packet:", UDP_Packet)

        resp, addr = sock.recvfrom(4096)
        packet_received = unpacket.unpack(resp)
        receievd_ack = packet_received[0]
        print("Packet Receieved: ",resp)


    if seq==1:
        seq=0
    else:
        seq =1

    if ack==1:
        ack=0
    else:
        ack=1


sock.close()
        



        
    


    
