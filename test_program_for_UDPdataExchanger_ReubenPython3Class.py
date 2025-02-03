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

##########################################
from CSVdataLogger_ReubenPython3Class import *
from MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class import *
from MyPrint_ReubenPython2and3Class import *
from UDPdataExchanger_ReubenPython3Class import *
##########################################

##########################################
import os
import sys
import platform
import time
import datetime
import threading
import collections
import argparse
import keyboard
##########################################

##########################################
from tkinter import *
import tkinter.font as tkFont
from tkinter import ttk
##########################################

##########################################
import platform
if platform.system() == "Windows":
    import ctypes
    winmm = ctypes.WinDLL('winmm')
    winmm.timeBeginPeriod(1) #Set minimum timer resolution to 1ms so that time.sleep(0.001) behaves properly.
##########################################

###########################################################################################################
##########################################################################################################
def getPreciseSecondsTimeStampString():
    ts = time.time()

    return ts
##########################################################################################################
##########################################################################################################

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
def ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(input, number_of_leading_numbers = 4, number_of_decimal_places = 3):

    number_of_decimal_places = max(1, number_of_decimal_places) #Make sure we're above 1

    ListOfStringsToJoin = []

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    if isinstance(input, str) == 1:
        ListOfStringsToJoin.append(input)
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    elif isinstance(input, int) == 1 or isinstance(input, float) == 1:
        element = float(input)
        prefix_string = "{:." + str(number_of_decimal_places) + "f}"
        element_as_string = prefix_string.format(element)

        ##########################################################################################################
        ##########################################################################################################
        if element >= 0:
            element_as_string = element_as_string.zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1)  # +1 for sign, +1 for decimal place
            element_as_string = "+" + element_as_string  # So that our strings always have either + or - signs to maintain the same string length
        else:
            element_as_string = element_as_string.zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1 + 1)  # +1 for sign, +1 for decimal place
        ##########################################################################################################
        ##########################################################################################################

        ListOfStringsToJoin.append(element_as_string)
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    elif isinstance(input, list) == 1:

        if len(input) > 0:
            for element in input: #RECURSION
                ListOfStringsToJoin.append(ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

        else: #Situation when we get a list() or []
            ListOfStringsToJoin.append(str(input))

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    elif isinstance(input, tuple) == 1:

        if len(input) > 0:
            for element in input: #RECURSION
                ListOfStringsToJoin.append("TUPLE" + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

        else: #Situation when we get a list() or []
            ListOfStringsToJoin.append(str(input))

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    elif isinstance(input, dict) == 1:

        if len(input) > 0:
            for Key in input: #RECURSION
                ListOfStringsToJoin.append(str(Key) + ": " + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(input[Key], number_of_leading_numbers, number_of_decimal_places))

        else: #Situation when we get a dict()
            ListOfStringsToJoin.append(str(input))

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    else:
        ListOfStringsToJoin.append(str(input))
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    if len(ListOfStringsToJoin) > 1:

        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        StringToReturn = ""
        for Index, StringToProcess in enumerate(ListOfStringsToJoin):

            ################################################
            if Index == 0: #The first element
                if StringToProcess.find(":") != -1 and StringToProcess[0] != "{": #meaning that we're processing a dict()
                    StringToReturn = "{"
                elif StringToProcess.find("TUPLE") != -1 and StringToProcess[0] != "(":  # meaning that we're processing a tuple
                    StringToReturn = "("
                else:
                    StringToReturn = "["

                StringToReturn = StringToReturn + StringToProcess.replace("TUPLE","") + ", "
            ################################################

            ################################################
            elif Index < len(ListOfStringsToJoin) - 1: #The middle elements
                StringToReturn = StringToReturn + StringToProcess + ", "
            ################################################

            ################################################
            else: #The last element
                StringToReturn = StringToReturn + StringToProcess

                if StringToProcess.find(":") != -1 and StringToProcess[-1] != "}":  # meaning that we're processing a dict()
                    StringToReturn = StringToReturn + "}"
                elif StringToProcess.find("TUPLE") != -1 and StringToProcess[-1] != ")":  # meaning that we're processing a tuple
                    StringToReturn = StringToReturn + ")"
                else:
                    StringToReturn = StringToReturn + "]"

            ################################################

        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

    elif len(ListOfStringsToJoin) == 1:
        StringToReturn = ListOfStringsToJoin[0]

    else:
        StringToReturn = ListOfStringsToJoin

    return StringToReturn
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def ConvertDictToProperlyFormattedStringForPrinting(DictToPrint, NumberOfDecimalsPlaceToUse = 3, NumberOfEntriesPerLine = 1, NumberOfTabsBetweenItems = 3):

    ProperlyFormattedStringForPrinting = ""
    ItemsPerLineCounter = 0

    for Key in DictToPrint:

        if isinstance(DictToPrint[Key], dict): #RECURSION
            ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                 Key + ":\n" + \
                                                 ConvertDictToProperlyFormattedStringForPrinting(DictToPrint[Key], NumberOfDecimalsPlaceToUse, NumberOfEntriesPerLine, NumberOfTabsBetweenItems)

        else:
            ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                 Key + ": " + \
                                                 ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(DictToPrint[Key], 0, NumberOfDecimalsPlaceToUse)

        if ItemsPerLineCounter < NumberOfEntriesPerLine - 1:
            ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\t"*NumberOfTabsBetweenItems
            ItemsPerLineCounter = ItemsPerLineCounter + 1
        else:
            ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\n"
            ItemsPerLineCounter = 0

    return ProperlyFormattedStringForPrinting
#######################################################################################################################
#######################################################################################################################

##########################################################################################################
##########################################################################################################
def IncrementTestFloat_Callback(OptionalArugment = 0):
    global TestFloatToTx_CallbackOffset

    TestFloatToTx_CallbackOffset = TestFloatToTx_CallbackOffset + 1.0
    print("IncrementTestFloat_Callback event has fired!")
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def DecrementTestFloat_Callback(OptionalArugment = 0):
    global TestFloatToTx_CallbackOffset

    TestFloatToTx_CallbackOffset = TestFloatToTx_CallbackOffset - 1.0
    print("DecrementTestFloat_Callback event has fired!")
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def GUI_update_clock():
    global root
    global EXIT_PROGRAM_FLAG
    global GUI_RootAfterCalNmackInterval_Milliseconds
    global USE_GUI_FLAG

    global UDPdataExchanger_Object
    global UDPdataExchanger_OPEN_FLAG
    global SHOW_IN_GUI_UDPdataExchanger_FLAG
    global UDPdataExchanger_MostRecentDict
    global UDPdataExchanger_MostRecentDict_Label

    global MyPrint_ReubenPython2and3ClassObject
    global MyPrint_OPEN_FLAG
    global SHOW_IN_GUI_MyPrint_FLAG

    global CSVdataLogger_ReubenPython3ClassObject
    global CSVdataLogger_OPEN_FLAG
    global SHOW_IN_GUI_CSVdataLogger_FLAG

    if USE_GUI_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
        #########################################################
        #########################################################

            #########################################################
            if UDPdataExchanger_OPEN_FLAG == 1 and SHOW_IN_GUI_UDPdataExchanger_FLAG == 1:
                UDPdataExchanger_MostRecentDict_Label["text"]  = ConvertDictToProperlyFormattedStringForPrinting(UDPdataExchanger_MostRecentDict, NumberOfDecimalsPlaceToUse=3, NumberOfEntriesPerLine=3, NumberOfTabsBetweenItems=1)
            #########################################################

            #########################################################
            if UDPdataExchanger_OPEN_FLAG == 1 and SHOW_IN_GUI_UDPdataExchanger_FLAG == 1:
                UDPdataExchanger_Object.GUI_update_clock()
            #########################################################

            #########################################################
            if MyPrint_OPEN_FLAG == 1 and SHOW_IN_GUI_MyPrint_FLAG == 1:
                MyPrint_ReubenPython2and3ClassObject.GUI_update_clock()
            #########################################################

            #########################################################
            if CSVdataLogger_OPEN_FLAG == 1 and SHOW_IN_GUI_CSVdataLogger_FLAG == 1:
                CSVdataLogger_ReubenPython3ClassObject.GUI_update_clock()
            #########################################################

            root.after(GUI_RootAfterCalNmackInterval_Milliseconds, GUI_update_clock)
        #########################################################
        #########################################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
def ExitProgram_Callback(OptionalArugment = 0):
    global EXIT_PROGRAM_FLAG
    global CSVdataLogger_ReubenPython3ClassObject
    global CSVdataLogger_OPEN_FLAG

    ##########################################################################################################
    ##########################################################################################################
    if CSVdataLogger_OPEN_FLAG == 1:

        ##########################################################################################################
        if CSVdataLogger_ReubenPython3ClassObject.IsSaving() == 0:
            print("ExitProgram_Callback event fired!")
            EXIT_PROGRAM_FLAG = 1
        ##########################################################################################################

        ##########################################################################################################
        else:
            print("CSV is saving, cannot exit!")
            EXIT_PROGRAM_FLAG = 0
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    else:
        print("ExitProgram_Callback event fired!")
        EXIT_PROGRAM_FLAG = 1
    ##########################################################################################################
    ##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def GUI_Thread():
    global root
    global root_Xpos
    global root_Ypos
    global root_width
    global root_height
    global GUI_RootAfterCalNmackInterval_Milliseconds
    global USE_TABS_IN_GUI_FLAG

    ################################################# KEY GUI LINE
    #################################################
    root = Tk()
    #################################################
    #################################################

    #################################################
    #################################################
    global TabControlObject
    global Tab_MainControls
    global Tab_UDPdataExchanger
    global Tab_MyPrint
    global Tab_CSVdataLogger

    if USE_TABS_IN_GUI_FLAG == 1:
        #################################################
        TabControlObject = ttk.Notebook(root)

        Tab_UDPdataExchanger = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_UDPdataExchanger, text='   UDP   ')

        Tab_MainControls = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_MainControls, text='   Main Controls   ')

        Tab_CSVdataLogger = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_CSVdataLogger, text='   CSVdataLogger   ')

        Tab_MyPrint = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_MyPrint, text='   MyPrint Terminal   ')

        TabControlObject.pack(expand=1, fill="both")  # CANNOT MIX PACK AND GRID IN THE SAME FRAME/TAB, SO ALL .GRID'S MUST BE CONTAINED WITHIN THEIR OWN FRAME/TAB.

        ############# #Set the tab header font
        TabStyle = ttk.Style()
        TabStyle.configure('TNotebook.Tab', font=('Helvetica', '12', 'bold'))
        #############

        #################################################
    else:
        #################################################
        Tab_MainControls = root
        Tab_UDPdataExchanger = root
        Tab_MyPrint = root
        Tab_CSVdataLogger = root
        #################################################

    #################################################
    #################################################
    
    #################################################
    #################################################
    global UDPdataExchanger_MostRecentDict_Label
    UDPdataExchanger_MostRecentDict_Label = Label(Tab_MainControls, text="UDPdataExchanger_MostRecentDict_Label", width=120, font=("Helvetica", 10))
    UDPdataExchanger_MostRecentDict_Label.grid(row=0, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
    #################################################
    #################################################

    #################################################
    ################################################# THIS BLOCK MUST COME 2ND-TO-LAST IN def GUI_Thread() IF USING TABS.
    root.protocol("WM_DELETE_WINDOW", ExitProgram_Callback)  # Set the calNmack function for when the window's closed.
    root.title("test_program_for_UDPdataExchanger_ReubenPython3Class")
    root.geometry('%dx%d+%d+%d' % (root_width, root_height, root_Xpos, root_Ypos)) # set the dimensions of the screen and where it is placed
    root.after(GUI_RootAfterCalNmackInterval_Milliseconds, GUI_update_clock)
    root.mainloop()
    #################################################
    #################################################

    #################################################  THIS BLOCK MUST COME LAST IN def GUI_Thread() REGARDLESS OF CODE.
    #################################################
    root.quit() #Stop the GUI thread, MUST BE CALLED FROM GUI_Thread
    root.destroy() #Close down the GUI thread, MUST BE CALLED FROM GUI_Thread
    #################################################
    #################################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
if __name__ == '__main__':

    #################################################
    #################################################
    global my_platform

    if platform.system() == "Linux":

        if "raspberrypi" in platform.uname():  # os.uname() doesn't work in windows
            my_platform = "pi"
        else:
            my_platform = "linux"

    elif platform.system() == "Windows":
        my_platform = "windows"

    elif platform.system() == "Darwin":
        my_platform = "mac"

    else:
        my_platform = "other"

    print("The OS platform is: " + my_platform)
    #################################################
    #################################################

    #################################################
    #################################################
    global USE_GUI_FLAG
    USE_GUI_FLAG = 1

    global USE_TABS_IN_GUI_FLAG
    USE_TABS_IN_GUI_FLAG = 1

    global USE_UDPdataExchanger_FLAG
    USE_UDPdataExchanger_FLAG = 1

    global USE_CSVdataLogger_FLAG
    USE_CSVdataLogger_FLAG = 1

    global USE_MyPrint_FLAG
    USE_MyPrint_FLAG = 1

    global USE_MyPlotterPureTkinterStandAloneProcess_FLAG
    USE_MyPlotterPureTkinterStandAloneProcess_FLAG = 1

    global USE_SinusoidalMotionInput_FLAG
    USE_SinusoidalMotionInput_FLAG = 1

    global USE_KEYBOARD_FLAG
    USE_KEYBOARD_FLAG = 1
    #################################################
    #################################################

    #################################################
    #################################################
    global SHOW_IN_GUI_UDPdataExchanger_FLAG
    SHOW_IN_GUI_UDPdataExchanger_FLAG = 1

    global SHOW_IN_GUI_MyPrint_FLAG
    SHOW_IN_GUI_MyPrint_FLAG = 1

    global SHOW_IN_GUI_CSVdataLogger_FLAG
    SHOW_IN_GUI_CSVdataLogger_FLAG = 1
    #################################################
    #################################################

    #################################################
    #################################################
    global GUI_ROW_UDPdataExchanger
    global GUI_COLUMN_UDPdataExchanger
    global GUI_PADX_UDPdataExchanger
    global GUI_PADY_UDPdataExchanger
    global GUI_ROWSPAN_UDPdataExchanger
    global GUI_COLUMNSPAN_UDPdataExchanger
    GUI_ROW_UDPdataExchanger = 1

    GUI_COLUMN_UDPdataExchanger = 0
    GUI_PADX_UDPdataExchanger = 1
    GUI_PADY_UDPdataExchanger = 1
    GUI_ROWSPAN_UDPdataExchanger = 1
    GUI_COLUMNSPAN_UDPdataExchanger = 1

    global GUI_ROW_CSVdataLogger
    global GUI_COLUMN_CSVdataLogger
    global GUI_PADX_CSVdataLogger
    global GUI_PADY_CSVdataLogger
    global GUI_ROWSPAN_CSVdataLogger
    global GUI_COLUMNSPAN_CSVdataLogger
    GUI_ROW_CSVdataLogger = 2

    GUI_COLUMN_CSVdataLogger = 0
    GUI_PADX_CSVdataLogger = 1
    GUI_PADY_CSVdataLogger = 1
    GUI_ROWSPAN_CSVdataLogger = 1
    GUI_COLUMNSPAN_CSVdataLogger = 1

    global GUI_ROW_MyPrint
    global GUI_COLUMN_MyPrint
    global GUI_PADX_MyPrint
    global GUI_PADY_MyPrint
    global GUI_ROWSPAN_MyPrint
    global GUI_COLUMNSPAN_MyPrint
    GUI_ROW_MyPrint = 3

    GUI_COLUMN_MyPrint = 0
    GUI_PADX_MyPrint = 1
    GUI_PADY_MyPrint = 1
    GUI_ROWSPAN_MyPrint = 1
    GUI_COLUMNSPAN_MyPrint = 1
    #################################################
    #################################################

    #################################################
    #################################################
    global UDP_RxOrTxRole
    global UDP_InternalOrExtenal

    argparse_Object = argparse.ArgumentParser()
    argparse_Object.add_argument("-r", "--role", nargs='?', const='arg_was_not_given', required=False, help="'Rx' or 'Tx'")
    argparse_Object.add_argument("-ioe", "--InternalOrExternal", nargs='?', const='arg_was_not_given', required=False, help="'Internal' or 'External'")
    ARGV_Dict = vars(argparse_Object.parse_args())
    #print("ARGV_Dict: " + str(ARGV_Dict))

    #################################################
    if ARGV_Dict["role"] != None:
         UDP_RxOrTxRole  = str(ARGV_Dict["role"]).lower()

         if UDP_RxOrTxRole not in ["rx", "tx"]:
             print("Error: role must be 'rx' or 'tx'.")
             exit()
    else:
        UDP_RxOrTxRole = "rx"

    print("UDP_RxOrTxRole: " + str(UDP_RxOrTxRole))
    #################################################

    #################################################
    if ARGV_Dict["InternalOrExternal"] != None:
        UDP_InternalOrExtenal  = str(ARGV_Dict["InternalOrExternal"]).lower()

        if UDP_InternalOrExtenal not in ["internal", "external"]:
         print("Error: role must be 'internal' or 'external'.")
         exit()

        if UDP_InternalOrExtenal == "internal":
            IPV4_address = "127.0.0.1"

        if UDP_InternalOrExtenal == "external":
            IPV4_address = "192.168.1.77"

    else:
        IPV4_address = "127.0.0.1"

    #################################################

    print("IPV4_address: " + str(IPV4_address))
    #################################################
    #################################################

    #################################################
    #################################################
    global EXIT_PROGRAM_FLAG
    EXIT_PROGRAM_FLAG = 0

    global CurrentTime_MainLoopThread
    CurrentTime_MainLoopThread = -11111.0

    global StartingTime_MainLoopThread
    StartingTime_MainLoopThread = -11111.0

    global root

    global root_Xpos

    if UDP_RxOrTxRole == "rx":
        root_Xpos = 900
    else:
        root_Xpos = 0

    global root_Ypos
    root_Ypos = 0

    global root_width
    root_width = 900

    global root_height
    root_height = 1020 - root_Ypos

    global TabControlObject
    global Tab_MainControls
    global Tab_UDPdataExchanger
    global Tab_MyPrint

    global GUI_RootAfterCalNmackInterval_Milliseconds
    GUI_RootAfterCalNmackInterval_Milliseconds = 30
    
    global SinusoidalInput_MinValue
    SinusoidalInput_MinValue = -1.0

    global SinusoidalInput_MaxValue
    SinusoidalInput_MaxValue = 1.0

    global SinusoidalInput_ROMtestTimeToPeakAngle
    SinusoidalInput_ROMtestTimeToPeakAngle = 3.0
    
    global SinusoidalInput_TimeGain
    SinusoidalInput_TimeGain = math.pi / (2.0 * SinusoidalInput_ROMtestTimeToPeakAngle)
    #################################################
    #################################################

    #################################################
    #################################################
    global UDPdataExchanger_Object
    UDPdataExchanger_Object = list()

    global UDPdataExchanger_OPEN_FLAG
    UDPdataExchanger_OPEN_FLAG = 0

    global UDPdataExchanger_MostRecentDict
    UDPdataExchanger_MostRecentDict = dict()

    global UDPdataExchanger_MostRecentDict_TestFloat
    UDPdataExchanger_MostRecentDict_TestFloat = 0.0

    global UDPdataExchanger_MostRecentDict_TestTime
    UDPdataExchanger_MostRecentDict_TestTime = 0.0

    global TestFloatToTx
    TestFloatToTx = 0.0

    global TestFloatToTx_CallbackOffset
    TestFloatToTx_CallbackOffset = 0.0
    #################################################
    #################################################

    #################################################
    #################################################
    global MyPrint_ReubenPython2and3ClassObject

    global MyPrint_OPEN_FLAG
    MyPrint_OPEN_FLAG = -1
    #################################################
    #################################################

    #################################################
    #################################################
    global CSVdataLogger_ReubenPython3ClassObject

    global CSVdataLogger_OPEN_FLAG
    CSVdataLogger_OPEN_FLAG = -1

    global CSVdataLogger_MostRecentDict
    CSVdataLogger_MostRecentDict = dict()

    global CSVdataLogger_MostRecentDict_Time
    CSVdataLogger_MostRecentDict_Time = -11111.0
    #################################################
    #################################################

    #################################################
    #################################################
    global MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject

    global MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG
    MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG = -1

    global MyPlotterPureTkinter_MostRecentDict
    MyPlotterPureTkinter_MostRecentDict = dict()

    global MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag
    MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag = -1

    global LastTime_MainLoopThread_MyPlotterPureTkinterStandAloneProcess
    LastTime_MainLoopThread_MyPlotterPureTkinterStandAloneProcess = -11111.0
    #################################################
    #################################################

    #################################################  KEY GUI LINE
    #################################################
    if USE_GUI_FLAG == 1:
        print("Starting GUI thread...")
        GUI_Thread_ThreadingObject = threading.Thread(target=GUI_Thread)
        GUI_Thread_ThreadingObject.setDaemon(True) #Should mean that the GUI thread is destroyed automatically when the main thread is destroyed.
        GUI_Thread_ThreadingObject.start()
        time.sleep(0.5)  #Allow enough time for 'root' to be created that we can then pass it into other classes.
    else:
        root = None
        Tab_MainControls = None
        Tab_UDPdataExchanger = None
        Tab_MyPrint = None
    #################################################
    #################################################

    #################################################
    #################################################

    #################################################
    global UDPdataExchanger_GUIparametersDict
    UDPdataExchanger_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_UDPdataExchanger_FLAG),
                                    ("root", Tab_UDPdataExchanger),
                                    ("EnableInternal_MyPrint_Flag", 0),
                                    ("NumberOfPrintLines", 10),
                                    ("UseBorderAroundThisGuiObjectFlag", 0),
                                    ("GUI_ROW", GUI_ROW_UDPdataExchanger),
                                    ("GUI_COLUMN", GUI_COLUMN_UDPdataExchanger),
                                    ("GUI_PADX", GUI_PADX_UDPdataExchanger),
                                    ("GUI_PADY", GUI_PADY_UDPdataExchanger),
                                    ("GUI_ROWSPAN", GUI_ROWSPAN_UDPdataExchanger),
                                    ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_UDPdataExchanger)])
    #################################################

    #################################################
    global UDPdataExchanger_setup_dict
    UDPdataExchanger_setup_dict = dict([("GUIparametersDict", UDPdataExchanger_GUIparametersDict),
                                        ("NameToDisplay_UserSet", "UDPdataExchanger"),
                                        ("UDP_RxOrTxRole", UDP_RxOrTxRole),
                                        ("IPV4_address", IPV4_address),
                                        ("IPV4_Port", 1),
                                        ("UDP_BufferSizeInBytes", 100),
                                        ("MainThread_TimeToSleepEachLoop", 0.030),
                                        ("WatchdogTimerExpirationDurationSeconds", 0.5)])
    #################################################

    #################################################
    if USE_UDPdataExchanger_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            UDPdataExchanger_Object = UDPdataExchanger_ReubenPython3Class(UDPdataExchanger_setup_dict)
            UDPdataExchanger_OPEN_FLAG = UDPdataExchanger_Object.OBJECT_CREATED_SUCCESSFULLY_FLAG

            #################################################
            if UDPdataExchanger_OPEN_FLAG != 1:
                print("Failed to open UDPdataExchanger_ReubenPython3ClassObject.")
                ExitProgram_Callback()
            #################################################

        except:
            exceptions = sys.exc_info()[0]
            print("UDPdataExchanger_ReubenPython3ClassObject __init__, exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################

    #################################################
    #################################################

    #################################################
    #################################################
    global CSVdataLogger_ReubenPython3ClassObject_GUIparametersDict
    CSVdataLogger_ReubenPython3ClassObject_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_CSVdataLogger_FLAG),
                                    ("root", Tab_CSVdataLogger),
                                    ("EnableInternal_MyPrint_Flag", 1),
                                    ("NumberOfPrintLines", 10),
                                    ("UseBorderAroundThisGuiObjectFlag", 0),
                                    ("GUI_ROW", GUI_ROW_CSVdataLogger),
                                    ("GUI_COLUMN", GUI_COLUMN_CSVdataLogger),
                                    ("GUI_PADX", GUI_PADX_CSVdataLogger),
                                    ("GUI_PADY", GUI_PADY_CSVdataLogger),
                                    ("GUI_ROWSPAN", GUI_ROWSPAN_CSVdataLogger),
                                    ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_CSVdataLogger)])
    #################################################

    #################################################
    CSVdataLogger_ReubenPython3ClassObject_setup_dict_VariableNamesForHeaderList = ["Time (S)",
                                                                                    "Data"]

    print("CSVdataLogger_ReubenPython3ClassObject_setup_dict_VariableNamesForHeaderList: " + str(CSVdataLogger_ReubenPython3ClassObject_setup_dict_VariableNamesForHeaderList))
    #################################################

    #################################################
    global CSVdataLogger_ReubenPython3ClassObject_setup_dict
    CSVdataLogger_ReubenPython3ClassObject_setup_dict = dict([("GUIparametersDict", CSVdataLogger_ReubenPython3ClassObject_GUIparametersDict),
                                                                ("NameToDisplay_UserSet", "CSVdataLogger"),
                                                                ("CSVfile_DirectoryPath", os.getcwd() + "\\CSVfiles"),
                                                                ("FileNamePrefix", "CSV_file_"),
                                                                ("VariableNamesForHeaderList", CSVdataLogger_ReubenPython3ClassObject_setup_dict_VariableNamesForHeaderList),
                                                                ("MainThread_TimeToSleepEachLoop", 0.002),
                                                                ("SaveOnStartupFlag", 0)])

    if USE_CSVdataLogger_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            CSVdataLogger_ReubenPython3ClassObject = CSVdataLogger_ReubenPython3Class(CSVdataLogger_ReubenPython3ClassObject_setup_dict)
            CSVdataLogger_OPEN_FLAG = CSVdataLogger_ReubenPython3ClassObject.OBJECT_CREATED_SUCCESSFULLY_FLAG

            #################################################
            if CSVdataLogger_OPEN_FLAG != 1:
                print("Failed to open CSVdataLogger_ReubenPython3ClassObject.")
                ExitProgram_Callback()
            #################################################

        except:
            exceptions = sys.exc_info()[0]
            print("CSVdataLogger_ReubenPython3ClassObject __init__: Exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    global MyPrint_ReubenPython2and3ClassObject_GUIparametersDict
    MyPrint_ReubenPython2and3ClassObject_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_MyPrint_FLAG),
                                                                    ("root", Tab_MyPrint),
                                                                    ("UseBorderAroundThisGuiObjectFlag", 0),
                                                                    ("GUI_ROW", GUI_ROW_MyPrint),
                                                                    ("GUI_COLUMN", GUI_COLUMN_MyPrint),
                                                                    ("GUI_PADX", GUI_PADX_MyPrint),
                                                                    ("GUI_PADY", GUI_PADY_MyPrint),
                                                                    ("GUI_ROWSPAN", GUI_ROWSPAN_MyPrint),
                                                                    ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_MyPrint)])

    global MyPrint_ReubenPython2and3ClassObject_setup_dict
    MyPrint_ReubenPython2and3ClassObject_setup_dict = dict([("NumberOfPrintLines", 10),
                                                            ("WidthOfPrintingLabel", 200),
                                                            ("PrintToConsoleFlag", 1),
                                                            ("LogFileNameFullPath", os.getcwd() + "//TestLog.txt"),
                                                            ("GUIparametersDict", MyPrint_ReubenPython2and3ClassObject_GUIparametersDict)])

    if USE_MyPrint_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            MyPrint_ReubenPython2and3ClassObject = MyPrint_ReubenPython2and3Class(MyPrint_ReubenPython2and3ClassObject_setup_dict)
            MyPrint_OPEN_FLAG = MyPrint_ReubenPython2and3ClassObject.OBJECT_CREATED_SUCCESSFULLY_FLAG

            #################################################
            if MyPrint_OPEN_FLAG != 1:
                print("Failed to open MyPrint_ReubenPython2and3ClassObject.")
                ExitProgram_Callback()
            #################################################

        except:
            exceptions = sys.exc_info()[0]
            print("MyPrint_ReubenPython2and3ClassObject __init__: Exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################

    #################################################
    if UDP_RxOrTxRole == "tx":
        USE_MyPlotterPureTkinterStandAloneProcess_FLAG = 0
    #################################################

    global MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_NameList
    MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_NameList = ["Channel0", "Channel1", "Channel2", "Channel3", "Channel4", "Channel5"]

    global MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_ColorList
    MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_ColorList = ["Red", "Green", "Blue", "Black", "Purple", "Orange"]

    global MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_GUIparametersDict
    MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_GUIparametersDict = dict([("EnableInternal_MyPrint_Flag", 1),
                                                                                                ("NumberOfPrintLines", 10),
                                                                                                ("UseBorderAroundThisGuiObjectFlag", 0),
                                                                                                ("GraphCanvasWidth", 890),
                                                                                                ("GraphCanvasHeight", 700),
                                                                                                ("GraphCanvasWindowStartingX", 0),
                                                                                                ("GraphCanvasWindowStartingY", 0),
                                                                                                ("GUI_RootAfterCalNmackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents", 20)])

    global MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_setup_dict
    MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_setup_dict = dict([("GUIparametersDict", MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_GUIparametersDict),
                                                                                        ("ParentPID", os.getpid()),
                                                                                        ("WatchdogTimerExpirationDurationSeconds_StandAlonePlottingProcess", 5.0),
                                                                                        ("MarkerSize", 3),
                                                                                        ("CurvesToPlotNamesAndColorsDictOfLists",
                                                                                            dict([("NameList", MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_NameList),
                                                                                                  ("ColorList", MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_ColorList)])),
                                                                                        ("NumberOfDataPointToPlot", 50),
                                                                                        ("XaxisNumberOfTickMarks", 10),
                                                                                        ("YaxisNumberOfTickMarks", 10),
                                                                                        ("XaxisNumberOfDecimalPlacesForLabels", 3),
                                                                                        ("YaxisNumberOfDecimalPlacesForLabels", 3),
                                                                                        ("XaxisAutoscaleFlag", 1),
                                                                                        ("YaxisAutoscaleFlag", 1),
                                                                                        ("X_min", 0.0),
                                                                                        ("X_max", 20.0),
                                                                                        ("Y_min", -0.0015),
                                                                                        ("Y_max", 0.0015),
                                                                                        ("XaxisDrawnAtBottomOfGraph", 0),
                                                                                        ("XaxisLabelString", "Time (sec)"),
                                                                                        ("YaxisLabelString", "Y-units (units)"),
                                                                                        ("ShowLegendFlag", 1)])

    if USE_MyPlotterPureTkinterStandAloneProcess_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class(MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_setup_dict)
            MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject.OBJECT_CREATED_SUCCESSFULLY_FLAG

            #################################################
            if MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG != 1:
                print("Failed to open MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject.")
                ExitProgram_Callback()
            #################################################

        except:
            exceptions = sys.exc_info()[0]
            print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject, exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_KEYBOARD_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        keyboard.on_press_key("esc", ExitProgram_Callback)

        if UDP_RxOrTxRole == "tx":
            keyboard.on_press_key("w", IncrementTestFloat_Callback)
            keyboard.on_press_key("x", DecrementTestFloat_Callback)
    #################################################
    #################################################

    #################################################
    #################################################
    if EXIT_PROGRAM_FLAG == 0:
        print("Starting main loop 'test_program_for_UDPdataExchanger_ReubenPython3Class.")
        StartingTime_MainLoopThread = getPreciseSecondsTimeStampString()
    #################################################
    #################################################

    #################################################
    #################################################
    #################################################
    #################################################
    while(EXIT_PROGRAM_FLAG == 0):

        try:
            ################################################### GET's
            ###################################################
            ###################################################
            CurrentTime_MainLoopThread = getPreciseSecondsTimeStampString() - StartingTime_MainLoopThread
            ###################################################
            ###################################################
            ###################################################

            ################################################### GET's
            ###################################################
            ###################################################
            if UDPdataExchanger_OPEN_FLAG == 1:

                UDPdataExchanger_MostRecentDict = UDPdataExchanger_Object.GetMostRecentDataDict()
                #print("UDPdataExchanger_MostRecentDict: " + str(UDPdataExchanger_MostRecentDict))

                if "MostRecentMessage_Rx_Dict" in UDPdataExchanger_MostRecentDict:

                    if "TestTime" in UDPdataExchanger_MostRecentDict["MostRecentMessage_Rx_Dict"]:
                        UDPdataExchanger_MostRecentDict_TestTime = UDPdataExchanger_MostRecentDict["MostRecentMessage_Rx_Dict"]["TestTime"]

                    if "TestFloat" in UDPdataExchanger_MostRecentDict["MostRecentMessage_Rx_Dict"]:
                        UDPdataExchanger_MostRecentDict_TestFloat = UDPdataExchanger_MostRecentDict["MostRecentMessage_Rx_Dict"]["TestFloat"]
            ###################################################
            ###################################################
            ###################################################

            ################################################### SET's
            ###################################################
            ###################################################
            if UDPdataExchanger_OPEN_FLAG == 1:
                if UDP_RxOrTxRole == "tx":

                    ###################################################
                    ###################################################
                    if USE_SinusoidalMotionInput_FLAG == 1:
                        TestFloatToTx = TestFloatToTx_CallbackOffset + (SinusoidalInput_MaxValue + SinusoidalInput_MinValue)/2.0 + 0.5*abs(SinusoidalInput_MaxValue - SinusoidalInput_MinValue)*math.sin(SinusoidalInput_TimeGain*CurrentTime_MainLoopThread)
                    else:
                        TestFloatToTx = TestFloatToTx_CallbackOffset
                    ###################################################
                    ###################################################

                    UDPdataExchanger_Object.SendDictFromExternalProgram(dict([("TestFloat", TestFloatToTx),("TestTime", CurrentTime_MainLoopThread)]))
            ###################################################
            ###################################################
            ###################################################

            ################################################### SET's
            ###################################################
            ###################################################
            if UDPdataExchanger_OPEN_FLAG == 1 and CSVdataLogger_OPEN_FLAG == 1:

                ###################################################
                ###################################################
                ListToWrite = []
                ListToWrite.append(CurrentTime_MainLoopThread)

                ###################################################
                if "Time" in UDPdataExchanger_MostRecentDict:
                    ListToWrite.append(UDPdataExchanger_MostRecentDict["Time"])
                ###################################################

                ###################################################
                ###################################################

                CSVdataLogger_ReubenPython3ClassObject.AddDataToCSVfile_ExternalFunctionCall(ListToWrite)
            ###################################################
            ###################################################
            ###################################################

            ################################################### SET's
            ###################################################
            ###################################################
            if MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG == 1:

                ###################################################
                ###################################################
                MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject.GetMostRecentDataDict()

                if "StandAlonePlottingProcess_ReadyForWritingFlag" in MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict:
                    MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict["StandAlonePlottingProcess_ReadyForWritingFlag"]

                    if MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag == 1:
                        if CurrentTime_MainLoopThread - LastTime_MainLoopThread_MyPlotterPureTkinterStandAloneProcess >= 0.030:

                            MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject.ExternalAddPointOrListOfPointsToPlot(MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_NameList[0],
                                                                                                            [UDPdataExchanger_MostRecentDict_TestTime]*1,
                                                                                                            [UDPdataExchanger_MostRecentDict_TestFloat])


                            LastTime_MainLoopThread_MyPlotterPureTkinterStandAloneProcess = CurrentTime_MainLoopThread
                ###################################################
                ###################################################

            ###################################################
            ###################################################
            ###################################################

            time.sleep(0.030)

        except:
            exceptions = sys.exc_info()[0]
            print("test_program_for_UDPdataExchanger_ReubenPython3Class, exceptions: %s" % exceptions)
            traceback.print_exc()

    #################################################
    #################################################
    #################################################
    #################################################

    ################################################# THIS IS THE EXIT ROUTINE!
    #################################################
    #################################################
    #################################################
    print("Exiting main program 'test_program_for_UDPdataExchanger_ReubenPython3Class.")

    #################################################
    if UDPdataExchanger_OPEN_FLAG == 1:
        UDPdataExchanger_Object.ExitProgram_Callback()
    #################################################

    #################################################
    if MyPrint_OPEN_FLAG == 1:
        MyPrint_ReubenPython2and3ClassObject.ExitProgram_Callback()
    #################################################

    #################################################
    if CSVdataLogger_OPEN_FLAG == 1:
        CSVdataLogger_ReubenPython3ClassObject.ExitProgram_Callback()
    #################################################

    #################################################
    if MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG == 1:
        MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject.ExitProgram_Callback()
    #################################################

    #################################################
    #################################################
    #################################################
    #################################################

##########################################################################################################
##########################################################################################################