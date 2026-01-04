# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision Q, 12/22/2025

Verified working on: Python 3.11/12/13 for Windows 10/11 64-bit and Raspberry Pi Bookworm.
'''

__author__ = 'reuben.brewer'

##########################################################################################################
##########################################################################################################

#########################################################
import ReubenGithubCodeModulePaths #Replaces the need to have "ReubenGithubCodeModulePaths.pth" within "C:\Anaconda3\Lib\site-packages", which slows down the start of a Python interpreter if your code directories are in Google Drive.
ReubenGithubCodeModulePaths.Enable()
#########################################################

###########################################################
from EntryListWithBlinking_ReubenPython2and3Class import *
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
import queue as Queue
###########################################################

###########################################################
from tkinter import *
import tkinter.font as tkFont
from tkinter import ttk
###########################################################

###########################################################
import platform
if platform.system() == "Windows":
    import ctypes
    winmm = ctypes.WinDLL('winmm')
    winmm.timeBeginPeriod(1) #Set minimum timer resolution to 1ms so that time.sleep(0.001) behaves properly.
###########################################################

##########################################################################################################
##########################################################################################################

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

        self.CSVfile_FilepathFull = ""

        self.CSVfile_SaveFlag = 0
        self.CSVfile_SaveFlag_NeedsToBeChangedFlag = 0
        self.AcceptNewDataFlag = 0

        self.FilenamePrefix = ""
        self.TrialNumber = 0
        self.NoteToAddToFile = " " #Excel needs a non-zero str-length if it's in the header-row (can't use "").

        self.MostRecentDataDict = dict()
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
            if "GUI_WIDTH" in self.GUIparametersDict:
                self.GUI_WIDTH = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_WIDTH", self.GUIparametersDict["GUI_WIDTH"], -1.0, 1000.0))
            else:
                self.GUI_WIDTH = -1

            print("CSVdataLogger_ReubenPython3Class __init__: GUI_WIDTH: " + str(self.GUI_WIDTH))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_HEIGHT" in self.GUIparametersDict:
                self.GUI_HEIGHT = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_HEIGHT", self.GUIparametersDict["GUI_HEIGHT"], -1.0, 1000.0))
            else:
                self.GUI_HEIGHT = -1

            print("CSVdataLogger_ReubenPython3Class __init__: GUI_HEIGHT: " + str(self.GUI_HEIGHT))
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
        if "SaveOnStartupFlag" in setup_dict:
            self.SaveOnStartupFlag = self.PassThrough0and1values_ExitProgramOtherwise("SaveOnStartupFlag", setup_dict["SaveOnStartupFlag"])
        else:
            self.SaveOnStartupFlag = 0

        print("CSVdataLogger_ReubenPython3Class __init__: SaveOnStartupFlag: " + str(self.SaveOnStartupFlag))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.UpdateSetupDictParameters(setup_dict)
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.DataQueue = Queue.Queue()
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
        ######################################################### DON'T NEED THIS WHEN THERE'S A CALLBACK AND NOTHING TO DO IN THE MainThread!
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
    def UpdateSetupDictParameters(self, setup_dict):

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
        self.VariableNamesForHeaderList = list()
        self.VariablesHeaderStringCommaDelimited = ""

        if "VariableNamesForHeaderList" in setup_dict:
            VariableNamesForHeaderList_TEMP = setup_dict["VariableNamesForHeaderList"]

            self.SetVariableNamesForHeaderList(VariableNamesForHeaderList_TEMP)

        else:
            print("CSVdataLogger_ReubenPython3Class __init__: Error, 'VariableNamesForHeaderList' must be a list.")
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
        if "FilenamePrefix" in setup_dict:
            self.FilenamePrefix = str(setup_dict["FilenamePrefix"])
        else:
            self.FilenamePrefix = "CSVdataLogger_"

        print("CSVdataLogger_ReubenPython3Class __init__: FilenamePrefix: " + str(self.FilenamePrefix))
        #########################################################
        #########################################################
        
        #########################################################
        #########################################################
        if "TrialNumber" in setup_dict:
            self.TrialNumber = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("TrialNumber", setup_dict["TrialNumber"], 0, 100000))

        else:
            self.TrialNumber = 0

        print("CSVdataLogger_ReubenPython3Class __init__: TrialNumber: " + str(self.TrialNumber))
        #########################################################
        #########################################################
        
        #########################################################
        #########################################################
        if "NoteToAddToFile" in setup_dict:
            self.NoteToAddToFile = str(setup_dict["NoteToAddToFile"])

        else:
            self.NoteToAddToFile = " " #Excel needs a non-zero str-length if it's in the header-row (can't use "").

        print("CSVdataLogger_ReubenPython3Class __init__: NoteToAddToFile: " + str(self.NoteToAddToFile))
        #########################################################
        #########################################################
        
        #########################################################
        #########################################################
        if "EnableSaveButtonFlag" in setup_dict:
            self.EnableSaveButtonFlag = self.PassThrough0and1values_ExitProgramOtherwise("EnableSaveButtonFlag", setup_dict["EnableSaveButtonFlag"])
        else:
            self.EnableSaveButtonFlag = 1

        print("CSVdataLogger_ReubenPython3Class __init__: EnableSaveButtonFlag: " + str(self.EnableSaveButtonFlag))
        #########################################################
        #########################################################
        
        #########################################################
        #########################################################
        if "ShowSaveButtonFlag" in setup_dict:
            self.ShowSaveButtonFlag = self.PassThrough0and1values_ExitProgramOtherwise("ShowSaveButtonFlag", setup_dict["ShowSaveButtonFlag"])
        else:
            self.ShowSaveButtonFlag = 1

        print("CSVdataLogger_ReubenPython3Class __init__: ShowSaveButtonFlag: " + str(self.ShowSaveButtonFlag))
        #########################################################
        #########################################################
        
        #########################################################
        #########################################################
        if "SimplifyDataLabelFlag" in setup_dict:
            self.SimplifyDataLabelFlag = self.PassThrough0and1values_ExitProgramOtherwise("SimplifyDataLabelFlag", setup_dict["SimplifyDataLabelFlag"])
        else:
            self.SimplifyDataLabelFlag = 0

        print("CSVdataLogger_ReubenPython3Class __init__: SimplifyDataLabelFlag: " + str(self.SimplifyDataLabelFlag))
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
    def PassThrough0and1values_ExitProgramOtherwise(self, InputNameString, InputNumber, ExitProgramIfFailureFlag = 0):

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
            traceback.print_exc()

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
                              "). Press any key (and enter) to exit.")

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
            traceback.print_exc()

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
    def PassThroughFloatValuesInRange_ExitProgramOtherwise(self, InputNameString, InputNumber, RangeMinValue, RangeMaxValue, ExitProgramIfFailureFlag = 0):

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
    def IsAcceptingNewData(self):

        return self.AcceptNewDataFlag
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

            return 1
        except:
            exceptions = sys.exc_info()[0]
            print("CreateNewDirectoryIfItDoesntExist, Exceptions: %s" % exceptions)
            return 0
            #traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def SetVariableNamesForHeaderList(self, VariableNamesForHeaderList_Input):
        
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        try:
            VariableNamesForHeaderList_BeingConstructed = list()
            VariablesHeaderStringCommaDelimited_BeingConstructed = ""

            if isinstance(VariableNamesForHeaderList_Input, list) == 1:

                ##########################################################################################################
                ##########################################################################################################
                for index, VariableName in enumerate(VariableNamesForHeaderList_Input):
                    
                    VariablesHeaderStringCommaDelimited_BeingConstructed = VariablesHeaderStringCommaDelimited_BeingConstructed + str(VariableName)
                    VariableNamesForHeaderList_BeingConstructed.append(str(VariableName))

                    ##########################################################################################################
                    if index < len(VariableNamesForHeaderList_Input) - 1:
                        VariablesHeaderStringCommaDelimited_BeingConstructed = VariablesHeaderStringCommaDelimited_BeingConstructed + ", "

                    else:
                        VariablesHeaderStringCommaDelimited_BeingConstructed = VariablesHeaderStringCommaDelimited_BeingConstructed
                    ##########################################################################################################
                
                ##########################################################################################################
                ##########################################################################################################
                
                self.VariableNamesForHeaderList = VariableNamesForHeaderList_BeingConstructed
                self.VariablesHeaderStringCommaDelimited = VariablesHeaderStringCommaDelimited_BeingConstructed
                
                return 1
                
            else:
                print("SetVariableNamesForHeaderList: Error, 'VariableNamesForHeaderList' must be a list.")
                return 0
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
    
        ##########################################################################################################
        #########################################################################################################
        ##########################################################################################################
        except:
            exceptions = sys.exc_info()[0]
            print("SetVariableNamesForHeaderList, Exceptions: %s" % exceptions)
            return 0
            #traceback.print_exc()
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
    
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    
    ##########################################################################################################
    ##########################################################################################################
    def SetFilenamePrefix(self, FilenamePrefix_Input):
        
        try:
            self.FilenamePrefix = str(FilenamePrefix_Input)
            self.EntryListWithBlinking_ReubenPython2and3ClassObject_NeedsToBeUpdatedByExternalValueFlag = 1
            
        except:
            exceptions = sys.exc_info()[0]
            print("SetFilenamePrefix, Exceptions: %s" % exceptions)
            #traceback.print_exc()
            
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SetTrialNumber(self, TrialNumber_Input):
        
        try:
            self.TrialNumber = int(TrialNumber_Input)
            self.EntryListWithBlinking_ReubenPython2and3ClassObject_NeedsToBeUpdatedByExternalValueFlag = 1
            
            print("SetTrialNumber event fired!")
        except:
            exceptions = sys.exc_info()[0]
            print("SetTrialNumber, Exceptions: %s" % exceptions)
            #traceback.print_exc()
            
    ##########################################################################################################
    ##########################################################################################################
    
    ##########################################################################################################
    ##########################################################################################################
    def SetNoteToAddToFile(self, NoteToAddToFile_Input):
        
        try:
            self.NoteToAddToFile = str(NoteToAddToFile_Input)
            self.EntryListWithBlinking_ReubenPython2and3ClassObject_NeedsToBeUpdatedByExternalValueFlag = 1
            
        except:
            exceptions = sys.exc_info()[0]
            print("SetNoteToAddToFile, Exceptions: %s" % exceptions)
            #traceback.print_exc()
            
    ##########################################################################################################
    ##########################################################################################################
    
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def CreateCSVfileAndStartWritingData(self, CSVfile_DirectoryPath_Input = "", 
                                                FilenamePrefix_Input = "", 
                                                TrialNumber_Input = -1, 
                                                NoteToAddToFile_Input = "", 
                                                VariableNamesForHeaderList_Input = []):

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            ##########################################################################################################
            if CSVfile_DirectoryPath_Input != "":
                self.CSVfile_DirectoryPath = CSVfile_DirectoryPath_Input
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            if FilenamePrefix_Input != "":
                self.SetFilenamePrefix(FilenamePrefix_Input)
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            if TrialNumber_Input != -1:
                self.SetTrialNumber(TrialNumber_Input)
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            if NoteToAddToFile_Input != "":
                self.SetNoteToAddToFile(NoteToAddToFile_Input)
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            if VariableNamesForHeaderList_Input != []:
                self.SetVariableNamesForHeaderList(VariableNamesForHeaderList_Input)
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            self.CreateNewDirectoryIfItDoesntExist(self.CSVfile_DirectoryPath)

            self.CSVfile_FilepathFull = os.path.join(self.CSVfile_DirectoryPath,
                                                    self.FilenamePrefix
                                                    + "_Trial_" + str(self.TrialNumber)
                                                    + "_" + self.getTimeStampString()
                                                    + ".csv")

            self.CSVfile_FileObject = open(self.CSVfile_FilepathFull, "a") #Will append to file if it exists, create new file with this as first entry if file doesn't exist.

            ##########################################################################################################
            self.CSVfile_FileObject.write(self.VariablesHeaderStringCommaDelimited + ",NoteToAddToFile," + str(self.NoteToAddToFile) + "\n")
            ##########################################################################################################

            '''
            ##########################################################################################################
            #Most parsers (like Python's pandas.read_csv() or Excel import tools) ignore lines starting with # if configured to do so.

            # This file contains test data collected on June 15
            # Columns: Time (s), Position (mm)
            #Time,Position
            #0.0,0
            #1.0,10
            #2.0,20
            
            #In pandas, you can explicitly ignore comments with:
            
            #import pandas as pd
            #df = pd.read_csv("file.csv", comment="#")
            
            self.CSVfile_FileObject.write("#NoteToAddToFile," + self.NoteToAddToFile + "\n")
            ##########################################################################################################
            '''

            self.AcceptNewDataFlag = 1
            self.CSVfile_SaveFlag = 1

            print("CreateCSVfileAndStartWritingData: Opened file " + self.CSVfile_FilepathFull + " and started writing data!")

            return 1
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        except:
            exceptions = sys.exc_info()[0]
            print("CreateCSVfileAndStartWritingData, Exceptions: %s" % exceptions)
            return 0
            #traceback.print_exc()
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
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

                return 1

        except:
            exceptions = sys.exc_info()[0]
            print("CloseCSVfileAndStopWritingData, Exceptions: %s" % exceptions)
            return 0
            #traceback.print_exc()

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
    def GetMostRecentDataDict(self):

        if self.EXIT_PROGRAM_FLAG == 0:

            return deepcopy(self.MostRecentDataDict) #deepcopy IS required as MostRecentDataDict contains lists.

        else:
            return dict()  # So that we're not returning variables during the close-down process.
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def AddDataToCSVfile_ExternalFunctionCall(self, ListOfDataToWrite, PrintForDebuggingFlag=0):

        if PrintForDebuggingFlag == 1:
            print("AddDataToCSVfile_ExternalFunctionCall: self.AcceptNewDataFlag = " + str(self.AcceptNewDataFlag) + ", ListOfDataToWrite = " + str(ListOfDataToWrite))

        if self.AcceptNewDataFlag == 1:

            if isinstance(ListOfDataToWrite, list) == 1:

                if len(ListOfDataToWrite) == len(self.VariableNamesForHeaderList):
                    self.DataQueue.put(ListOfDataToWrite)

                else:
                    print("AddDataToCSVfile: ERROR,list is incorrect length. len(ListOfDataToWrite) = " + str(len(ListOfDataToWrite)) + ", len(self.VariableNamesForHeaderList) = " + str(len(self.VariableNamesForHeaderList)))

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
                self.UpdateFrequencyCalculation_MainThread()

                self.MostRecentDataDict["Time"] = self.CurrentTime_CalculatedFromMainThread
                self.MostRecentDataDict["DataStreamingFrequency_CalculatedFromMainThread"] = self.DataStreamingFrequency_CalculatedFromMainThread
                self.MostRecentDataDict["AcceptNewDataFlag"] = self.AcceptNewDataFlag
                self.MostRecentDataDict["IsSavingFlag"] = self.CSVfile_SaveFlag
                self.MostRecentDataDict["DataQueue_qsize"] = self.DataQueue.qsize()
                self.MostRecentDataDict["VariableNamesForHeaderList"] = self.VariableNamesForHeaderList
                self.MostRecentDataDict["FilepathFull"] = self.CSVfile_FilepathFull
                self.MostRecentDataDict["FilenamePrefix"] = self.FilenamePrefix
                self.MostRecentDataDict["TrialNumber"] = self.TrialNumber
                self.MostRecentDataDict["NoteToAddToFile"] = self.NoteToAddToFile

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
    def CreateGUIobjects(self, TkinterParent):

        print("CSVdataLogger_ReubenPython3ClassStarting, CreateGUIobjects event fired.")

        #################################################
        #################################################
        self.root = TkinterParent
        self.parent = TkinterParent
        #################################################
        #################################################

        #################################################
        #################################################
        if self.GUI_WIDTH != -1 and self.GUI_HEIGHT != -1:
            self.myFrame = Frame(self.root, height = self.GUI_HEIGHT, width = self.GUI_WIDTH) #MUST SPECIFY BOTH HEIGHT AND WIDTH FOR PROPER RESULTS
        else:
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
                   
        if self.GUI_WIDTH != -1 and self.GUI_HEIGHT != -1:
            self.myFrame.grid_propagate(False)  # Prevent auto-resize, perform first in GUI_Thread() before everything else has been grid()'ed
        
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
        self.CSVfile_SaveFlag_Button = Button(self.myFrame, text='Save CSV', state="normal", width=20, font=("Helvetica", 12), command=lambda i=1: self.CSVfile_SaveFlag_ButtonResponse())
        
        if self.ShowSaveButtonFlag == 1:
            self.CSVfile_SaveFlag_Button.grid(row=0, column=0, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=1, rowspan=1)
        #################################################
        #################################################

        #################################################
        #################################################
        self.EntryListWithBlinking_ReubenPython2and3ClassObject_NeedsToBeUpdatedByExternalValueFlag = 0

        self.EntryWidth = 60
        self.LabelWidth = 20
        self.FontSize = 12

        self.EntryListWithBlinking_ReubenPython2and3ClassObject_GUIparametersDict = dict([("UseBorderAroundThisGuiObjectFlag", 0),
                                                                                          ("GUI_ROW", 0),
                                                                                          ("GUI_COLUMN", 1),
                                                                                          ("GUI_PADX", 10),
                                                                                          ("GUI_PADY", 10),
                                                                                          ("GUI_ROWSPAN", 1),
                                                                                          ("GUI_COLUMNSPAN", 1),
                                                                                          ("GUI_STICKY", "w")])

        self.EntryListWithBlinking_Variables_ListOfDicts = [dict([("Name", "FilenamePrefix"),("Type", "str"), ("StartingVal", self.FilenamePrefix), ("EntryWidth", self.EntryWidth), ("LabelWidth", self.LabelWidth), ("FontSize", self.FontSize)]),
                                                            dict([("Name", "TrialNumber"),("Type", "int"), ("StartingVal", self.TrialNumber), ("MinVal", 0), ("MaxVal", 1000000), ("EntryWidth", self.EntryWidth), ("LabelWidth", self.LabelWidth), ("FontSize", self.FontSize)]),
                                                            dict([("Name", "NoteToAddToFile"),("Type", "str"), ("StartingVal", self.NoteToAddToFile), ("EntryWidth", self.EntryWidth), ("LabelWidth", self.LabelWidth), ("FontSize", self.FontSize)])]

        self.EntryListWithBlinking_ReubenPython2and3ClassObject_setup_dict = dict([("GUIparametersDict", self.EntryListWithBlinking_ReubenPython2and3ClassObject_GUIparametersDict),
                                                                              ("EntryListWithBlinking_Variables_ListOfDicts", self.EntryListWithBlinking_Variables_ListOfDicts),
                                                                              ("DebugByPrintingVariablesFlag", 0)])

        try:
            self.EntryListWithBlinking_ReubenPython2and3ClassObject = EntryListWithBlinking_ReubenPython2and3Class(self.EntryListWithBlinking_ReubenPython2and3ClassObject_setup_dict)
            time.sleep(0.010)
            self.EntryListWithBlinking_OPEN_FLAG = self.EntryListWithBlinking_ReubenPython2and3ClassObject.OBJECT_CREATED_SUCCESSFULLY_FLAG

            if self.EntryListWithBlinking_OPEN_FLAG == 1:
                self.EntryListWithBlinking_ReubenPython2and3ClassObject.CreateGUIobjects(TkinterParent=self.myFrame)

        except:
            exceptions = sys.exc_info()[0]
            print("GUI_Thread for CSVdataLogger_ReubenPython3Class, EntryListWithBlinking_ReubenPython2and3ClassObject __init__: Exceptions: %s" % exceptions)
            traceback.print_exc()
        #################################################
        #################################################

        #################################################
        #################################################
        self.Data_Label = Label(self.myFrame, text="Data_Label", width=125)
        
        if self.SimplifyDataLabelFlag == 0:
            self.Data_Label.grid(row=1, column=0, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=2, rowspan=1)
            self.Data_Label["width"] = 125
        else:
            self.Data_Label.grid(row=0, column=2, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=2, rowspan=2)
            self.Data_Label["width"] = 25
        #################################################
        #################################################

        #################################################
        #################################################
        self.PrintToGui_Label = Label(self.myFrame, text="PrintToGui_Label", width=125)
        if self.EnableInternal_MyPrint_Flag == 1:
            self.PrintToGui_Label.grid(row=2, column=0, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=10, rowspan=10)
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
    def grid(self):
        
        ##########################################################################################################
        try:
            #print("grid() event fired for CSVdataLogger_ReubenPython3Class")
            
            self.myFrame.grid()
            
            self.GUI_update_clock()
            
        ##########################################################################################################
        
        ##########################################################################################################
        except:
            exceptions = sys.exc_info()[0]
            print("grid() for CSVdataLogger_ReubenPython3Class, Exceptions: %s" % exceptions)
            traceback.print_exc()
        ##########################################################################################################
        
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def grid_remove(self):
        
        ##########################################################################################################
        try:
            #print("grid() event fired for CSVdataLogger_ReubenPython3Class")
            
            self.myFrame.grid_remove()
            
            self.GUI_update_clock()

        ##########################################################################################################
        
        ##########################################################################################################
        except:
            exceptions = sys.exc_info()[0]
            print("grid_remove() for CSVdataLogger_ReubenPython3Class, Exceptions: %s" % exceptions)
            traceback.print_exc()
        ##########################################################################################################
        
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
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def GUI_update_clock(self):

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        if self.USE_GUI_FLAG == 1:

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            if self.EXIT_PROGRAM_FLAG == 0:

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                if self.GUI_ready_to_be_updated_flag == 1:

                    ##########################################################################################################
                    ##########################################################################################################
                    ##########################################################################################################
                    try:

                        ##########################################################################################################
                        ##########################################################################################################
                        if self.EnableSaveButtonFlag == 1 and self.CSVfile_SaveFlag_Button["state"] != "normal":
                            self.CSVfile_SaveFlag_Button["state"] = "normal"

                        elif self.EnableSaveButtonFlag == 0 and self.CSVfile_SaveFlag_Button["state"] != "disabled":
                            self.CSVfile_SaveFlag_Button["state"] = "disabled"
                        ##########################################################################################################
                        ##########################################################################################################

                        ##########################################################################################################
                        ##########################################################################################################
                        if self.SimplifyDataLabelFlag == 0:
                            self.Data_Label["text"] = self.ConvertDictToProperlyFormattedStringForPrinting(self.MostRecentDataDict,
                                                                                                        NumberOfDecimalsPlaceToUse = 5,
                                                                                                        NumberOfEntriesPerLine = 1,
                                                                                                        NumberOfTabsBetweenItems = 3)
                        else:
                            self.Data_Label["text"] = "SaveFlag: " + str(self.CSVfile_SaveFlag) + "\nAcceptNewDataFlag: " + str(self.AcceptNewDataFlag) + "\nDataQueue_qsize: " + str(self.DataQueue.qsize())
                        ##########################################################################################################
                        ##########################################################################################################

                        ##########################################################################################################
                        ##########################################################################################################
                        if self.CSVfile_SaveFlag == 1:
                            self.CSVfile_SaveFlag_Button["bg"] = self.TKinter_LightGreenColor
                            self.CSVfile_SaveFlag_Button["text"] = "Saving CSV"
                        else:
                            self.CSVfile_SaveFlag_Button["bg"] = self.TKinter_LightRedColor
                            self.CSVfile_SaveFlag_Button["text"] = "NOT saving CSV"
                        ##########################################################################################################
                        ##########################################################################################################

                        ##########################################################################################################
                        ##########################################################################################################
                        if self.EntryListWithBlinking_OPEN_FLAG == 1:

                            ##########################################################################################################
                            if self.EntryListWithBlinking_ReubenPython2and3ClassObject_NeedsToBeUpdatedByExternalValueFlag == 1:

                                self.EntryListWithBlinking_ReubenPython2and3ClassObject.SetEntryValue("FilenamePrefix", self.FilenamePrefix)
                                self.EntryListWithBlinking_ReubenPython2and3ClassObject.SetEntryValue("TrialNumber", self.TrialNumber)
                                self.EntryListWithBlinking_ReubenPython2and3ClassObject.SetEntryValue("NoteToAddToFile", self.NoteToAddToFile)

                                self.EntryListWithBlinking_ReubenPython2and3ClassObject_NeedsToBeUpdatedByExternalValueFlag = 0
                            ##########################################################################################################

                            ##########################################################################################################
                            self.EntryListWithBlinking_ReubenPython2and3ClassObject.GUI_update_clock()
                            ##########################################################################################################

                            ##########################################################################################################
                            MostRecentDataDict_EntryListWithBlinking = self.EntryListWithBlinking_ReubenPython2and3ClassObject.GetMostRecentDataDict()  # Get latest gain values

                            self.FilenamePrefix = MostRecentDataDict_EntryListWithBlinking["FilenamePrefix"]
                            self.TrialNumber = MostRecentDataDict_EntryListWithBlinking["TrialNumber"]
                            self.NoteToAddToFile = MostRecentDataDict_EntryListWithBlinking["NoteToAddToFile"]
                            ##########################################################################################################

                        ##########################################################################################################
                        ##########################################################################################################

                        ##########################################################################################################
                        ##########################################################################################################
                        self.PrintToGui_Label.config(text=self.PrintToGui_Label_TextInput_Str)
                        ##########################################################################################################
                        ##########################################################################################################

                    except:
                        exceptions = sys.exc_info()[0]
                        print("CSVdataLogger_ReubenPython3Class GUI_update_clock ERROR: Exceptions: %s" % exceptions)
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
    ##########################################################################################################
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

        try:
            ProperlyFormattedStringForPrinting = ""
            ItemsPerLineCounter = 0

            for Key in DictToPrint:

                ##########################################################################################################
                if isinstance(DictToPrint[Key], dict): #RECURSION
                    ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                         str(Key) + ":\n" + \
                                                         self.ConvertDictToProperlyFormattedStringForPrinting(DictToPrint[Key],
                                                                                                              NumberOfDecimalsPlaceToUse,
                                                                                                              NumberOfEntriesPerLine,
                                                                                                              NumberOfTabsBetweenItems)

                else:
                    ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                         str(Key) + ": " + \
                                                         self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(DictToPrint[Key],
                                                                                                                                               0,
                                                                                                                                               NumberOfDecimalsPlaceToUse)
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

        except:
            exceptions = sys.exc_info()[0]
            print("ConvertDictToProperlyFormattedStringForPrinting, Exceptions: %s" % exceptions)
            return ""
            #traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

