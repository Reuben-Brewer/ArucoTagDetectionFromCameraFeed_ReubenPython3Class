# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision G, 12/22/2025

Verified working on: Python 3.12 for Windows 11 64-bit and Raspberry Pi Bookworm.
'''

__author__ = 'reuben.brewer'

#########################################################
import sys
import socket
import time
import keyboard
import traceback
#########################################################

#######################################################################################################################
#######################################################################################################################
def ExitProgram_Callback(OptionalArg = 0):
    global EXIT_PROGRAM_FLAG

    print("ExitProgram_Callback event fired!")

    EXIT_PROGRAM_FLAG = 1
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
if __name__ == '__main__':

    global EXIT_PROGRAM_FLAG
    EXIT_PROGRAM_FLAG = 0

    #######################################################################################################################
    UDP_IP_ClientRxSide = "192.168.1.77" #IP address of this listening/client/Rx machine that's running this code and receiving data. We don't need to know the address that's sending/serving/Tx the data.

    UDP_Port = 1 #Cannot use 0 as a port.
    UDP_RxBufferSizeInBytes = 200 #Max-packet-size is 1500 in-practice (maximum transmission unit (MTU) to prevent packet-fragmenting), 65507 bytes in theory-only

    UDP_SocketObject = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  #AF_INET for internet, SOCK_DGRAM for UDP
    UDP_SocketObject.bind((UDP_IP_ClientRxSide, UDP_Port)) #bind() needed only on the client/Rx side, not on the server/Tx side.

    UDP_SocketObject.settimeout(1.0) #Without a timeout set, the while 1: loop will continue forever when the keyboard-press triggers a program exit.

    UDP_SocketObject.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, UDP_RxBufferSizeInBytes)
    print("UDP_SocketObject.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF): " + str(UDP_SocketObject.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)))
    
    '''
    https://stackoverflow.com/questions/28563518/buffer-size-for-reading-udp-packets-in-python

    SO_RCVBUF
    Sets or gets the maximum socket receive buffer in bytes.  The kernel doubles
    this value (to allow space for bookkeeping overhead) when it is set using
    setsockopt(2), and this doubled  value  is  returned  by  getsockopt(2).
    The default value is set by the /proc/sys/net/core/rmem_default file, and
    the maximum allowed value is set by the /proc/sys/net/core/rmem_max file.
    The minimum (doubled) value for this option is 256.
    '''
    #######################################################################################################################

    #######################################################################################################################
    keyboard.on_press_key("esc", ExitProgram_Callback)
    #######################################################################################################################

    #######################################################################################################################
    while EXIT_PROGRAM_FLAG == 0:

        try:

            data, AddressOfSocketSendingThisData = UDP_SocketObject.recvfrom(UDP_RxBufferSizeInBytes)
            data = data.decode('utf-8')
            print("Rx_TestCountDown_UDP_ReubenPython3: Received UDP data: "  + str(data) + ", len = " + str(len(data)))

        except:
            exceptions = sys.exc_info()[0]
            if str(exceptions) != "<class 'socket.timeout'>": #Only display non-UDP-timeout exceptions
                print("Rx_TestCountDown_UDP_ReubenPython3, Exceptions: %s" % exceptions)
                #traceback.print_exc()

    #######################################################################################################################

    #######################################################################################################################
    try:
        UDP_SocketObject.close()
    except:
        pass
    #######################################################################################################################

#######################################################################################################################
#######################################################################################################################