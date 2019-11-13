import binascii
import socket
import struct
import sys
import hashlib
import random
from struct import * 

def Packet_Checksum_Corrupter(packetdata):
     if True and random.choice([0,1,0,1]) == 1: #  # Set to False to disable Packet Corruption. Default is 50% packets are corrupt
        return(b'Corrupt!')
     else:
        return(packetdata)

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
unpacker = struct.Struct('I I 8s 32s')
receieved_ack = -1

#Create the socket and listen
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
while True:
    #Receive Data
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    UDP_Packet = unpacker.unpack(data)
    print("received from:", addr)
    print("received message:", UDP_Packet)
    Packet_Checksum_Corrupter(UDP_Packet)

    
    
    #Create the Checksum for comparison
    values = (UDP_Packet[0],UDP_Packet[1],UDP_Packet[2])
    packer = struct.Struct('I I 8s')
    packed_data = packer.pack(*values)
    chksum =  bytes(hashlib.md5(packed_data).hexdigest(), encoding="UTF-8")

    receieved_ack= UDP_Packet[0]
    seq=UDP_Packet[1]

    
    #Compare Checksums to test for corrupt data
    if UDP_Packet[3] == chksum:
        print('CheckSums Match, Packet OK')
        print('Packet Received: ',UDP_Packet[0],UDP_Packet[1],UDP_Packet[2])

        if seq==1:
            seq=0
        else:
            seq=1
            
        resp = (receieved_ack,UDP_Packet[1])
        UDP_Data = struct.Struct('I I')
        respData = UDP_Data.pack(*resp)
        respChksum = bytes(hashlib.md5(respData).hexdigest(), encoding="UTF-8")
        resp = (receieved_ack,UDP_Packet[1],respChksum)
        UDP_data= struct.Struct('I I 32s')
        UDP_Packet = UDP_data.pack(*resp)
        sock.sendto(UDP_Packet, addr)
        print("Response being sent:",resp)

        sock.sendto(UDP_Packet,addr)

    else:
        print('Checksums Do Not Match, Packet Corrupt')

        if ack ==1:
            ack=0
        else:
            ack=1

        resp = (ack,UDP_Packet[1])
        UDP_Data = struct.Struct('I I')
        respData = UDP_data.pack(*resp)
        respChksum = bytes(hashlib.md5(respData).hexdigest(), encoding="UTF-8")

        resp = (ack, UDP_Packet, respChksum)
        UDP_Data = struct.Struct('I I')
        UDP_Packet = UDP_data.pack(*resp)
        sock.sendto(UDP_Packet, addr)












        
