# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision G, 12/22/2025

Verified working on: Python 3.11/12/13 for Windows 10/11 64-bit and Raspberry Pi Bookworm.
'''

__author__ = 'reuben.brewer'

##########################################################################################################
##########################################################################################################

##########################################
import ReubenGithubCodeModulePaths #Replaces the need to have "ReubenGithubCodeModulePaths.pth" within "C:\Anaconda3\Lib\site-packages".
ReubenGithubCodeModulePaths.Enable()
##########################################

##########################################
from LowPassFilterForDictsOfLists_ReubenPython2and3Class import *
##########################################

##########################################
import os
import sys
import platform
import time
import datetime
import collections
from copy import * #for deepcopy
import inspect #To enable 'TellWhichFileWereIn'
import threading
import traceback
import socket
##########################################

########################################## https://stackoverflow.com/questions/54370322/how-to-limit-the-number-of-float-digits-jsonencoder-produces
##########################################
import json

##########################################
class RoundingFloat(float):
    K = 3
    __repr__ = staticmethod(lambda x, N=K: format(x, '.' + str(N) + 'f'))
##########################################

##########################################
json.encoder.c_make_encoder = None
if hasattr(json.encoder, 'FLOAT_REPR'):
    json.encoder.FLOAT_REPR = RoundingFloat.__repr__ #Python 2
else:
    json.encoder.float = RoundingFloat #Python 3
##########################################

##########################################
##########################################

##########################################
from tkinter import *
import tkinter.font as tkFont
from tkinter import ttk
##########################################

##########################################
import queue as Queue
##########################################

##########################################
import platform
if platform.system() == "Windows":
    import ctypes
    winmm = ctypes.WinDLL('winmm')
    winmm.timeBeginPeriod(1) #Set minimum timer resolution to 1ms so that time.sleep(0.001) behaves properly.
##########################################

##########################################################################################################
##########################################################################################################

class UDPdataExchanger_ReubenPython3Class(Frame): #Subclass the Tkinter Frame

    ##########################################################################################################
    ##########################################################################################################
    def __init__(self, SetupDict): #Subclass the Tkinter Frame

        print("#################### UDPdataExchanger_ReubenPython3Class __init__ starting. ####################")

        #########################################################
        #########################################################
        self.PrintAllReceivedSerialMessageForDebuggingFlag = 0 #unicorn

        self.EXIT_PROGRAM_FLAG = 0
        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0
        self.EnableInternal_MyPrint_Flag = 0
        self.MainThread_still_running_flag = 0
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.CurrentTime_CalculatedFromMainThread = -11111.0
        self.LastTime_CalculatedFromMainThread = -11111.0
        self.StartingTime_CalculatedFromMainThread = -11111.0
        self.DataStreamingFrequency_CalculatedFromMainThread = -11111.0
        self.DataStreamingDeltaT_CalculatedFromMainThread = -11111.0
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.UDP_PortIsOpenFlag = 0
        self.UDP_TimeoutCounter = 0

        self.UDP_RxPacketsReceivedCounter = 0
        self.UDP_TxPacketsTransmittedCounter = 0

        self.UDP_RxLastTimePacketWasReceived = 0.0
        self.WatchdogTimerExpirationState = 0
        self.TimeSinceWatchdogWasKicked = 0.0

        self.DataStream_State = 1 #Starts out communicating data

        self.ToggleDataStreamOnOrOff_EventNeedsToBeFiredFlag = 0

        self.JSONstringToTx_Queue = Queue.Queue()
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.MostRecentDataDict = dict()

        self.MostRecentDataDict["UDP_TxPacketsTransmittedCounter"] = self.UDP_TxPacketsTransmittedCounter
        self.MostRecentDataDict["UDP_RxPacketsReceivedCounter"] = self.UDP_RxPacketsReceivedCounter
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if platform.system() == "Linux":

            if "raspberrypi" in platform.uname(): #os.uname() doesn't work in windows
                self.my_platform = "pi"
            else:
                self.my_platform = "linux"

        elif platform.system() == "Windows":
            self.my_platform = "windows"

        elif platform.system() == "Darwin":
            self.my_platform = "mac"

        else:
            self.my_platform = "other"

        print("UDPdataExchanger_ReubenPython3Class __init__: The OS platform is: " + self.my_platform)
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "GUIparametersDict" in SetupDict:
            self.GUIparametersDict = SetupDict["GUIparametersDict"]

            #########################################################
            #########################################################
            if "USE_GUI_FLAG" in self.GUIparametersDict:
                self.USE_GUI_FLAG = self.PassThrough0and1values_ExitProgramOtherwise("USE_GUI_FLAG", self.GUIparametersDict["USE_GUI_FLAG"])
            else:
                self.USE_GUI_FLAG = 0

            print("UDPdataExchanger_ReubenPython3Class __init__: USE_GUI_FLAG: " + str(self.USE_GUI_FLAG))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "EnableInternal_MyPrint_Flag" in self.GUIparametersDict:
                self.EnableInternal_MyPrint_Flag = self.PassThrough0and1values_ExitProgramOtherwise("EnableInternal_MyPrint_Flag", self.GUIparametersDict["EnableInternal_MyPrint_Flag"])
            else:
                self.EnableInternal_MyPrint_Flag = 0

            print("UDPdataExchanger_ReubenPython3Class __init__: EnableInternal_MyPrint_Flag: " + str(self.EnableInternal_MyPrint_Flag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "PrintToConsoleFlag" in self.GUIparametersDict:
                self.PrintToConsoleFlag = self.PassThrough0and1values_ExitProgramOtherwise("PrintToConsoleFlag", self.GUIparametersDict["PrintToConsoleFlag"])
            else:
                self.PrintToConsoleFlag = 1

            print("UDPdataExchanger_ReubenPython3Class __init__: PrintToConsoleFlag: " + str(self.PrintToConsoleFlag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "NumberOfPrintLines" in self.GUIparametersDict:
                self.NumberOfPrintLines = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("NumberOfPrintLines", self.GUIparametersDict["NumberOfPrintLines"], 0.0, 50.0))
            else:
                self.NumberOfPrintLines = 10

            print("UDPdataExchanger_ReubenPython3Class __init__: NumberOfPrintLines: " + str(self.NumberOfPrintLines))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "UseBorderAroundThisGuiObjectFlag" in self.GUIparametersDict:
                self.UseBorderAroundThisGuiObjectFlag = self.PassThrough0and1values_ExitProgramOtherwise("UseBorderAroundThisGuiObjectFlag", self.GUIparametersDict["UseBorderAroundThisGuiObjectFlag"])
            else:
                self.UseBorderAroundThisGuiObjectFlag = 0

            print("UDPdataExchanger_ReubenPython3Class __init__: UseBorderAroundThisGuiObjectFlag: " + str(self.UseBorderAroundThisGuiObjectFlag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_ROW" in self.GUIparametersDict:
                self.GUI_ROW = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROW", self.GUIparametersDict["GUI_ROW"], 0.0, 1000.0))
            else:
                self.GUI_ROW = 0

            print("UDPdataExchanger_ReubenPython3Class __init__: GUI_ROW: " + str(self.GUI_ROW))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_COLUMN" in self.GUIparametersDict:
                self.GUI_COLUMN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMN", self.GUIparametersDict["GUI_COLUMN"], 0.0, 1000.0))
            else:
                self.GUI_COLUMN = 0

            print("UDPdataExchanger_ReubenPython3Class __init__: GUI_COLUMN: " + str(self.GUI_COLUMN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_PADX" in self.GUIparametersDict:
                self.GUI_PADX = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADX", self.GUIparametersDict["GUI_PADX"], 0.0, 1000.0))
            else:
                self.GUI_PADX = 0

            print("UDPdataExchanger_ReubenPython3Class __init__: GUI_PADX: " + str(self.GUI_PADX))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_PADY" in self.GUIparametersDict:
                self.GUI_PADY = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADY", self.GUIparametersDict["GUI_PADY"], 0.0, 1000.0))
            else:
                self.GUI_PADY = 0

            print("UDPdataExchanger_ReubenPython3Class __init__: GUI_PADY: " + str(self.GUI_PADY))
            #########################################################
            #########################################################

            ##########################################
            if "GUI_ROWSPAN" in self.GUIparametersDict:
                self.GUI_ROWSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROWSPAN", self.GUIparametersDict["GUI_ROWSPAN"], 1.0, 1000.0))
            else:
                self.GUI_ROWSPAN = 1

            print("UDPdataExchanger_ReubenPython3Class __init__: GUI_ROWSPAN: " + str(self.GUI_ROWSPAN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_COLUMNSPAN" in self.GUIparametersDict:
                self.GUI_COLUMNSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMNSPAN", self.GUIparametersDict["GUI_COLUMNSPAN"], 1.0, 1000.0))
            else:
                self.GUI_COLUMNSPAN = 1

            print("UDPdataExchanger_ReubenPython3Class __init__: GUI_COLUMNSPAN: " + str(self.GUI_COLUMNSPAN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_STICKY" in self.GUIparametersDict:
                self.GUI_STICKY = str(self.GUIparametersDict["GUI_STICKY"])
            else:
                self.GUI_STICKY = "w"

            print("UDPdataExchanger_ReubenPython3Class __init__: GUI_STICKY: " + str(self.GUI_STICKY))
            #########################################################
            #########################################################

        else:
            self.GUIparametersDict = dict()
            self.USE_GUI_FLAG = 0
            print("UDPdataExchanger_ReubenPython3Class __init__: No GUIparametersDict present, setting USE_GUI_FLAG: " + str(self.USE_GUI_FLAG))

        #print("UDPdataExchanger_ReubenPython3Class __init__: GUIparametersDict: " + str(self.GUIparametersDict))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "NameToDisplay_UserSet" in SetupDict:
            self.NameToDisplay_UserSet = str(SetupDict["NameToDisplay_UserSet"])
        else:
            self.NameToDisplay_UserSet = ""

        print("UDPdataExchanger_ReubenPython3Class __init__: NameToDisplay_UserSet" + str(self.NameToDisplay_UserSet))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "WatchdogTimerExpirationDurationSeconds" in SetupDict:
            self.WatchdogTimerExpirationDurationSeconds = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("WatchdogTimerExpirationDurationSeconds", SetupDict["WatchdogTimerExpirationDurationSeconds"], 0.000, 100000.0)

        else:
            self.WatchdogTimerExpirationDurationSeconds = 0.25

        print("UDPdataExchanger_ReubenPython3Class __init__: WatchdogTimerExpirationDurationSeconds: " + str(self.WatchdogTimerExpirationDurationSeconds))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        SuccessFlag = self.UpdateSetupDictParameters(SetupDict)
        if SuccessFlag != 1:
            print("UDPdataExchanger_ReubenPython3Class __init__: UpdateSetupDictParameters() failed.")
            return
        #########################################################
        #########################################################

        #########################################################
        #########################################################

        #########################################################
        #new_filtered_value = k * raw_sensor_value + (1 - k) * old_filtered_value
        self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject_DictOfVariableFilterSettings = dict([("DataStreamingFrequency_CalculatedFromMainThread", dict([("UseMedianFilterFlag", 0), ("UseExponentialSmoothingFilterFlag", 1),("ExponentialSmoothingFilterLambda", 0.05)]))])

        self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject_SetupDict = dict([("DictOfVariableFilterSettings", self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject_DictOfVariableFilterSettings)])

        self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject = LowPassFilterForDictsOfLists_ReubenPython2and3Class(self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject_SetupDict)
        self.LOWPASSFILTER_OPEN_FLAG = self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject.OBJECT_CREATED_SUCCESSFULLY_FLAG
        #########################################################

        #########################################################
        if self.LOWPASSFILTER_OPEN_FLAG != 1:
            print("UDPdataExchanger_ReubenPython3Class __init__: Failed to open LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject.")
            return
        #########################################################

        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.PrintToGui_Label_TextInputHistory_List = [" "]*self.NumberOfPrintLines
        self.PrintToGui_Label_TextInput_Str = ""
        self.GUI_ready_to_be_updated_flag = 0
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        try:
            self.MostRecentDataDict["UDP_RxOrTxRole"] = self.UDP_RxOrTxRole

            self.OpenUDPsocket()

        except:
            exceptions = sys.exc_info()[0]
            print("UDPdataExchanger_ReubenPython3Class __init__: Exceptions: %s" % exceptions)
            traceback.print_exc()
            return
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.MainThread_ThreadingObject = threading.Thread(target=self.MainThread, args=())
        self.MainThread_ThreadingObject.start()
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 1
        #########################################################
        #########################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateSetupDictParameters(self, SetupDict):

        #########################################################
        #########################################################
        if "UDP_RxOrTxRole" in SetupDict:
            self.UDP_RxOrTxRole = str(SetupDict["UDP_RxOrTxRole"]).lower()

            if self.UDP_RxOrTxRole not in ["rx", "tx"]:
                print("UDPdataExchanger_ReubenPython3Class __init__: Error: UDP_RxOrTxRole must be 'rx' or 'tx'.")
                return 0

        else:
            self.UDP_RxOrTxRole = "rx"

        print("UDPdataExchanger_ReubenPython3Class __init__: UDP_RxOrTxRole: " + str(self.UDP_RxOrTxRole))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "IPV4_address" in SetupDict:
            self.IPV4_address = str(SetupDict["IPV4_address"])

        else:
            self.IPV4_address = "127.0.0.1"

        print("UDPdataExchanger_ReubenPython3Class __init__: IPV4_address: " + str(self.IPV4_address))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "IPV4_Port" in SetupDict:
            self.IPV4_Port = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("IPV4_Port", SetupDict["IPV4_Port"], 1, 65535)) #port 0 doesn't work

        else:
            self.IPV4_Port = 1

        print("UDPdataExchanger_ReubenPython3Class __init__: IPV4_Port: " + str(self.IPV4_Port))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "UDP_BufferSizeInBytes" in SetupDict:
            self.UDP_BufferSizeInBytes = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("UDP_BufferSizeInBytes", SetupDict["UDP_BufferSizeInBytes"], 1, 1500)) #Max-packet-size is 1500 in-practice (maximum transmission unit (MTU) to prevent packet-fragmenting), 65507 bytes in theory-only

        else:
            self.UDP_BufferSizeInBytes = 64

        print("UDPdataExchanger_ReubenPython3Class __init__: UDP_BufferSizeInBytes: " + str(self.UDP_BufferSizeInBytes))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "UDP_TimeoutAtPortLevelInSeconds" in SetupDict:
            self.UDP_TimeoutAtPortLevelInSeconds = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("UDP_TimeoutAtPortLevelInSeconds", SetupDict["UDP_TimeoutAtPortLevelInSeconds"], 0.0, 1000000.0)

        else:
            self.UDP_TimeoutAtPortLevelInSeconds = 1.0

        print("UDPdataExchanger_ReubenPython3Class __init__: UDP_TimeoutAtPortLevelInSeconds: " + str(self.UDP_TimeoutAtPortLevelInSeconds))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "MainThread_TimeToSleepEachLoop" in SetupDict:
            self.MainThread_TimeToSleepEachLoop = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("MainThread_TimeToSleepEachLoop", SetupDict["MainThread_TimeToSleepEachLoop"], 0.001, 100000)

        else:
            self.MainThread_TimeToSleepEachLoop = 0.002

        print("UDPdataExchanger_ReubenPython3Class __init__: MainThread_TimeToSleepEachLoop: " + str(self.MainThread_TimeToSleepEachLoop))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        return 1
        #########################################################
        #########################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def LimitNumber_IntOutputOnly(self, min_val, max_val, test_val):
        if test_val > max_val:
            test_val = max_val

        elif test_val < min_val:
            test_val = min_val

        else:
            test_val = test_val

        test_val = int(test_val)

        return test_val
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def LimitNumber_FloatOutputOnly(self, min_val, max_val, test_val):
        if test_val > max_val:
            test_val = max_val

        elif test_val < min_val:
            test_val = min_val

        else:
            test_val = test_val

        test_val = float(test_val)

        return test_val
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def PassThrough0and1values_ExitProgramOtherwise(self, InputNameString, InputNumber, ExitProgramIfFailureFlag=1):

        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            InputNumber_ConvertedToFloat = float(InputNumber)
            ##########################################################################################################

        except:

            ##########################################################################################################
            exceptions = sys.exc_info()[0]
            print("PassThrough0and1values_ExitProgramOtherwise Error. InputNumber must be a numerical value, Exceptions: %s" % exceptions)

            ##########################
            if ExitProgramIfFailureFlag == 1:
                sys.exit()
            else:
                return -1
            ##########################

            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            if InputNumber_ConvertedToFloat == 0.0 or InputNumber_ConvertedToFloat == 1.0:
                return InputNumber_ConvertedToFloat

            else:

                print("PassThrough0and1values_ExitProgramOtherwise Error. '" +
                      str(InputNameString) +
                      "' must be 0 or 1 (value was " +
                      str(InputNumber_ConvertedToFloat) +
                      ").")

                ##########################
                if ExitProgramIfFailureFlag == 1:
                    sys.exit()

                else:
                    return -1
                ##########################

            ##########################################################################################################

        except:

            ##########################################################################################################
            exceptions = sys.exc_info()[0]
            print("PassThrough0and1values_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)

            ##########################
            if ExitProgramIfFailureFlag == 1:
                sys.exit()
            else:
                return -1
            ##########################

            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def PassThroughFloatValuesInRange_ExitProgramOtherwise(self, InputNameString, InputNumber, RangeMinValue, RangeMaxValue, ExitProgramIfFailureFlag=1):

        ##########################################################################################################
        ##########################################################################################################
        try:
            ##########################################################################################################
            InputNumber_ConvertedToFloat = float(InputNumber)
            ##########################################################################################################

        except:
            ##########################################################################################################
            exceptions = sys.exc_info()[0]
            print("PassThroughFloatValuesInRange_ExitProgramOtherwise Error. InputNumber must be a float value, Exceptions: %s" % exceptions)
            traceback.print_exc()

            ##########################
            if ExitProgramIfFailureFlag == 1:
                sys.exit()
            else:
                return -11111.0
            ##########################

            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            InputNumber_ConvertedToFloat_Limited = self.LimitNumber_FloatOutputOnly(RangeMinValue, RangeMaxValue, InputNumber_ConvertedToFloat)

            if InputNumber_ConvertedToFloat_Limited != InputNumber_ConvertedToFloat:
                print("PassThroughFloatValuesInRange_ExitProgramOtherwise Error. '" +
                      str(InputNameString) +
                      "' must be in the range [" +
                      str(RangeMinValue) +
                      ", " +
                      str(RangeMaxValue) +
                      "] (value was " +
                      str(InputNumber_ConvertedToFloat) + ")")

                ##########################
                if ExitProgramIfFailureFlag == 1:
                    sys.exit()
                else:
                    return -11111.0
                ##########################

            else:
                return InputNumber_ConvertedToFloat_Limited
            ##########################################################################################################

        except:
            ##########################################################################################################
            exceptions = sys.exc_info()[0]
            print("PassThroughFloatValuesInRange_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)
            traceback.print_exc()

            ##########################
            if ExitProgramIfFailureFlag == 1:
                sys.exit()
            else:
                return -11111.0
            ##########################

            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TellWhichFileWereIn(self):

        #We used to use this method, but it gave us the root calling file, not the class calling file
        #absolute_file_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        #filename = absolute_file_path[absolute_file_path.rfind("\\") + 1:]

        frame = inspect.stack()[1]
        filename = frame[1][frame[1].rfind("\\") + 1:]
        filename = filename.replace(".py","")

        return filename
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def getPreciseSecondsTimeStampString(self):
        ts = time.time()

        return ts
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GetMostRecentDataDict(self):

        if self.EXIT_PROGRAM_FLAG == 0:

            return deepcopy(self.MostRecentDataDict) #deepcopy IS required as MostRecentDataDict contains lists.

        else:
            return dict()  # So that we're not returning variables during the close-down process.
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_MainThread_Filtered(self):

        try:
            self.DataStreamingDeltaT_CalculatedFromMainThread = self.CurrentTime_CalculatedFromMainThread - self.LastTime_CalculatedFromMainThread

            if self.DataStreamingDeltaT_CalculatedFromMainThread != 0.0:
                DataStreamingFrequency_CalculatedFromMainThread_TEMP = 1.0/self.DataStreamingDeltaT_CalculatedFromMainThread

                ResultsDict = self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject.AddDataDictFromExternalProgram(dict([("DataStreamingFrequency_CalculatedFromMainThread", DataStreamingFrequency_CalculatedFromMainThread_TEMP)]))
                self.DataStreamingFrequency_CalculatedFromMainThread = ResultsDict["DataStreamingFrequency_CalculatedFromMainThread"]["Filtered_MostRecentValuesList"][0]

            self.LastTime_CalculatedFromMainThread = self.CurrentTime_CalculatedFromMainThread
        except:
            exceptions = sys.exc_info()[0]
            print("UpdateFrequencyCalculation_MainThread_Filtered, Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ############################################################################################################
    ##########################################################################################################
    def ConvertDictToJSONstring(self, DictToConvert):

        JSONstring = ""

        try:
            if type(DictToConvert) == dict:
                JSONstring = json.dumps(DictToConvert, allow_nan=True)

            else:
                print("ConvertDictToJSONstring: Error, input must be a dictionary.")

        except:
            exceptions = sys.exc_info()[0]
            print("ConvertDictToJSONstring, exceptions: %s" % exceptions)

        return JSONstring
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ConvertJSONstringToDict(self, JSONstringToConvert):

        DictToConvert = dict()

        try:
            if type(JSONstringToConvert) == str:
                DictToConvert = json.loads(JSONstringToConvert)
            else:
                print("ConvertJSONstringToDict ERROR: Input must be a string.")
        except:
            exceptions = sys.exc_info()[0]
            print("ConvertJSONstringToDict, exceptions: %s" % exceptions)

        return DictToConvert
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def OpenUDPsocket(self):

        try:
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            if self.UDP_RxOrTxRole == "rx":

                self.UDP_SocketObject = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  #AF_INET for internet, SOCK_DGRAM for UDP
                self.UDP_SocketObject.bind((self.IPV4_address, self.IPV4_Port)) #bind() needed only on the client/Rx side, not on the server/Tx side.
            
                self.UDP_SocketObject.settimeout(self.UDP_TimeoutAtPortLevelInSeconds) #Without a timeout set, the while 1: loop will continue forever when the keyboard-press triggers a program exit.
            
                self.UDP_SocketObject.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.UDP_BufferSizeInBytes)

                print("OpenUDPsocket for Rx: UDP_SocketObject.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF): " + 
                      str(self.UDP_SocketObject.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)))

                self.UDP_PortIsOpenFlag = 1

                print("OpenUDPsocket success for role " + self.UDP_RxOrTxRole)

                return 1
            ##########################################################################################################

            ##########################################################################################################
            elif self.UDP_RxOrTxRole == "tx":
                
                self.UDP_SocketObject = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #AF_INET for internet, SOCK_DGRAM for UDP
    
                self.UDP_SocketObject.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, self.UDP_BufferSizeInBytes)
    
                print("OpenUDPsocket for Tx: UDP_SocketObject.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF): " +
                      str(self.UDP_SocketObject.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)))
    
                self.UDP_PortIsOpenFlag = 1

                print("OpenUDPsocket success for role " + self.UDP_RxOrTxRole)
    
                return 1
            ##########################################################################################################

            ##########################################################################################################
            else:
                return 0
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################

        except:

            ##########################################################################################################
            ##########################################################################################################
            self.UDP_PortIsOpenFlag = 0
            exceptions = sys.exc_info()[0]

            ########################
            for i in range(0, 10):
                print("@@@@@@@@@@ OpenUDPsocket for " + self.UDP_RxOrTxRole + ": VERIFY NETWORK SETTINGS, exceptions: %s" % exceptions)
            ########################

            traceback.print_exc()
            return 0
            ##########################################################################################################
            ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def CloseUDPsocket(self):

        try:
            self.UDP_SocketObject.close()

            return 1

        except:
            exceptions = sys.exc_info()[0]
            print("CloseUDPsocket, Exceptions: %s" % exceptions)

            return 0
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def RxUDPmessage(self, StringToTx, PrintDebuggingDataFlag = 0):

        ##########################################################################################################
        try:

            if self.IPV4_Port >= 1 and self.IPV4_Port <= 65535: #Can't be 0

                if self.UDP_PortIsOpenFlag == 1:

                    Rx_DataStr, Rx_IPV4addressOfSocketSendingThisData = self.UDP_SocketObject.recvfrom(self.UDP_BufferSizeInBytes)
                    Rx_DataStr = Rx_DataStr.decode('utf-8') #Python 3 requires .decode('utf-8') to be performed on data to get a normal string.

                    ####### If there is a timeout (no received data), then we won't proceed beyond this line!

                    self.UDP_RxPacketsReceivedCounter = self.UDP_RxPacketsReceivedCounter + 1
                    self.UDP_RxLastTimePacketWasReceived = self.getPreciseSecondsTimeStampString() - self.StartingTime_CalculatedFromMainThread

                    if PrintDebuggingDataFlag == 1:
                        print("RxUDPmessage: Received UDP data (from IPV4 = " + str(Rx_IPV4addressOfSocketSendingThisData) +"): "  + str(Rx_DataStr) + ", len = " + str(len(Rx_DataStr)))

                    self.MostRecentDataDict["MostRecentMessage_Rx_Str"] = Rx_DataStr

                    self.MostRecentDataDict["MostRecentMessage_Rx_Str_Length"] = len(Rx_DataStr)

                    Rx_DataDict = self.ConvertJSONstringToDict(Rx_DataStr)
                    self.MostRecentDataDict["MostRecentMessage_Rx_Dict"] = Rx_DataDict

                    self.MostRecentDataDict["MostRecentMessage_Rx_LocalTimeOfReceivingComputer"] = self.UDP_RxLastTimePacketWasReceived

                    self.MostRecentDataDict["UDP_RxPacketsReceivedCounter"] = self.UDP_RxPacketsReceivedCounter

                    return 1

                else:
                    if self.PrintAllReceivedSerialMessageForDebuggingFlag == 1:
                        print("RxUDPmessage Error: self.UDP_PortIsOpenFlag = 0.")
                    return 0

            else:
                print("RxUDPmessage Error: IPV4_Port must be in range [1, 65535].")
                return 0
        ##########################################################################################################

        ##########################################################################################################
        except:
            exceptions = sys.exc_info()[0]

            if str(exceptions).lower().find("timeout") == -1: #Only display non-UDP-timeout exceptions
                print("RxUDPmessage: exceptions: %s" % exceptions)
                traceback.print_exc()
            else:
                self.UDP_TimeoutCounter = self.UDP_TimeoutCounter + 1
                self.MostRecentDataDict["UDP_TimeoutCounter"] = self.UDP_TimeoutCounter
                return 0
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TxUDPmessage(self, StringToTx):

        try:

            if isinstance(StringToTx, str) == 1:

                if len(StringToTx) > 0:

                    if self.IPV4_Port >= 1 and self.IPV4_Port <= 65535: #Can't be 0

                        if self.UDP_PortIsOpenFlag == 1:

                            self.UDP_SocketObject.sendto(StringToTx.encode('utf-8'), (self.IPV4_address, self.IPV4_Port)) #Python 3 requires .encode('utf-8') to be performed on string.
                            self.UDP_TxPacketsTransmittedCounter = self.UDP_TxPacketsTransmittedCounter + 1

                            self.MostRecentDataDict["MostRecentMessage_Tx"] = StringToTx
                            self.MostRecentDataDict["MostRecentMessage_Tx_Length"] = len(StringToTx)
                            self.MostRecentDataDict["UDP_TxPacketsTransmittedCounter"] = self.UDP_TxPacketsTransmittedCounter

                            return 1

                        else:
                            print("TxUDPmessage Error: self.UDP_PortIsOpenFlag = 0.")
                            return 0

                    else:
                        print("TxUDPmessage Error: IPV4_Port must be in range [1, 65535].")
                        return 0

                else:
                    print("TxUDPmessage: Error, StringToTx was empty.")
                    return 0

            else:
                print("TxUDPmessage Error: StringToTx must be type str.")
                return 0

        except:
            exceptions = sys.exc_info()[0]
            print("TxUDPmessage: exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SendDictFromExternalProgram(self, InputDict):

        try:

            if self.UDP_RxOrTxRole == "tx":

                if isinstance(InputDict, dict) == 0:
                    print("TxDataFromExternalProgram: Error, InputDict must be type dict.")
                    return 0

                JSONstringToTx = self.ConvertDictToJSONstring(InputDict)

                self.JSONstringToTx_Queue.put(JSONstringToTx)

                return 1

            else:
                print("SendDictFromExternalProgram: Error, UDP_RxOrTxRole must be Tx.")
                return 0

        except:
            exceptions = sys.exc_info()[0]
            print("TxDataFromExternalProgram: exceptions: %s" % exceptions)
            traceback.print_exc()
            return 0

    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## unicorn
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def MainThread(self):

        self.MyPrint_WithoutLogFile("Started MainThread for UDPdataExchanger_ReubenPython3Class object.")
        self.MainThread_StillRunningFlag = 1

        self.StartingTime_CalculatedFromMainThread = self.getPreciseSecondsTimeStampString()
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        while self.EXIT_PROGRAM_FLAG == 0:

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            self.CurrentTime_CalculatedFromMainThread = self.getPreciseSecondsTimeStampString() - self.StartingTime_CalculatedFromMainThread
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

            ########################################################################################################## unicorn
            ##########################################################################################################
            if self.WatchdogTimerExpirationDurationSeconds > 0.0:

                ##########################################################################################################
                if self.UDP_RxOrTxRole == "rx": #No watchdog for tx

                    self.TimeSinceWatchdogWasKicked = self.CurrentTime_CalculatedFromMainThread - self.UDP_RxLastTimePacketWasReceived

                    if  self.TimeSinceWatchdogWasKicked >= self.WatchdogTimerExpirationDurationSeconds:
                        self.WatchdogTimerExpirationState = 1
                    else:
                        self.WatchdogTimerExpirationState = 0
                ##########################################################################################################

            else:
                self.WatchdogTimerExpirationState = 0
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            self.MostRecentDataDict["WatchdogTimerExpirationState"] = self.WatchdogTimerExpirationState
            self.MostRecentDataDict["TimeSinceWatchdogWasKicked"] = self.TimeSinceWatchdogWasKicked
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            if self.ToggleDataStreamOnOrOff_EventNeedsToBeFiredFlag == 1:

                if self.DataStream_State == 0:
                    self.DataStream_State = 1
                else:
                    self.DataStream_State = 0

                self.ToggleDataStreamOnOrOff_EventNeedsToBeFiredFlag = 0
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            try:

                ##########################################################################################################
                ##########################################################################################################
                if self.UDP_RxOrTxRole == "rx":

                    ##########################################################################################################
                    try:

                        if self.DataStream_State == 1:
                            self.RxUDPmessage(self.PrintAllReceivedSerialMessageForDebuggingFlag)

                    except:
                        exceptions = sys.exc_info()[0]
                        print("MainThread, message receiving section, Exceptions: %s" % exceptions)
                        traceback.print_exc()
                    ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                elif self.UDP_RxOrTxRole == "tx":

                    ##########################################################################################################
                    try:

                        if self.DataStream_State == 1:
                            if self.JSONstringToTx_Queue.qsize() > 0:
                                JSONstringToTx_LocalCopy = self.JSONstringToTx_Queue.get()

                                self.TxUDPmessage(JSONstringToTx_LocalCopy)

                    except:
                        exceptions = sys.exc_info()[0]
                        print("MainThread, message receiving section, Exceptions: %s" % exceptions)
                        traceback.print_exc()
                    ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                else:
                    pass
                ##########################################################################################################
                ##########################################################################################################

            except:
                exceptions = sys.exc_info()[0]
                print("UDPdataExchanger_ReubenPython3Class, MainThread, Inner Exceptions: %s" % exceptions)
                traceback.print_exc()

            ########################################################################################################## These should be outside of the queue and heartbeat
            ##########################################################################################################
            ##########################################################################################################

            ########################################################################################################## USE THE TIME.SLEEP() TO SET THE LOOP FREQUENCY
            ##########################################################################################################
            ##########################################################################################################
            self.UpdateFrequencyCalculation_MainThread_Filtered()

            self.MostRecentDataDict["Time"] = self.CurrentTime_CalculatedFromMainThread
            self.MostRecentDataDict["DataStreamingFrequency_CalculatedFromMainThread"] = self.DataStreamingFrequency_CalculatedFromMainThread

            if self.MainThread_TimeToSleepEachLoop > 0.0:
                if self.MainThread_TimeToSleepEachLoop > 0.001:
                    time.sleep(self.MainThread_TimeToSleepEachLoop - 0.001) #The "- 0.001" corrects for slight deviation from intended frequency due to other functions being called.
                else:
                    time.sleep(self.MainThread_TimeToSleepEachLoop)
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        try:

            self.CloseUDPsocket()
            self.MainThread_StillRunningFlag = 0
            print("Finished MainThread for UDPdataExchanger_ReubenPython3Class object.")

        except:
            exceptions = sys.exc_info()[0]
            print("UDPdataExchanger_ReubenPython3Class, MainThread, closing routine exceptions: %s" % exceptions)
            traceback.print_exc()
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ExitProgram_Callback(self):

        print("Exiting all threads for UDPdataExchanger_ReubenPython3Class object")

        self.EXIT_PROGRAM_FLAG = 1
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def CreateGUIobjects(self, TkinterParent):

        print("UDPdataExchanger_ReubenPython3Class, CreateGUIobjects fired!")

        #################################################
        #################################################
        self.root = TkinterParent
        self.parent = TkinterParent
        #################################################
        #################################################

        #################################################
        #################################################
        self.myFrame = Frame(self.root)

        if self.UseBorderAroundThisGuiObjectFlag == 1:
            self.myFrame["borderwidth"] = 2
            self.myFrame["relief"] = "ridge"

        self.myFrame.grid(row = self.GUI_ROW,
                          column = self.GUI_COLUMN,
                          padx = self.GUI_PADX,
                          pady = self.GUI_PADY,
                          rowspan = self.GUI_ROWSPAN,
                          columnspan= self.GUI_COLUMNSPAN,
                          sticky = self.GUI_STICKY)
        #################################################
        #################################################

        #################################################
        #################################################
        self.TKinter_LightGreenColor = '#%02x%02x%02x' % (150, 255, 150) #RGB
        self.TKinter_LightRedColor = '#%02x%02x%02x' % (255, 150, 150) #RGB
        self.TKinter_LightYellowColor = '#%02x%02x%02x' % (255, 255, 150)  # RGB
        self.TKinter_DefaultGrayColor = '#%02x%02x%02x' % (240, 240, 240)  # RGB
        #################################################
        #################################################
        #################################################

        #################################################
        #################################################
        self.DeviceInfo_Label = Label(self.myFrame, text="Device Info", width=50, font=("Helvetica", 12))
        self.DeviceInfo_Label["text"] = self.NameToDisplay_UserSet + \
                                        "\nRole = " + str(self.UDP_RxOrTxRole) + \
                                        "\nIPV4 = " + str(self.IPV4_address) + \
                                        "\nPort = " + str(self.IPV4_Port)

        self.DeviceInfo_Label.grid(row=0, column=0, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=1, rowspan=1)
        #################################################
        #################################################

        #################################################
        #################################################
        self.Data_Label = Label(self.myFrame, text="Data_Label", width=120)
        self.Data_Label.grid(row=1, column=0, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=1, rowspan=1)
        #################################################
        #################################################

        #################################################
        #################################################
        self.ButtonsFrame = Frame(self.myFrame)
        self.ButtonsFrame.grid(row = 2, column = 0, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=1, rowspan=1)
        #################################################
        #################################################

        #################################################
        #################################################
        self.ToggleDataStreamOnOrOff_Button = Button(self.ButtonsFrame, text="ToggleDataStreamOnOrOff_Button", state="normal", width=15, command=lambda: self.ToggleDataStreamOnOrOff_Button_Response())
        self.ToggleDataStreamOnOrOff_Button.grid(row=0, column=0, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=1, rowspan=1)
        #################################################
        #################################################

        #################################################
        #################################################
        self.PrintToGui_Label = Label(self.myFrame, text="PrintToGui_Label", width=75)
        if self.EnableInternal_MyPrint_Flag == 1:
            self.PrintToGui_Label.grid(row=3, column=0, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=10, rowspan=10)
        #################################################
        #################################################

        #################################################
        #################################################
        self.GUI_ready_to_be_updated_flag = 1
        #################################################
        #################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ToggleDataStreamOnOrOff_Button_Response(self):

        self.ToggleDataStreamOnOrOff_EventNeedsToBeFiredFlag = 1

        #self.MyPrint_WithoutLogFile("ToggleDataStreamOnOrOff_Button_Response: Event fired!")

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GUI_update_clock(self):

        #######################################################
        #######################################################
        #######################################################
        #######################################################
        if self.USE_GUI_FLAG == 1 and self.EXIT_PROGRAM_FLAG == 0:

            #######################################################
            #######################################################
            #######################################################
            if self.GUI_ready_to_be_updated_flag == 1:

                #######################################################
                #######################################################
                try:

                    #######################################################
                    self.Data_Label["text"] = self.ConvertDictToProperlyFormattedStringForPrinting(self.MostRecentDataDict,
                                                                                                    NumberOfDecimalsPlaceToUse = 5,
                                                                                                    NumberOfEntriesPerLine = 1,
                                                                                                    NumberOfTabsBetweenItems = 3)
                    #######################################################

                    #######################################################
                    if self.UDP_RxOrTxRole == "rx": #No watdhgo for tx
                        if self.WatchdogTimerExpirationState == 0:
                            self.Data_Label["bg"] = self.TKinter_LightGreenColor
                        else:
                            self.Data_Label["bg"] = self.TKinter_LightRedColor
                    #######################################################

                    #######################################################
                    self.ToggleDataStreamOnOrOff_Button["text"] = "Data Stream\n" + str(self.DataStream_State)

                    if self.DataStream_State == 1:
                        self.ToggleDataStreamOnOrOff_Button["bg"] = self.TKinter_LightGreenColor
                    else:
                        self.ToggleDataStreamOnOrOff_Button["bg"] = self.TKinter_LightRedColor
                    #######################################################

                    #######################################################
                    self.PrintToGui_Label.config(text=self.PrintToGui_Label_TextInput_Str)
                    #######################################################

                except:
                    exceptions = sys.exc_info()[0]
                    print("UDPdataExchanger_ReubenPython3Class GUI_update_clock ERROR: Exceptions: %s" % exceptions)
                    traceback.print_exc()
                #######################################################
                #######################################################

            #######################################################
            #######################################################
            #######################################################

        #######################################################
        #######################################################
        #######################################################
        #######################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def MyPrint_WithoutLogFile(self, input_string):

        input_string = str(input_string)

        if input_string != "":

            #input_string = input_string.replace("\n", "").replace("\r", "")

            ################################ Write to console
            # Some people said that print crashed for pyinstaller-built-applications and that sys.stdout.write fixed this.
            # http://stackoverflow.com/questions/13429924/pyinstaller-packaged-application-works-fine-in-console-mode-crashes-in-window-m
            if self.PrintToConsoleFlag == 1:
                sys.stdout.write(input_string + "\n")
            ################################

            ################################ Write to GUI
            self.PrintToGui_Label_TextInputHistory_List.append(self.PrintToGui_Label_TextInputHistory_List.pop(0)) #Shift the list
            self.PrintToGui_Label_TextInputHistory_List[-1] = str(input_string) #Add the latest value

            self.PrintToGui_Label_TextInput_Str = ""
            for Counter, Line in enumerate(self.PrintToGui_Label_TextInputHistory_List):
                self.PrintToGui_Label_TextInput_Str = self.PrintToGui_Label_TextInput_Str + Line

                if Counter < len(self.PrintToGui_Label_TextInputHistory_List) - 1:
                    self.PrintToGui_Label_TextInput_Str = self.PrintToGui_Label_TextInput_Str + "\n"
            ################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self, input, number_of_leading_numbers = 4, number_of_decimal_places = 3):

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
                    ListOfStringsToJoin.append(self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

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
                    ListOfStringsToJoin.append("TUPLE" + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

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
                    ListOfStringsToJoin.append(str(Key) + ": " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(input[Key], number_of_leading_numbers, number_of_decimal_places))

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

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ConvertDictToProperlyFormattedStringForPrinting(self, DictToPrint, NumberOfDecimalsPlaceToUse = 3, NumberOfEntriesPerLine = 1, NumberOfTabsBetweenItems = 3):

        ProperlyFormattedStringForPrinting = ""
        ItemsPerLineCounter = 0

        for Key in DictToPrint:

            ##########################################################################################################
            if isinstance(DictToPrint[Key], dict): #RECURSION
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                     Key + ":\n" + \
                                                     self.ConvertDictToProperlyFormattedStringForPrinting(DictToPrint[Key], NumberOfDecimalsPlaceToUse, NumberOfEntriesPerLine, NumberOfTabsBetweenItems)

            else:
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                     Key + ": " + \
                                                     self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(DictToPrint[Key], 0, NumberOfDecimalsPlaceToUse)
            ##########################################################################################################

            ##########################################################################################################
            if ItemsPerLineCounter < NumberOfEntriesPerLine - 1:
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\t"*NumberOfTabsBetweenItems
                ItemsPerLineCounter = ItemsPerLineCounter + 1
            else:
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\n"
                ItemsPerLineCounter = 0
            ##########################################################################################################

        return ProperlyFormattedStringForPrinting
    ##########################################################################################################
    ##########################################################################################################
