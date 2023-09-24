# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision E, 05/10/2023

Verified working on: Python 3.8 for Windows 8.1, 10 64-bit and Raspberry Pi Buster (may work on Mac in non-GUI mode, but haven't tested yet).
'''

__author__ = 'reuben.brewer'

###########################################################
from LowPassFilter_ReubenPython2and3Class import *
###########################################################

###########################################################
import os
import sys
import platform
import time
import datetime
import math
import collections
from copy import * #for deepcopy
import inspect #To enable 'TellWhichFileWereIn'
import threading
import traceback
###########################################################

###########################################################
from tkinter import *
import tkinter.font as tkFont
from tkinter import ttk
###########################################################

###########################################################
import queue as Queue
###########################################################

###########################################################
from future.builtins import input as input
########################################################### "sudo pip3 install future" (Python 3) AND "sudo pip install future" (Python 2)

###########################################################
import platform
if platform.system() == "Windows":
    import ctypes
    winmm = ctypes.WinDLL('winmm')
    winmm.timeBeginPeriod(1) #Set minimum timer resolution to 1ms so that time.sleep(0.001) behaves properly.
###########################################################

class CSVdataLogger_ReubenPython3Class(Frame): #Subclass the Tkinter Frame

    ##########################################################################################################
    ##########################################################################################################
    def __init__(self, setup_dict): #Subclass the Tkinter Frame

        print("#################### CSVdataLogger_ReubenPython3Class __init__ starting. ####################")

        #########################################################
        #########################################################
        self.EXIT_PROGRAM_FLAG = 0
        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0
        self.EnableInternal_MyPrint_Flag = 0
        self.MainThread_still_running_flag = 0

        self.CurrentTime_CalculatedFromMainThread = -11111.0
        self.StartingTime_CalculatedFromMainThread = -11111.0
        self.LastTime_CalculatedFromMainThread = -11111.0
        self.DataStreamingFrequency_CalculatedFromMainThread = -11111.0
        self.DataStreamingDeltaT_CalculatedFromMainThread = -11111.0

        self.CSVfile_SaveFlag = 0
        self.CSVfile_SaveFlag_NeedsToBeChangedFlag = 0
        self.AcceptNewDataFlag = 0
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

        print("CSVdataLogger_ReubenPython3Class __init__: The OS platform is: " + self.my_platform)
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "GUIparametersDict" in setup_dict:
            self.GUIparametersDict = setup_dict["GUIparametersDict"]

            #########################################################
            #########################################################
            if "USE_GUI_FLAG" in self.GUIparametersDict:
                self.USE_GUI_FLAG = self.PassThrough0and1values_ExitProgramOtherwise("USE_GUI_FLAG", self.GUIparametersDict["USE_GUI_FLAG"])
            else:
                self.USE_GUI_FLAG = 0

            print("CSVdataLogger_ReubenPython3Class __init__: USE_GUI_FLAG: " + str(self.USE_GUI_FLAG))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "root" in self.GUIparametersDict:
                self.root = self.GUIparametersDict["root"]
            else:
                print("CSVdataLogger_ReubenPython3Class __init__: Error, must pass in 'root'")
                return
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "EnableInternal_MyPrint_Flag" in self.GUIparametersDict:
                self.EnableInternal_MyPrint_Flag = self.PassThrough0and1values_ExitProgramOtherwise("EnableInternal_MyPrint_Flag", self.GUIparametersDict["EnableInternal_MyPrint_Flag"])
            else:
                self.EnableInternal_MyPrint_Flag = 0

            print("CSVdataLogger_ReubenPython3Class __init__: EnableInternal_MyPrint_Flag: " + str(self.EnableInternal_MyPrint_Flag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "PrintToConsoleFlag" in self.GUIparametersDict:
                self.PrintToConsoleFlag = self.PassThrough0and1values_ExitProgramOtherwise("PrintToConsoleFlag", self.GUIparametersDict["PrintToConsoleFlag"])
            else:
                self.PrintToConsoleFlag = 1

            print("CSVdataLogger_ReubenPython3Class __init__: PrintToConsoleFlag: " + str(self.PrintToConsoleFlag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "NumberOfPrintLines" in self.GUIparametersDict:
                self.NumberOfPrintLines = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("NumberOfPrintLines", self.GUIparametersDict["NumberOfPrintLines"], 0.0, 50.0))
            else:
                self.NumberOfPrintLines = 10

            print("CSVdataLogger_ReubenPython3Class __init__: NumberOfPrintLines: " + str(self.NumberOfPrintLines))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "UseBorderAroundThisGuiObjectFlag" in self.GUIparametersDict:
                self.UseBorderAroundThisGuiObjectFlag = self.PassThrough0and1values_ExitProgramOtherwise("UseBorderAroundThisGuiObjectFlag", self.GUIparametersDict["UseBorderAroundThisGuiObjectFlag"])
            else:
                self.UseBorderAroundThisGuiObjectFlag = 0

            print("CSVdataLogger_ReubenPython3Class __init__: UseBorderAroundThisGuiObjectFlag: " + str(self.UseBorderAroundThisGuiObjectFlag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_ROW" in self.GUIparametersDict:
                self.GUI_ROW = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROW", self.GUIparametersDict["GUI_ROW"], 0.0, 1000.0))
            else:
                self.GUI_ROW = 0

            print("CSVdataLogger_ReubenPython3Class __init__: GUI_ROW: " + str(self.GUI_ROW))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_COLUMN" in self.GUIparametersDict:
                self.GUI_COLUMN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMN", self.GUIparametersDict["GUI_COLUMN"], 0.0, 1000.0))
            else:
                self.GUI_COLUMN = 0

            print("CSVdataLogger_ReubenPython3Class __init__: GUI_COLUMN: " + str(self.GUI_COLUMN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_PADX" in self.GUIparametersDict:
                self.GUI_PADX = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADX", self.GUIparametersDict["GUI_PADX"], 0.0, 1000.0))
            else:
                self.GUI_PADX = 0

            print("CSVdataLogger_ReubenPython3Class __init__: GUI_PADX: " + str(self.GUI_PADX))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_PADY" in self.GUIparametersDict:
                self.GUI_PADY = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADY", self.GUIparametersDict["GUI_PADY"], 0.0, 1000.0))
            else:
                self.GUI_PADY = 0

            print("CSVdataLogger_ReubenPython3Class __init__: GUI_PADY: " + str(self.GUI_PADY))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_ROWSPAN" in self.GUIparametersDict:
                self.GUI_ROWSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROWSPAN", self.GUIparametersDict["GUI_ROWSPAN"], 1.0, 1000.0))
            else:
                self.GUI_ROWSPAN = 1

            print("CSVdataLogger_ReubenPython3Class __init__: GUI_ROWSPAN: " + str(self.GUI_ROWSPAN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_COLUMNSPAN" in self.GUIparametersDict:
                self.GUI_COLUMNSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMNSPAN", self.GUIparametersDict["GUI_COLUMNSPAN"], 1.0, 1000.0))
            else:
                self.GUI_COLUMNSPAN = 1

            print("CSVdataLogger_ReubenPython3Class __init__: GUI_COLUMNSPAN: " + str(self.GUI_COLUMNSPAN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_STICKY" in self.GUIparametersDict:
                self.GUI_STICKY = str(self.GUIparametersDict["GUI_STICKY"])
            else:
                self.GUI_STICKY = "w"

            print("CSVdataLogger_ReubenPython3Class __init__: GUI_STICKY: " + str(self.GUI_STICKY))
            #########################################################
            #########################################################

        else:
            self.GUIparametersDict = dict()
            self.USE_GUI_FLAG = 0
            print("CSVdataLogger_ReubenPython3Class __init__: No GUIparametersDict present, setting USE_GUI_FLAG: " + str(self.USE_GUI_FLAG))

        #print("CSVdataLogger_ReubenPython3Class __init__: GUIparametersDict: " + str(self.GUIparametersDict))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "NameToDisplay_UserSet" in setup_dict:
            self.NameToDisplay_UserSet = str(setup_dict["NameToDisplay_UserSet"])
        else:
            self.NameToDisplay_UserSet = ""

        print("CSVdataLogger_ReubenPython3Class __init__: NameToDisplay_UserSet: " + str(self.NameToDisplay_UserSet))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "CSVfile_DirectoryPath" in setup_dict:
            self.CSVfile_DirectoryPath = str(setup_dict["CSVfile_DirectoryPath"])
        else:
            self.CSVfile_DirectoryPath = os.getcwd()

        print("CSVdataLogger_ReubenPython3Class __init__: CSVfile_DirectoryPath: " + str(self.CSVfile_DirectoryPath))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "FileNamePrefix" in setup_dict:
            self.FileNamePrefix = str(setup_dict["FileNamePrefix"])
        else:
            self.FileNamePrefix = "CSVdataLogger_"

        print("CSVdataLogger_ReubenPython3Class __init__: FileNamePrefix: " + str(self.FileNamePrefix))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "VariableNamesForHeaderList" in setup_dict:
            VariableNamesForHeaderList_TEMP = setup_dict["VariableNamesForHeaderList"]

            self.VariableNamesForHeaderList = list()

            self.VariablesHeaderStringCommaDelimited = ""

            if isinstance(VariableNamesForHeaderList_TEMP, list) == 1:

                for index, VariableName in enumerate(VariableNamesForHeaderList_TEMP):
                    self.VariablesHeaderStringCommaDelimited = self.VariablesHeaderStringCommaDelimited + str(VariableName)
                    self.VariableNamesForHeaderList.append(str(VariableName))

                    ###################################################
                    if index < len(VariableNamesForHeaderList_TEMP) - 1:
                        self.VariablesHeaderStringCommaDelimited = self.VariablesHeaderStringCommaDelimited + ", "

                    else:
                        self.VariablesHeaderStringCommaDelimited = self.VariablesHeaderStringCommaDelimited + "\n"
                    ###################################################

            else:
                print("CSVdataLogger_ReubenPython3Class __init__: Error, 'VariableNamesForHeaderList' must be a list.")
                return

        else:
            print("CSVdataLogger_ReubenPython3Class __init__: Error, must input 'VariableNamesForHeaderList'")
            return

        print("CSVdataLogger_ReubenPython3Class __init__: VariableNamesForHeaderList: " + str(self.VariableNamesForHeaderList))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "MainThread_TimeToSleepEachLoop" in setup_dict:
            self.MainThread_TimeToSleepEachLoop = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("MainThread_TimeToSleepEachLoop", setup_dict["MainThread_TimeToSleepEachLoop"], 0.001, 100000)

        else:
            self.MainThread_TimeToSleepEachLoop = 0.005

        print("CSVdataLogger_ReubenPython3Class __init__: MainThread_TimeToSleepEachLoop: " + str(self.MainThread_TimeToSleepEachLoop))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "SaveOnStartupFlag" in setup_dict:
            self.SaveOnStartupFlag = self.PassThrough0and1values_ExitProgramOtherwise("SaveOnStartupFlag", setup_dict["SaveOnStartupFlag"])
        else:
            self.SaveOnStartupFlag = 0

        print("CSVdataLogger_ReubenPython3Class __init__: SaveOnStartupFlag: " + str(self.SaveOnStartupFlag))
        #########################################################
        #########################################################

        self.DataQueue = Queue.Queue()

        #########################################################
        #########################################################
        self.PrintToGui_Label_TextInputHistory_List = [" "]*self.NumberOfPrintLines
        self.PrintToGui_Label_TextInput_Str = ""
        self.GUI_ready_to_be_updated_flag = 0
        #########################################################
        #########################################################

        #########################################################
        ######################################################### DON'T NEED THIS WHEN THERE'S A CALLBACK AND NOTHING TO DO IN THE MainThread!
        self.MainThread_ThreadingObject = threading.Thread(target=self.MainThread, args=())
        self.MainThread_ThreadingObject.start()
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if self.USE_GUI_FLAG == 1:
            self.StartGUI(self.root)
        #########################################################
        #########################################################

        ######################################################### Give the Phidgets board a chance to open before sending commands to it.
        #########################################################
        time.sleep(0.25)
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
    def __del__(self):
        pass
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def PassThrough0and1values_ExitProgramOtherwise(self, InputNameString, InputNumber):

        try:
            InputNumber_ConvertedToFloat = float(InputNumber)
        except:
            exceptions = sys.exc_info()[0]
            print("PassThrough0and1values_ExitProgramOtherwise Error. InputNumber must be a float value, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()

        try:
            if InputNumber_ConvertedToFloat == 0.0 or InputNumber_ConvertedToFloat == 1:
                return InputNumber_ConvertedToFloat
            else:
                input("PassThrough0and1values_ExitProgramOtherwise Error. '" +
                          InputNameString +
                          "' must be 0 or 1 (value was " +
                          str(InputNumber_ConvertedToFloat) +
                          "). Press any key (and enter) to exit.")

                sys.exit()
        except:
            exceptions = sys.exc_info()[0]
            print("PassThrough0and1values_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def PassThroughFloatValuesInRange_ExitProgramOtherwise(self, InputNameString, InputNumber, RangeMinValue, RangeMaxValue):
        try:
            InputNumber_ConvertedToFloat = float(InputNumber)
        except:
            exceptions = sys.exc_info()[0]
            print("PassThroughFloatValuesInRange_ExitProgramOtherwise Error. InputNumber must be a float value, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()

        try:
            if InputNumber_ConvertedToFloat >= RangeMinValue and InputNumber_ConvertedToFloat <= RangeMaxValue:
                return InputNumber_ConvertedToFloat
            else:
                input("PassThroughFloatValuesInRange_ExitProgramOtherwise Error. '" +
                          InputNameString +
                          "' must be in the range [" +
                          str(RangeMinValue) +
                          ", " +
                          str(RangeMaxValue) +
                          "] (value was " +
                          str(InputNumber_ConvertedToFloat) + "). Press any key (and enter) to exit.")

                sys.exit()
        except:
            exceptions = sys.exc_info()[0]
            print("PassThroughFloatValuesInRange_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()
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
    def getTimeStampString(self):

        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%m_%d_%Y---%H_%M_%S')

        return st
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def IsSaving(self):

        return self.CSVfile_SaveFlag
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_MainThread(self):

        try:
            self.DataStreamingDeltaT_CalculatedFromMainThread = self.CurrentTime_CalculatedFromMainThread - self.LastTime_CalculatedFromMainThread

            if self.DataStreamingDeltaT_CalculatedFromMainThread != 0.0:
                self.DataStreamingFrequency_CalculatedFromMainThread = 1.0/self.DataStreamingDeltaT_CalculatedFromMainThread

            self.LastTime_CalculatedFromMainThread = self.CurrentTime_CalculatedFromMainThread
        except:
            exceptions = sys.exc_info()[0]
            print("UpdateFrequencyCalculation_MainThread ERROR with Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def CreateNewDirectoryIfItDoesntExist(self, directory):
        try:
            #print("CreateNewDirectoryIfItDoesntExist, directory: " + directory)
            if os.path.isdir(directory) == 0: #No directory with this name exists
                os.makedirs(directory)
        except:
            exceptions = sys.exc_info()[0]
            print("CreateNewDirectoryIfItDoesntExist, Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def CreateCSVfileAndStartWritingData(self, CSVfile_DirectoryPath_Input = "", FileNamePrefix_Input = ""):

        try:

            if CSVfile_DirectoryPath_Input != "":
                self.CSVfile_DirectoryPath = CSVfile_DirectoryPath_Input
                self.CreateNewDirectoryIfItDoesntExist(self.CSVfile_DirectoryPath)

            if FileNamePrefix_Input != "":
                self.FileNamePrefix = FileNamePrefix_Input

            self.CreateNewDirectoryIfItDoesntExist(self.CSVfile_DirectoryPath)

            self.CSVfile_FilepathFull = self.CSVfile_DirectoryPath + "//" + self.FileNamePrefix + self.getTimeStampString() + ".csv"

            self.CSVfile_FileObject = open(self.CSVfile_FilepathFull, "a") #Will append to file if it exists, create new file with this as first entry if file doesn't exist.
            self.CSVfile_FileObject.write(self.VariablesHeaderStringCommaDelimited + "\n")

            self.AcceptNewDataFlag = 1
            self.CSVfile_SaveFlag = 1

            print("CreateCSVfileAndStartWritingData: Opened file " + self.CSVfile_FilepathFull + " and started writing data!")

        except:
            exceptions = sys.exc_info()[0]
            print("CreateCSVfileAndStartWritingData, Exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def StopWritingDataAndCloseCSVfileImmediately(self):

        try:
            if self.CSVfile_SaveFlag == 1:

                self.AcceptNewDataFlag = 0
                self.CSVfile_SaveFlag = 0

                self.CSVfile_FileObject.close()

                print("CloseCSVfileAndStopWritingData: Closed file " + self.CSVfile_FilepathFull + " and stopped writing data!")

        except:
            exceptions = sys.exc_info()[0]
            print("CloseCSVfileAndStopWritingData, Exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __WriteLineToCSVfile_InternalFunctionCall(self, ListOfDataToWrite):

        try:

            if self.CSVfile_SaveFlag == 1:

                LineToWrite = ""

                ###################################################
                ###################################################
                for index, element in enumerate(ListOfDataToWrite):

                    ###################################################
                    if isinstance(element, list) == 1:
                        LineToWrite = LineToWrite + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, 0, 5).replace("[","").replace("]","")
                    else:
                        LineToWrite = LineToWrite + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, 0, 5)
                    ###################################################

                    ###################################################
                    if index < len(ListOfDataToWrite) -1:
                        LineToWrite = LineToWrite + ", "
                    else:
                        LineToWrite = LineToWrite + "\n"
                    ###################################################

                ###################################################
                ###################################################

                ###################################################
                ###################################################
                self.CSVfile_FileObject.write(LineToWrite)
                ###################################################
                ###################################################

        except:
            exceptions = sys.exc_info()[0]
            print("__WriteLineToCSVfile_InternalFunctionCall, Exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def AddDataToCSVfile_ExternalFunctionCall(self, ListOfDataToWrite):

        if self.AcceptNewDataFlag == 1:

            if isinstance(ListOfDataToWrite, list) == 1:

                if len(ListOfDataToWrite) == len(self.VariableNamesForHeaderList):
                    self.DataQueue.put(ListOfDataToWrite)

                else:
                    print("AddDataToCSVfile: ERROR,list is incorrect length.")

            else:

                print("AddDataToCSVfile: ERROR, input must be a list.")

    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## unicorn
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def MainThread(self):

        self.MyPrint_WithoutLogFile("Started MainThread for CSVdataLogger_ReubenPython3Class object.")

        self.MainThread_still_running_flag = 1

        if self.SaveOnStartupFlag == 1:
            self.CreateCSVfileAndStartWritingData()

        self.StartingTime_CalculatedFromMainThread = self.getPreciseSecondsTimeStampString()

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        while self.EXIT_PROGRAM_FLAG == 0:

            try:

                ##########################################################################################################
                ##########################################################################################################
                self.CurrentTime_CalculatedFromMainThread = self.getPreciseSecondsTimeStampString() - self.StartingTime_CalculatedFromMainThread
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                if self.CSVfile_SaveFlag_NeedsToBeChangedFlag == 1:

                    if self.DataQueue.qsize() == 0:
                        if self.CSVfile_SaveFlag == 1:  # Currently saving, need to close the file.
                            self.StopWritingDataAndCloseCSVfileImmediately()

                        else:  # Currently NOT saving, need to open the file.
                            self.CreateCSVfileAndStartWritingData()

                        self.CSVfile_SaveFlag_NeedsToBeChangedFlag = 0

                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                if self.CSVfile_SaveFlag == 1:

                    ##########################################################################################################
                    if self.DataQueue.qsize() > 0:

                        ###################################################
                        ListOfDataToWrite = self.DataQueue.get()

                        self.__WriteLineToCSVfile_InternalFunctionCall(ListOfDataToWrite)
                        ###################################################

                ##########################################################################################################

                ##########################################################################################################
                #else:

                #    ###################################################
                #    if self.EXIT_PROGRAM_FLAG == 0:
                #        break
                    ###################################################

                ##########################################################################################################

                ##########################################################################################################
                self.UpdateFrequencyCalculation_MainThread()

                if self.MainThread_TimeToSleepEachLoop > 0.0:
                    time.sleep(self.MainThread_TimeToSleepEachLoop)
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################

            except:
                exceptions = sys.exc_info()[0]
                print("CloseCSVfileAndStopWritingData, Exceptions: %s" % exceptions)
                traceback.print_exc()

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        self.StopWritingDataAndCloseCSVfileImmediately()

        self.MyPrint_WithoutLogFile("Finished MainThread for CSVdataLogger_ReubenPython3Class object.")

        self.MainThread_still_running_flag = 0
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ExitProgram_Callback(self):

        print("Exiting all threads for CSVdataLogger_ReubenPython3Class object")

        self.EXIT_PROGRAM_FLAG = 1
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def StartGUI(self, GuiParent):

        #self.GUI_Thread_ThreadingObject = threading.Thread(target=self.GUI_Thread, args=(GuiParent,))
        #self.GUI_Thread_ThreadingObject.setDaemon(True) #Should mean that the GUI thread is destroyed automatically when the main thread is destroyed.
        #self.GUI_Thread_ThreadingObject.start()

        self.GUI_Thread(GuiParent)
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GUI_Thread(self, parent):

        print("Starting the GUI_Thread for CSVdataLogger_ReubenPython3Class object.")

        #################################################
        #################################################
        self.root = parent
        self.parent = parent
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
        self.DeviceInfo_Label = Label(self.myFrame, text="Device Info", width=125)

        self.DeviceInfo_Label["text"] = self.NameToDisplay_UserSet

        self.DeviceInfo_Label.grid(row=0, column=0, padx=10, pady=10, columnspan=1, rowspan=1)
        #################################################
        #################################################

        #################################################
        #################################################
        self.Data_Label = Label(self.myFrame, text="Data_Label", width=125)
        self.Data_Label.grid(row=1, column=0, padx=5, pady=5, columnspan=1, rowspan=1)
        #################################################
        #################################################

        #################################################
        #################################################
        self.CSVfile_SaveFlag_Button = Button(self.myFrame, text='Save CSV', state="normal", width=20, font=("Helvetica", 12), command=lambda i=1: self.CSVfile_SaveFlag_ButtonResponse())
        self.CSVfile_SaveFlag_Button.grid(row=2, column=0, padx=5, pady=5, columnspan=1, rowspan=1)
        #################################################
        #################################################

        #################################################
        #################################################
        self.PrintToGui_Label = Label(self.myFrame, text="PrintToGui_Label", width=125)
        if self.EnableInternal_MyPrint_Flag == 1:
            self.PrintToGui_Label.grid(row=3, column=0, padx=10, pady=10, columnspan=10, rowspan=10)
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
    def CSVfile_SaveFlag_ButtonResponse(self):

        self.AcceptNewDataFlag = 0
        self.CSVfile_SaveFlag_NeedsToBeChangedFlag = 1

        #self.MyPrint_WithoutLogFile("CSVfileForTrajectoryData_SaveFlag_ButtonResponse event fired!")

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GUI_update_clock(self):

        #######################################################
        #######################################################
        #######################################################
        #######################################################
        #######################################################
        if self.USE_GUI_FLAG == 1:

            #######################################################
            #######################################################
            #######################################################
            #######################################################
            if self.EXIT_PROGRAM_FLAG == 0:

                #######################################################
                #######################################################
                #######################################################
                if self.GUI_ready_to_be_updated_flag == 1:

                    #######################################################
                    #######################################################
                    try:

                        #######################################################
                        self.Data_Label["text"] = "Time: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.CurrentTime_CalculatedFromMainThread, 0, 3) + \
                                                "\nCallback Frequency: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.DataStreamingFrequency_CalculatedFromMainThread, 0, 3) + \
                                                "\nAcceptNewDataFlag: " + str(self.AcceptNewDataFlag) + \
                                                "\t\tCSVfile_SaveFlag: " + str(self.CSVfile_SaveFlag) + \
                                                "\t\tDataQueue.qsize(): " + str(self.DataQueue.qsize())
                        #######################################################

                        #######################################################
                        if self.CSVfile_SaveFlag == 1:
                            self.CSVfile_SaveFlag_Button["bg"] = self.TKinter_LightGreenColor
                            self.CSVfile_SaveFlag_Button["text"] = "Saving CSV"
                        else:
                            self.CSVfile_SaveFlag_Button["bg"] = self.TKinter_LightRedColor
                            self.CSVfile_SaveFlag_Button["text"] = "NOT saving CSV"
                        #######################################################

                        #######################################################
                        self.PrintToGui_Label.config(text=self.PrintToGui_Label_TextInput_Str)
                        #######################################################

                    except:
                        exceptions = sys.exc_info()[0]
                        print("CSVdataLogger_ReubenPython3Class GUI_update_clock ERROR: Exceptions: %s" % exceptions)
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

