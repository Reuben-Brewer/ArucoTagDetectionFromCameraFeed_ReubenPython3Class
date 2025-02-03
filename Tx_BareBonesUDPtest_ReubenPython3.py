# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision E, 02/02/2024

Verified working on: Python 3.12 for Windows 11 64-bit.
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
    UDP_IPtargetAddressThatWillRxData = "127.0.0.1"
    UDP_Port = 1 #Cannot use 0 as a port.
    UDP_TxBufferSizeInBytes = 64  #Max-packet-size is 1500 in-practice (maximum transmission unit (MTU) to prevent packet-fragmenting), 65507 bytes in theory-only

    UDP_SocketObject = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #AF_INET for internet, SOCK_DGRAM for UDP

    UDP_SocketObject.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, UDP_TxBufferSizeInBytes)
    print("UDP_SocketObject.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF): " + str(UDP_SocketObject.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)))

    message_prefix = ""

    counter = 0
    #######################################################################################################################

    #######################################################################################################################
    keyboard.on_press_key("esc", ExitProgram_Callback)
    keyboard.on_press_key("space", ExitProgram_Callback)
    keyboard.on_press_key("c", ExitProgram_Callback)
    keyboard.on_press_key("e", ExitProgram_Callback)
    keyboard.on_press_key("q", ExitProgram_Callback)
    #######################################################################################################################

    #######################################################################################################################
    while EXIT_PROGRAM_FLAG == 0:
        
        try:
            counter = counter + 1
            message = message_prefix + "counter: " + str(counter) + ", time: " + str(time.time())
            message = message.encode('utf-8') #Python3 requires you to use '.encode('utf-8')' on strings before they can be sent to the socket.
            
            UDP_SocketObject.sendto(message, (UDP_IPtargetAddressThatWillRxData, UDP_Port))
            
            print("Message to Tx: " + str(message) + ", message length = " + str(len(message)))
            
            time.sleep(0.10)

        except:
            exceptions = sys.exc_info()[0]
            print("Tx_TestCountDown_UDP_ReubenPython3, Exceptions: %s" % exceptions)
            traceback.print_exc()
    #######################################################################################################################

    #######################################################################################################################
    try:
        UDP_SocketObject.close()
    except:
        pass
    #######################################################################################################################
    
#######################################################################################################################
#######################################################################################################################