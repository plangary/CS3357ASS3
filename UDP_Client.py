import binascii
import socket
import struct
import sys
import hashlib
from struct import * 

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
seq=0
ack=0
received_ack=-1
unpacker = struct.Struct('I I 32s')

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)

data_to_send = ('NCC-1701','NCC-1422','NCC-1017')

for data in data_to_send:

    data_bytes = data.encode("utf-8")
    
    #Create the Checksum
    values = (ack,seq,data_bytes)
    UDP_Data = struct.Struct('I I 8s')
    packed_data = UDP_Data.pack(*values)
    chksum =  bytes(hashlib.md5(packed_data).hexdigest(), encoding="UTF-8")

    #Build the UDP Packet
    values = (ack,seq,data_bytes,chksum)
    UDP_Packet_Data = struct.Struct('I I 8s 32s')
    UDP_Packet = UDP_Packet_Data.pack(*values)

    #Send the UDP Packet
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.sendto(UDP_Packet, (UDP_IP, UDP_PORT))
    
    print("Packet sent:", values)

    data, addr = sock.recvfrom(1024)
    UDP_Packet_Data_rcv = unpacker.unpack(data)
    print("Packet received:",UDP_Packet_Data_rcv)

    received_ack =UDP_Packet_Data_rcv[0]

    while received_ack != ack:
        print("Packet Corrupted: ACKs do not match")
      
        sock.sendto(UDP_Packet,(UDP_IP,UDP_PORT))
        print("Resending Packet:", UDP_Packet)

        resp, addr = sock.recvfrom(1024)
        packet_received = unpacker.unpack(resp)
        receievd_ack = packet_received[0]
        print("Packet Receieved: ",resp)


    if received_ack==1:
        ack=0
    else:
        ack=1


sock.close()
        



        
    


    
