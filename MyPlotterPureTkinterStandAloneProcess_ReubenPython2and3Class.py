# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com,
www.reubotics.com

Apache 2 License
Software Revision AA, 12/22/2025

Verified working on: Python 3.11/12/13 for Windows 10/11 64-bit, Ubuntu 20.04, and Raspberry Pi Bookworm.
'''

__author__ = 'reuben.brewer'

##########################################################
import ReubenGithubCodeModulePaths #Replaces the need to have "ReubenGithubCodeModulePaths.pth" within "C:\Anaconda3\Lib\site-packages", which slows down the start of a Python interpreter if your code directories are in Google Drive.
ReubenGithubCodeModulePaths.Enable()
#########################################################

#########################################################
try:
    from GetCPUandMemoryUsageOfProcessByPID_ReubenPython3Class import *
    GetCPUandMemoryUsageOfProcessByPID_ModuleImportedFlag = 1

except:
    exceptions = sys.exc_info()[0]
    GetCPUandMemoryUsageOfProcessByPID_ModuleImportedFlag = 0
    print("Error: the module 'GetCPUandMemoryUsageOfProcessByPID_ReubenPython3Class' could not be imported. Exceptions: %s" % exceptions)
    traceback.print_exc()
#########################################################

#########################################################
import os
import sys
import time
import datetime
import numpy
import multiprocessing
import collections
from copy import *  # for deepcopy(dict)
import inspect  # To enable 'TellWhichFileWereIn'
import traceback
import math
from decimal import Decimal
import threading
import platform
import psutil
import pexpect
import subprocess
import re
import signal  #for CTRLc_HandlerFunction
import queue as Queue
from queue import Empty #For draining the queue
#########################################################

#########################################################
from tkinter import *
import tkinter.font as tkFont
from tkinter import ttk
#########################################################

#########################################################
try:
    import pyautogui
    pyautogui_ModuleImportedFlag = 1

except:
    pyautogui_ModuleImportedFlag = 0
    print("Error: the module 'pyautogui' could not be imported.")
#########################################################

#########################################################
import platform

if platform.system() == "Windows":
    import ctypes

    winmm = ctypes.WinDLL('winmm')
    winmm.timeBeginPeriod(1)  # Set minimum timer resolution to 1ms so that time.sleep(0.001) behaves properly.
#########################################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
class MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class(Frame):  # Subclass the Tkinter Frame

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def __init__(self, SetupDict):

        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0
        self.pyautogui_ModuleImportedFlag = pyautogui_ModuleImportedFlag

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        if sys.version_info[0] < 3:
            print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class __init__: Only Python 3 is supported, not 2.")
            return
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        try:
            
            multiprocessing_StartMethod = multiprocessing.get_start_method()
            print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class __init__: multiprocessing.get_start_method(): " + str(multiprocessing_StartMethod))
            
            if multiprocessing_StartMethod != "spawn":
                print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class __init__: Issuing multiprocessing.set_start_method('spawn', force=True).")
                multiprocessing.set_start_method('spawn', force=True)  # 'spawn' is required for all Linux flavors, with 'force=True' required specicially by Ubuntu (not Raspberry Pi).
                
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        except:
            exceptions = sys.exc_info()[0]
            print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class __init__: multiprocessing.set_start_method('spawn', force=True) Exceptions: %s" % exceptions)
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        
        '''
        From: https://docs.python.org/3/library/multiprocessing.html#multiprocessing-programming
        Spawn: The parent process starts a fresh python interpreter process.
        The child process will only inherit those resources necessary to run the process object’s run() method.
        In particular, unnecessary file descriptors and handles from the parent process will not be inherited.
        Starting a process using this method is rather slow compared to using fork or forkserver.
        Available on Unix and Windows. The default on Windows and macOS.
        '''

        self.MultiprocessingQueue_Rx = multiprocessing.Queue()  # NOT a regular Queue.queue
        self.MultiprocessingQueue_Tx = multiprocessing.Queue()  # NOT a regular Queue.queue
        self.job_for_another_core = multiprocessing.Process(target=self.StandAlonePlottingProcess, args=(self.MultiprocessingQueue_Rx, self.MultiprocessingQueue_Tx, SetupDict))  # args=(self.MultiprocessingQueue_Rx,)
        self.job_for_another_core.start()

        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 1
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ###########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def CTRLc_RegisterHandlerFunction(self):

        CurrentHandlerRegisteredForSIGINT = signal.getsignal(signal.SIGINT)
        defaultish = (signal.SIG_DFL, signal.SIG_IGN, None, getattr(signal, "default_int_handler", None)) #Treat Python's built-in default handler as "unregistered"

        if CurrentHandlerRegisteredForSIGINT in defaultish:  # Only install if it's default/ignored (i.e., nobody set it yet)
            signal.signal(signal.SIGINT, self.CTRLc_HandlerFunction)
            print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, CTRLc_RegisterHandlerFunction event fired!")

        else:
            print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, could not register CTRLc_RegisterHandlerFunction (already registered previously)")
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## MUST ISSUE CTRLc_RegisterHandlerFunction() AT START OF PROGRAM
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def CTRLc_HandlerFunction(self, signum, frame):

        print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, CTRLc_HandlerFunction event firing!")

        self.SendEndCommandToStandAloneProcess()

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def RemoveLeadingZerosFromString(self, StringInput):
        OutputString = re.sub(r'([+-])0+(?=\d)', r'\1', StringInput)

        return OutputString
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def __ProcessVariablesThatCanNOTbeLiveUpdated(self, SetupDict, PrintInfoForDebuggingFlag = 0):

        return 1 #Can add variables here later as needed.

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def __ProcessVariablesThatCanBeLiveUpdated(self, SetupDict, PrintInfoForDebuggingFlag = 0):

        try:

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            self.SetupDict = SetupDict
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            ########################################################################################################## UNICORN
            self.RootGeometryHasBeenModifiedFlag = 1 #By default, ALWAYS clear the graph when we enter this function.
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            if "GUIparametersDict" in SetupDict:
                GUIparametersDict = SetupDict["GUIparametersDict"]

                ##########################################
                ##########################################
                if "GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents" in GUIparametersDict:
                    self.GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents", GUIparametersDict["GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents"], 0.0, 1000.0))
                else:
                    self.GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents = 30  # Will get us around 30Hz actual when plottting 2 curves with 100 data points each and 35 tick marks on each axis

                if PrintInfoForDebuggingFlag == 1: print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, __ProcessVariablesThatCanBeLiveUpdated: GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents: " + str(self.GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents))
                ##########################################
                ##########################################

                ##########################################
                ##########################################
                if "EnableInternal_MyPrint_Flag" in GUIparametersDict:
                    self.EnableInternal_MyPrint_Flag = self.PassThrough0and1values_ExitProgramOtherwise("EnableInternal_MyPrint_Flag", GUIparametersDict["EnableInternal_MyPrint_Flag"])
                else:
                    self.EnableInternal_MyPrint_Flag = 0

                if PrintInfoForDebuggingFlag == 1: print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, __ProcessVariablesThatCanBeLiveUpdated: EnableInternal_MyPrint_Flag: " + str(self.EnableInternal_MyPrint_Flag))
                ##########################################
                ##########################################

                ##########################################
                ##########################################
                if "PrintToConsoleFlag" in GUIparametersDict:
                    self.PrintToConsoleFlag = self.PassThrough0and1values_ExitProgramOtherwise("PrintToConsoleFlag", GUIparametersDict["PrintToConsoleFlag"])
                else:
                    self.PrintToConsoleFlag = 1

                if PrintInfoForDebuggingFlag == 1: print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, __ProcessVariablesThatCanBeLiveUpdated: PrintToConsoleFlag: " + str(self.PrintToConsoleFlag))
                ##########################################
                ##########################################

                ##########################################
                ##########################################
                if "NumberOfPrintLines" in GUIparametersDict:
                    self.NumberOfPrintLines = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("NumberOfPrintLines", GUIparametersDict["NumberOfPrintLines"], 0.0, 50.0))
                else:
                    self.NumberOfPrintLines = 10

                if PrintInfoForDebuggingFlag == 1: print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, __ProcessVariablesThatCanBeLiveUpdated: NumberOfPrintLines: " + str(self.NumberOfPrintLines))
                ##########################################
                ##########################################

                ##########################################
                ##########################################
                if "GraphCanvasWidth" in GUIparametersDict:
                    self.GraphCanvasWidth = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GraphCanvasWidth", GUIparametersDict["GraphCanvasWidth"], 480.0, 1000000.0)
                else:
                    self.GraphCanvasWidth = 640.0

                if PrintInfoForDebuggingFlag == 1: print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, __ProcessVariablesThatCanBeLiveUpdated: GraphCanvasWidth: " + str(self.GraphCanvasWidth))
                ##########################################
                ##########################################

                ##########################################
                ##########################################
                if "GraphCanvasHeight" in GUIparametersDict:
                    self.GraphCanvasHeight = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GraphCanvasHeight", GUIparametersDict["GraphCanvasHeight"], 240.0, 1000000.0)
                else:
                    self.GraphCanvasHeight = 480.0

                if PrintInfoForDebuggingFlag == 1: print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, __ProcessVariablesThatCanBeLiveUpdated: GraphCanvasHeight: " + str(self.GraphCanvasHeight))
                ##########################################
                ##########################################

                ##########################################
                ##########################################
                if "GraphCanvasWindowTitle" in GUIparametersDict:
                    self.GraphCanvasWindowTitle = str(GUIparametersDict["GraphCanvasWindowTitle"])
                else:
                    self.GraphCanvasWindowTitle = "MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class"

                if PrintInfoForDebuggingFlag == 1: print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, __ProcessVariablesThatCanBeLiveUpdated: GraphCanvasWindowTitle: " + self.GraphCanvasWindowTitle)
                ##########################################
                ##########################################

                ##########################################
                ##########################################
                if "GraphCanvasWindowStartingX" in GUIparametersDict:
                    self.GraphCanvasWindowStartingX = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GraphCanvasWindowStartingX", GUIparametersDict["GraphCanvasWindowStartingX"], 0.0, 1000000.0))
                else:
                    self.GraphCanvasWindowStartingX = 0.0

                if PrintInfoForDebuggingFlag == 1: print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, __ProcessVariablesThatCanBeLiveUpdated: GraphCanvasWindowStartingX: " + str(self.GraphCanvasWindowStartingX))
                ##########################################
                ##########################################

                ##########################################
                ##########################################
                if "GraphCanvasWindowStartingY" in GUIparametersDict:
                    self.GraphCanvasWindowStartingY = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GraphCanvasWindowStartingY", GUIparametersDict["GraphCanvasWindowStartingY"], 0.0, 1000000.0))
                else:
                    self.GraphCanvasWindowStartingY = 0.0

                if PrintInfoForDebuggingFlag == 1: print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, __ProcessVariablesThatCanBeLiveUpdated: GraphCanvasWindowStartingY: " + str(self.GraphCanvasWindowStartingY))
                ##########################################
                ##########################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

            ##########################################
            ##########################################
            if "ParentPID" in SetupDict:
                self.ParentPID = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("ParentPID", SetupDict["ParentPID"], 0.0, 100000000.0))
            else:
                self.ParentPID = -11111

            if PrintInfoForDebuggingFlag == 1: print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, __ProcessVariablesThatCanBeLiveUpdated: ParentPID: " + str(self.ParentPID))
            ##########################################
            ##########################################

            ##########################################
            ##########################################
            if "SmallTextSize" in SetupDict:
                self.SmallTextSize = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("SmallTextSize", SetupDict["SmallTextSize"], 7, 20))
            else:
                self.SmallTextSize = 7

            if PrintInfoForDebuggingFlag == 1: print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, __ProcessVariablesThatCanBeLiveUpdated: SmallTextSize: " + str(self.SmallTextSize))
            ##########################################
            ##########################################

            ##########################################
            ##########################################
            if "LargeTextSize" in SetupDict:
                self.LargeTextSize = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("LargeTextSize", SetupDict["LargeTextSize"], 7, 20))
            else:
                self.LargeTextSize = 12

            if PrintInfoForDebuggingFlag == 1: print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, __ProcessVariablesThatCanBeLiveUpdated: LargeTextSize: " + str(self.LargeTextSize))
            ##########################################
            ##########################################

            ##########################################
            ##########################################
            if "NumberOfDataPointToPlot" in SetupDict:
                self.NumberOfDataPointToPlot = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("NumberOfDataPointToPlot", SetupDict["NumberOfDataPointToPlot"], 0.0, 1000000))
            else:
                self.NumberOfDataPointToPlot = 10

            if PrintInfoForDebuggingFlag == 1: print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, __ProcessVariablesThatCanBeLiveUpdated: NumberOfDataPointToPlot: " + str(self.NumberOfDataPointToPlot))
            ##########################################
            ##########################################

            ##########################################
            ##########################################
            if "XaxisNumberOfTickMarks" in SetupDict:
                self.XaxisNumberOfTickMarks = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("XaxisNumberOfTickMarks", SetupDict["XaxisNumberOfTickMarks"], 0.0, 1000))
            else:
                self.XaxisNumberOfTickMarks = 30

            if PrintInfoForDebuggingFlag == 1: print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, __ProcessVariablesThatCanBeLiveUpdated: XaxisNumberOfTickMarks: " + str(self.XaxisNumberOfTickMarks))
            ##########################################
            ##########################################

            ##########################################
            ##########################################
            if "YaxisNumberOfTickMarks" in SetupDict:
                self.YaxisNumberOfTickMarks = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("YaxisNumberOfTickMarks", SetupDict["YaxisNumberOfTickMarks"], 0.0, 1000))
            else:
                self.YaxisNumberOfTickMarks = 30

            if PrintInfoForDebuggingFlag == 1: print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, __ProcessVariablesThatCanBeLiveUpdated: YaxisNumberOfTickMarks: " + str(self.YaxisNumberOfTickMarks))
            ##########################################
            ##########################################

            ##########################################
            ##########################################
            if "XaxisNumberOfDecimalPlacesForLabels" in SetupDict:
                self.XaxisNumberOfDecimalPlacesForLabels = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("XaxisNumberOfDecimalPlacesForLabels", SetupDict["XaxisNumberOfDecimalPlacesForLabels"], 0.0, 3.0))
            else:
                self.XaxisNumberOfDecimalPlacesForLabels = 1

            if PrintInfoForDebuggingFlag == 1: print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, __ProcessVariablesThatCanBeLiveUpdated: XaxisNumberOfDecimalPlacesForLabels: " + str(self.XaxisNumberOfDecimalPlacesForLabels))
            ##########################################
            ##########################################

            ##########################################
            ##########################################
            if "YaxisNumberOfDecimalPlacesForLabels" in SetupDict:
                self.YaxisNumberOfDecimalPlacesForLabels = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("YaxisNumberOfDecimalPlacesForLabels", SetupDict["YaxisNumberOfDecimalPlacesForLabels"], 0.0, 3.0))
            else:
                self.YaxisNumberOfDecimalPlacesForLabels = 1

            if PrintInfoForDebuggingFlag == 1: print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, __ProcessVariablesThatCanBeLiveUpdated: YaxisNumberOfDecimalPlacesForLabels: " + str(self.YaxisNumberOfDecimalPlacesForLabels))
            ##########################################
            ##########################################

            ##########################################
            ##########################################
            if "X_min" in SetupDict:
                self.X_min = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("X_min", SetupDict["X_min"], -1000000000000.0, 1000000000000.0)
            else:
                self.X_min = 0.0

            if PrintInfoForDebuggingFlag == 1: print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, __ProcessVariablesThatCanBeLiveUpdated: X_min: " + str(self.X_min))

            self.X_min_StoredFrom__ProcessVariablesThatCanBeLiveUpdated = self.X_min
            ##########################################
            ##########################################

            ##########################################
            ##########################################
            if "X_max" in SetupDict:
                self.X_max = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("X_max", SetupDict["X_max"], -1000000000000.0, 1000000000000.0)
            else:
                self.X_max = 10.0

            if PrintInfoForDebuggingFlag == 1: print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, __ProcessVariablesThatCanBeLiveUpdated: X_max: " + str(self.X_max))

            self.X_max_StoredFrom__ProcessVariablesThatCanBeLiveUpdated = self.X_max
            ##########################################
            ##########################################

            ##########################################
            ##########################################
            if "Y_min" in SetupDict:
                self.Y_min = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("Y_min", SetupDict["Y_min"], -1000000000000.0, 1000000000000.0)
            else:
                self.Y_min = -10.0

            if PrintInfoForDebuggingFlag == 1: print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, __ProcessVariablesThatCanBeLiveUpdated: Y_min: " + str(self.Y_min))

            self.Y_min_StoredFrom__ProcessVariablesThatCanBeLiveUpdated = self.Y_min
            ##########################################
            ##########################################

            ##########################################
            ##########################################
            if "Y_max" in SetupDict:
                self.Y_max = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("Y_max", SetupDict["Y_max"], -1000000000000.0, 1000000000000.0)
            else:
                self.Y_max = 10.0

            if PrintInfoForDebuggingFlag == 1: print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, __ProcessVariablesThatCanBeLiveUpdated: Y_max: " + str(self.Y_max))

            self.Y_max_StoredFrom__ProcessVariablesThatCanBeLiveUpdated = self.Y_max
            ##########################################
            ##########################################

            ##########################################
            ##########################################
            if "XaxisAutoscaleFlag" in SetupDict:
                self.XaxisAutoscaleFlag = self.PassThrough0and1values_ExitProgramOtherwise("XaxisAutoscaleFlag", SetupDict["XaxisAutoscaleFlag"])
            else:
                self.XaxisAutoscaleFlag = 1

            if PrintInfoForDebuggingFlag == 1: print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, __ProcessVariablesThatCanBeLiveUpdated: XaxisAutoscaleFlag: " + str(self.XaxisAutoscaleFlag))

            if self.XaxisAutoscaleFlag == 1:
                self.X_min = 0  # Have to override any other X_min, X_max values that may have been passed-in in the SetupDict
                self.X_max = 0.1  # Have to override any other X_min, X_max values that may have been passed-in in the SetupDict
            ##########################################
            ##########################################

            ##########################################
            ##########################################
            if "YaxisAutoscaleFlag" in SetupDict:
                self.YaxisAutoscaleFlag = self.PassThrough0and1values_ExitProgramOtherwise("YaxisAutoscaleFlag", SetupDict["YaxisAutoscaleFlag"])
            else:
                self.YaxisAutoscaleFlag = 1

            if PrintInfoForDebuggingFlag == 1: print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, __ProcessVariablesThatCanBeLiveUpdated: YaxisAutoscaleFlag: " + str(self.YaxisAutoscaleFlag))

            if self.YaxisAutoscaleFlag == 1:
                self.Y_min = 0  # Have to override any other X_min, X_max values that may have been passed-in in the SetupDict
                self.Y_max = 0.1  # Have to override any other X_min, X_max values that may have been passed-in in the SetupDict
            ##########################################
            ##########################################

            ##########################################
            ##########################################
            if "XaxisDrawnAtBottomOfGraph" in SetupDict:
                self.XaxisDrawnAtBottomOfGraph = self.PassThrough0and1values_ExitProgramOtherwise("XaxisDrawnAtBottomOfGraph", SetupDict["XaxisDrawnAtBottomOfGraph"])
            else:
                self.XaxisDrawnAtBottomOfGraph = 1

            if PrintInfoForDebuggingFlag == 1: print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, __ProcessVariablesThatCanBeLiveUpdated: XaxisDrawnAtBottomOfGraph: " + str(self.XaxisDrawnAtBottomOfGraph))
            ##########################################
            ##########################################

            ##########################################
            ##########################################
            if "ShowLegendFlag" in SetupDict:
                self.ShowLegendFlag = self.PassThrough0and1values_ExitProgramOtherwise("ShowLegendFlag", SetupDict["ShowLegendFlag"])
            else:
                self.ShowLegendFlag = 0

            if PrintInfoForDebuggingFlag == 1: print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, __ProcessVariablesThatCanBeLiveUpdated: ShowLegendFlag: " + str(self.ShowLegendFlag))
            ##########################################
            ##########################################

            ##########################################
            ##########################################
            if "XaxisLabelString" in SetupDict:
                self.XaxisLabelString = str(SetupDict["XaxisLabelString"])
            else:
                self.XaxisLabelString = ""

            if PrintInfoForDebuggingFlag == 1: print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, __ProcessVariablesThatCanBeLiveUpdated: XaxisLabelString: " + str(self.XaxisLabelString))
            ##########################################
            ##########################################

            ##########################################
            ##########################################
            if "YaxisLabelString" in SetupDict:
                self.YaxisLabelString = str(SetupDict["YaxisLabelString"])
            else:
                self.YaxisLabelString = ""

            if PrintInfoForDebuggingFlag == 1: print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, __ProcessVariablesThatCanBeLiveUpdated: YaxisLabelString: " + str(self.YaxisLabelString))
            ##########################################
            ##########################################

            ##########################################
            ##########################################

            ##########################################
            if "CurvesToPlotNamesAndColorsDictOfLists" in SetupDict:
                self.CurvesToPlotNamesAndColorsDictOfLists = SetupDict["CurvesToPlotNamesAndColorsDictOfLists"]
            else:
                self.CurvesToPlotNamesAndColorsDictOfLists = dict([(list(), "NameList"), (list(), "ColorList")])

            if PrintInfoForDebuggingFlag == 1: print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, __ProcessVariablesThatCanBeLiveUpdated: CurvesToPlotNamesAndColorsDictOfLists: " + str(self.CurvesToPlotNamesAndColorsDictOfLists))
            ##########################################

            ##########################################
            self.CurvesToPlotDictOfDicts = dict()

            if "NameList" in self.CurvesToPlotNamesAndColorsDictOfLists:
                NameList = self.CurvesToPlotNamesAndColorsDictOfLists["NameList"]

                if "ColorList" in self.CurvesToPlotNamesAndColorsDictOfLists:
                    ColorList = self.CurvesToPlotNamesAndColorsDictOfLists["ColorList"]

                    if "MarkerSizeList" in self.CurvesToPlotNamesAndColorsDictOfLists:
                        MarkerSizeList = self.CurvesToPlotNamesAndColorsDictOfLists["MarkerSizeList"]
                    else:
                        MarkerSizeList = [3] * len(NameList)

                    if "LineWidthList" in self.CurvesToPlotNamesAndColorsDictOfLists:
                        LineWidthList = self.CurvesToPlotNamesAndColorsDictOfLists["LineWidthList"]
                    else:
                        LineWidthList = [3] * len(NameList)

                    if "IncludeInXaxisAutoscaleCalculationList" in self.CurvesToPlotNamesAndColorsDictOfLists:
                        IncludeInXaxisAutoscaleCalculationList = self.CurvesToPlotNamesAndColorsDictOfLists["IncludeInXaxisAutoscaleCalculationList"]
                    else:
                        IncludeInXaxisAutoscaleCalculationList = [1] * len(NameList)

                    if "IncludeInYaxisAutoscaleCalculationList" in self.CurvesToPlotNamesAndColorsDictOfLists:
                        IncludeInYaxisAutoscaleCalculationList = self.CurvesToPlotNamesAndColorsDictOfLists["IncludeInYaxisAutoscaleCalculationList"]
                    else:
                        IncludeInYaxisAutoscaleCalculationList = [1] * len(NameList)

                    if len(NameList) == len(ColorList) \
                            and len(NameList) == len(MarkerSizeList) \
                            and len(NameList) == len(LineWidthList) \
                            and len(NameList) == len(IncludeInXaxisAutoscaleCalculationList) \
                            and len(NameList) == len(IncludeInYaxisAutoscaleCalculationList):

                        for counter, element in enumerate(NameList):
                            self.AddCurveToPlot(NameList[counter],
                                                ColorList[counter],
                                                MarkerSizeList[counter],
                                                LineWidthList[counter],
                                                IncludeInXaxisAutoscaleCalculationList[counter],
                                                IncludeInYaxisAutoscaleCalculationList[counter])

                    else:
                        print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, __ProcessVariablesThatCanBeLiveUpdated: Error, 'NameList','CurveList','MarkerSizeList', and 'LineWidthList' must be the same length in self.CurvesToPlotNamesAndColorsDictOfLists.")
                        return 0
                else:
                    print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, __ProcessVariablesThatCanBeLiveUpdated: Error, 'CurveList' key must be in self.CurvesToPlotNamesAndColorsDictOfLists.")
                    return 0
            else:
                print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, __ProcessVariablesThatCanBeLiveUpdated: Error, 'NameList' key must be in self.CurvesToPlotNamesAndColorsDictOfLists.")
                return 0
            ##########################################

            ##########################################
            ##########################################

            ##########################################
            ##########################################
            self.AxesAllLines_IDforCreateLine = [-1]*(1 + 1 + self.XaxisNumberOfTickMarks + self.YaxisNumberOfTickMarks)
            self.AxesAllText_IDforCreateText = [-1]*(1 + 1 + self.XaxisNumberOfTickMarks + self.YaxisNumberOfTickMarks + len(self.CurvesToPlotNamesAndColorsDictOfLists["NameList"])) #Adding in the legend text
            ##########################################
            ##########################################

            ##########################################
            ##########################################
            if "WatchdogTimerDurationSeconds_ExpirationWillEndStandAlonePlottingProcess" in SetupDict:
                self.WatchdogTimerDurationSeconds_ExpirationWillEndStandAlonePlottingProcess = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("WatchdogTimerDurationSeconds_ExpirationWillEndStandAlonePlottingProcess",
                                                                                                                                                       SetupDict["WatchdogTimerDurationSeconds_ExpirationWillEndStandAlonePlottingProcess"], 0.0, 1000.0)
            else:
                self.WatchdogTimerDurationSeconds_ExpirationWillEndStandAlonePlottingProcess = 0.0

            if PrintInfoForDebuggingFlag == 1: print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, __ProcessVariablesThatCanBeLiveUpdated: WatchdogTimerDurationSeconds_ExpirationWillEndStandAlonePlottingProcess: " + str(self.WatchdogTimerDurationSeconds_ExpirationWillEndStandAlonePlottingProcess))
            ##########################################
            ##########################################

            ##########################################
            ##########################################
            if "StandAlonePlottingProcess_TimeToSleepEachLoop" in SetupDict:

                ##########################################
                if self.OSnameStr == "windows":
                    self.StandAlonePlottingProcess_TimeToSleepEachLoop = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("StandAlonePlottingProcess_TimeToSleepEachLoop", SetupDict["StandAlonePlottingProcess_TimeToSleepEachLoop"], 0.001, 1.0)
                ##########################################

                ##########################################
                elif self.OSnameStr == "pi":
                    self.StandAlonePlottingProcess_TimeToSleepEachLoop = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("StandAlonePlottingProcess_TimeToSleepEachLoop", SetupDict["StandAlonePlottingProcess_TimeToSleepEachLoop"], 0.005, 1.0)  # Pi can't handle below 0.005
                ##########################################

                ##########################################
                else:
                    self.StandAlonePlottingProcess_TimeToSleepEachLoop = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("StandAlonePlottingProcess_TimeToSleepEachLoop", SetupDict["StandAlonePlottingProcess_TimeToSleepEachLoop"], 0.001, 1.0)
                ##########################################

            else:
                self.StandAlonePlottingProcess_TimeToSleepEachLoop = 0.030

            if PrintInfoForDebuggingFlag == 1: print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, __ProcessVariablesThatCanBeLiveUpdated: StandAlonePlottingProcess_TimeToSleepEachLoop: " + str(self.StandAlonePlottingProcess_TimeToSleepEachLoop))
            ##########################################
            ##########################################

            ##########################################
            ##########################################
            if "AxisMinMaxEpsilon" in SetupDict:
                self.AxisMinMaxEpsilon = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("AxisMinMaxEpsilon", SetupDict["AxisMinMaxEpsilon"], 0.000001, 1000.0)
            else:
                self.AxisMinMaxEpsilon = 0.000001

            if PrintInfoForDebuggingFlag == 1: print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, __ProcessVariablesThatCanBeLiveUpdated: AxisMinMaxEpsilon: " + str(self.AxisMinMaxEpsilon))
            ##########################################
            ##########################################

            ##########################################
            ##########################################
            if "GraphNumberOfLeadingZeros" in SetupDict:
                self.GraphNumberOfLeadingZeros = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GraphNumberOfLeadingZeros", SetupDict["GraphNumberOfLeadingZeros"], 0.0, 10.0))
            else:
                self.GraphNumberOfLeadingZeros = 2

            if PrintInfoForDebuggingFlag == 1: print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, __ProcessVariablesThatCanBeLiveUpdated: GraphNumberOfLeadingZeros: " + str(self.GraphNumberOfLeadingZeros))
            ##########################################
            ##########################################

            ##########################################
            ##########################################
            if "GraphNumberOfDecimalPlaces" in SetupDict:
                self.GraphNumberOfDecimalPlaces = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GraphNumberOfDecimalPlaces", SetupDict["GraphNumberOfDecimalPlaces"], 0.0, 10.0))
            else:
                self.GraphNumberOfDecimalPlaces = 5

            if PrintInfoForDebuggingFlag == 1: print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, __ProcessVariablesThatCanBeLiveUpdated: GraphNumberOfDecimalPlaces: " + str(self.GraphNumberOfDecimalPlaces))
            ##########################################
            ##########################################

            ##########################################
            ##########################################
            if "SavePlot_DirectoryPath" in SetupDict:
                self.SavePlot_DirectoryPath = str(SetupDict["SavePlot_DirectoryPath"])
            else:
                self.SavePlot_DirectoryPath = os.path.join(os.getcwd(), "SavedImages")

            if PrintInfoForDebuggingFlag == 1: print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, __ProcessVariablesThatCanBeLiveUpdated: SavePlot_DirectoryPath: " + str(self.SavePlot_DirectoryPath))
            ##########################################
            ##########################################

            ##########################################
            ##########################################
            if "KeepPlotterWindowAlwaysOnTopFlag" in SetupDict:
                self.KeepPlotterWindowAlwaysOnTopFlag = self.PassThrough0and1values_ExitProgramOtherwise("KeepPlotterWindowAlwaysOnTopFlag", SetupDict["KeepPlotterWindowAlwaysOnTopFlag"])
            else:
                self.KeepPlotterWindowAlwaysOnTopFlag = 0

            if PrintInfoForDebuggingFlag == 1: print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, __ProcessVariablesThatCanBeLiveUpdated: KeepPlotterWindowAlwaysOnTopFlag: " + str(self.KeepPlotterWindowAlwaysOnTopFlag))
            ##########################################
            ##########################################

            ##########################################
            ##########################################
            if "RemoveTitleBorderCloseButtonAndDisallowWindowMoveFlag" in SetupDict:
                self.RemoveTitleBorderCloseButtonAndDisallowWindowMoveFlag = self.PassThrough0and1values_ExitProgramOtherwise("RemoveTitleBorderCloseButtonAndDisallowWindowMoveFlag", SetupDict["RemoveTitleBorderCloseButtonAndDisallowWindowMoveFlag"])
            else:
                self.RemoveTitleBorderCloseButtonAndDisallowWindowMoveFlag = 0

            if PrintInfoForDebuggingFlag == 1: print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, __ProcessVariablesThatCanBeLiveUpdated: RemoveTitleBorderCloseButtonAndDisallowWindowMoveFlag: " + str(self.RemoveTitleBorderCloseButtonAndDisallowWindowMoveFlag))
            ##########################################
            ##########################################

            ##########################################
            ##########################################
            if "AllowResizingOfWindowFlag" in SetupDict:
                self.AllowResizingOfWindowFlag = self.PassThrough0and1values_ExitProgramOtherwise("AllowResizingOfWindowFlag", SetupDict["AllowResizingOfWindowFlag"])
            else:
                self.AllowResizingOfWindowFlag = 1

            if PrintInfoForDebuggingFlag == 1: print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, __ProcessVariablesThatCanBeLiveUpdated: AllowResizingOfWindowFlag: " + str(self.AllowResizingOfWindowFlag))
            ##########################################
            ##########################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

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
            print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, __ProcessVariablesThatCanBeLiveUpdated: Exceptions: %s" % exceptions)
            #traceback.print_exc()
            return 0
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
    def GetCPUandMemoryUsageOfProcessByPID(self, Process_PID, PrintInfoForDebuggingFlag=0):

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        try:
            ProcessObject = psutil.Process(Process_PID)

            if self.GetCPUandMemoryUsageOfProcessByPID_MeasurementWarmedUpFlag == 0:
                ProcessObject.cpu_percent(interval=0.1)  # First call returns 0.0 but wamrs up the measurement.
                self.GetCPUandMemoryUsageOfProcessByPID_MeasurementWarmedUpFlag = 1

            CPUusage_Percent = ProcessObject.cpu_percent(interval=0.0)  # Use a short interval, 0.0 for non-blocking

            MemoryInfo = ProcessObject.memory_info()
            MemoryUsage_MB = MemoryInfo.rss / (1024 * 1024)  # Convert to MB

            MemoryUsage_Percent = ProcessObject.memory_percent()

            DictToReturn = dict([("CPUusage_Percent", round(CPUusage_Percent, 5)),
                                 ("MemoryUsage_Percent", round(MemoryUsage_Percent, 5)),
                                 ("MemoryUsage_MB", round(MemoryUsage_MB, 5))])

            ##########################################################################################################
            ##########################################################################################################
            if PrintInfoForDebuggingFlag == 1:
                print("GetCPUandMemoryUsageOfProcessByPID: For Process_PID = " + str(Process_PID) + "DictToReturn = " + str(DictToReturn))
            ##########################################################################################################
            ##########################################################################################################

            return DictToReturn
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        except:
            exceptions = sys.exc_info()[0]
            print("GetCPUandMemoryUsageOfProcessByPID, exceptions: %s" % exceptions)
            # traceback.print_exc()

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
    @staticmethod
    def GetOSnameStr(PrintInfoForDebuggingFlag=0):

        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            if platform.system() == "Linux":

                if "raspberrypi" in platform.uname():  # os.uname() doesn't work in windows
                    OSnameStr = "pi"

                else:
                    OSnameStr = "linux"
            ##########################################################################################################

            ##########################################################################################################
            elif platform.system() == "Windows":
                OSnameStr = "windows"
            ##########################################################################################################

            ##########################################################################################################
            elif platform.system() == "Darwin":
                OSnameStr = "mac"
            ##########################################################################################################

            ##########################################################################################################
            else:
                OSnameStr = "other"
            ##########################################################################################################

            ##########################################################################################################
            if PrintInfoForDebuggingFlag == 1:
                print("GetOSnameStr: The OS is: " + OSnameStr)
            ##########################################################################################################

            ##########################################################################################################
            return OSnameStr
            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        except:

            exceptions = sys.exc_info()[0]
            print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class: GetOSnameStr, exceptions: %s" % exceptions)
            # traceback.print_exc()
            return ""

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
    def WatchdogTimerCheck(self):

        #############################################
        if self.WatchdogTimerDurationSeconds_ExpirationWillEndStandAlonePlottingProcess > 0.0:
            self.TimeIntoWatchdogTimer = self.CurrentTime_CalculatedFromStandAlonePlottingProcess - self.LastTime_CalculatedFromStandAlonePlottingProcess

            if self.TimeIntoWatchdogTimer >= self.WatchdogTimerDurationSeconds_ExpirationWillEndStandAlonePlottingProcess:
                print("***** MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, Watchdog fired, self.TimeIntoWatchdogTimer = " + str(self.TimeIntoWatchdogTimer) + "seconds *****")
                self.EXIT_PROGRAM_FLAG = 1
        #############################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## unicorn
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def StandAlonePlottingProcess(self, MultiprocessingQueue_Rx_Local, MultiprocessingQueue_Tx_Local, SetupDict):

        print("Entering MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class StandAlonePlottingProcess.")

        ##########################################
        self.EXIT_PROGRAM_FLAG = 0
        self.GUI_ready_to_be_updated_flag = 0
        ##########################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        SuccessFlag = self.__ProcessVariablesThatCanNOTbeLiveUpdated(SetupDict, PrintInfoForDebuggingFlag = 1)
        if SuccessFlag == 0:
            self.EXIT_PROGRAM_FLAG = 1

        self.RootGeometryHasBeenModified_HasThisEventFiredBeforeFlag = 0
        SuccessFlag = self.__ProcessVariablesThatCanBeLiveUpdated(SetupDict, PrintInfoForDebuggingFlag = 1)
        if SuccessFlag == 0:
            self.EXIT_PROGRAM_FLAG = 1

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

        ##########################################
        self.OSnameStr = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class.GetOSnameStr()

        self.SelfPID = os.getpid()
        ##########################################

        ##########################################
        self.PrintToGui_Label_TextInputHistory_List = [" "] * self.NumberOfPrintLines
        self.PrintToGui_Label_TextInput_Str = ""
        ##########################################

        ##########################################
        self.TKinter_LightGreenColor = '#%02x%02x%02x' % (150, 255, 150)  # RGB
        self.TKinter_LightRedColor = '#%02x%02x%02x' % (255, 150, 150)  # RGB
        self.TKinter_LightYellowColor = '#%02x%02x%02x' % (255, 255, 150)  # RGB
        self.TKinter_DefaultGrayColor = '#%02x%02x%02x' % (240, 240, 240)  # RGB
        ##########################################

        ##########################################
        self.GraphBoxOutline_X0 = 50  # Offset from the Canvas object so that there's room for the axis-labels
        self.GraphBoxOutline_Y0 = 50  # Offset from the Canvas object so that there's room for the axis-labels
        ##########################################

        ##########################################
        self.CurrentTime_CalculatedFromGUIthread = -11111.0
        self.LastTime_CalculatedFromGUIthread = -11111.0
        self.StartingTime_CalculatedFromGUIthread = -11111.0
        self.LoopFrequency_CalculatedFromGUIthread = -11111.0
        self.LoopDeltaT_CalculatedFromGUIthread = -11111.0
        ##########################################

        ##########################################
        self.CurrentTime_CalculatedFromStandAlonePlottingProcess = -11111.0
        self.LastTime_CalculatedFromStandAlonePlottingProcess = -11111.0
        self.StartingTime_CalculatedFromStandAlonePlottingProcess = -11111.0
        self.LoopFrequency_CalculatedFromStandAlonePlottingProcess = -11111.0
        self.LoopDeltaT_CalculatedFromStandAlonePlottingProcess = -11111.0

        self.TimeIntoWatchdogTimer = 0.0
        ##########################################

        ##########################################
        self.StandAlonePlottingProcess_ReadyForWritingFlag = 0
        ##########################################

        ##########################################
        self.FreezePlotFlag = 0
        self.SavePlotFlag = 0
        ##########################################

        ##########################################
        self.MemoryUsageOfProcessByPID_Dict = dict([("CPUusage_Percent", -1),
                                                    ("MemoryUsage_Percent", -1),
                                                    ("MemoryUsage_MB", -1)])
        ##########################################

        ##########################################
        self.MostRecentDataDict = dict()
        ##########################################

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

        ##########################################
        self.GetCPUandMemoryUsageOfProcessByPID_OPEN_FLAG = 0
        ##########################################

        ##########################################
        try:
            if GetCPUandMemoryUsageOfProcessByPID_ModuleImportedFlag == 1 and self.EXIT_PROGRAM_FLAG == 0:
                self.GetCPUandMemoryUsageOfProcessByPID_Object = GetCPUandMemoryUsageOfProcessByPID_ReubenPython3Class(dict([("Process_PID_Integer", self.SelfPID)]))
                self.GetCPUandMemoryUsageOfProcessByPID_OPEN_FLAG = self.GetCPUandMemoryUsageOfProcessByPID_Object.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("GetCPUandMemoryUsageOfProcessByPID_ReubenPython3ClassObject __init__, exceptions: %s" % exceptions)
            traceback.print_exc()
        ##########################################

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

        if self.EXIT_PROGRAM_FLAG == 0:
            self.StartGUI()

        self.CTRLc_RegisterHandlerFunction()

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        self.StartingTime_CalculatedFromStandAlonePlottingProcess = self.getPreciseSecondsTimeStampString()
        self.LastTime_CalculatedFromStandAlonePlottingProcess = self.StartingTime_CalculatedFromStandAlonePlottingProcess

        self.StandAlonePlottingProcess_ReadyForWritingFlag = 1

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        while self.EXIT_PROGRAM_FLAG == 0:

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            try:

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                self.CurrentTime_CalculatedFromStandAlonePlottingProcess = self.getPreciseSecondsTimeStampString() - self.StartingTime_CalculatedFromStandAlonePlottingProcess
                
                self.WatchdogTimerCheck()
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                if self.GetCPUandMemoryUsageOfProcessByPID_OPEN_FLAG == 1:
                    GetCPUandMemoryUsageOfProcessByPID_MostRecentDict = self.GetCPUandMemoryUsageOfProcessByPID_Object.GetMostRecentDataDict()

                    if "MemoryUsageOfProcessByPID_Dict" in GetCPUandMemoryUsageOfProcessByPID_MostRecentDict:
                        self.MemoryUsageOfProcessByPID_Dict = GetCPUandMemoryUsageOfProcessByPID_MostRecentDict["MemoryUsageOfProcessByPID_Dict"]
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                while not MultiprocessingQueue_Rx_Local.empty():

                    ##########################################################################################################
                    ##########################################################################################################
                    self.UpdateFrequencyCalculation_CalculatedFromStandAlonePlottingProcess() #ONLY UPDATE IF WE GET A DATA PACKET
                    ##########################################################################################################
                    ##########################################################################################################

                    ##########################################################################################################
                    ##########################################################################################################
                    inputDict = MultiprocessingQueue_Rx_Local.get(FALSE)  # for queue, non-blocking with "FALSE" argument, could also use MultiprocessingQueue_Rx_Local.get_nowait() for non-blocking
                    ##########################################################################################################
                    ##########################################################################################################

                    ##########################################################################################################
                    ##########################################################################################################
                    if "YaxisAutoscaleFlag" in inputDict: #Check if a SetupDict is being passed-in
                        self.__ProcessVariablesThatCanBeLiveUpdated(inputDict, PrintInfoForDebuggingFlag=0)
                    ##########################################################################################################
                    ##########################################################################################################

                    ##########################################################################################################
                    ##########################################################################################################
                    else:

                        ##########################################################################################################
                        if "EndStandAloneProcessFlag" in inputDict:
                            self.EXIT_PROGRAM_FLAG = 1
                        ##########################################################################################################

                        ##########################################################################################################
                        if "ToggleAutoscale" in inputDict:
                            self.ToggleAutoscale()
                        ##########################################################################################################

                        ##########################################################################################################
                        if "FreezePlot" in inputDict:
                            self.FreezePlot()
                        ##########################################################################################################

                        ##########################################################################################################
                        if "UnfreezePlot" in inputDict:
                            self.UnfreezePlot()
                        ##########################################################################################################

                        ##########################################################################################################
                        if "ToggleFreezePlot" in inputDict:
                            self.ToggleFreezePlot()
                        ##########################################################################################################

                        ##########################################################################################################
                        if "SavePlot" in inputDict:
                            self.SavePlotFlag = 1
                        ##########################################################################################################

                        ##########################################################################################################
                        if "ResetMinAndMax" in inputDict:
                            self.ResetMinAndMax()
                        ##########################################################################################################

                        ##########################################################################################################
                        if "ClearPlot" in inputDict:
                            self.ClearPlot()
                        ##########################################################################################################

                        ##########################################################################################################
                        else: #MAIN DATA PLOTTING CALL

                            if "CurveName" in inputDict:

                                CurveName = inputDict["CurveName"]
                                x = inputDict["x"]
                                y = inputDict["y"]

                                self.__AddPointOrListOfPointsToPlot(CurveName, x, y)
                        ##########################################################################################################

                    ##########################################################################################################
                    ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                self.MostRecentDataDict = dict([("StandAlonePlottingProcess_ReadyForWritingFlag", self.StandAlonePlottingProcess_ReadyForWritingFlag)])
                MultiprocessingQueue_Tx_Local.put(self.MostRecentDataDict.copy())

                # ("CurvesToPlotDictOfDicts", self.CurvesToPlotDictOfDicts), 07/15/25: Not using this data (and it's a lot), so let's remove it for now.
                # deepcopy is required (beyond .copy() ) because self.MostRecentDataDict contains a dict.
                # MultiprocessingQueue_Tx_Local.put(deepcopy(self.MostRecentDataDict))
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                time.sleep(self.StandAlonePlottingProcess_TimeToSleepEachLoop)
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
            except:
                exceptions = sys.exc_info()[0]
                print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, StandAlonePlottingProcess, exceptions: %s" % exceptions)
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
        try:
            if self.GetCPUandMemoryUsageOfProcessByPID_OPEN_FLAG == 1:
                self.GetCPUandMemoryUsageOfProcessByPID_Object.ExitProgram_Callback()
        except:
            pass
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ########################################################################################################## Drain all remaining items in Queues OR ELSE THIS THREAD WON'T DRAIN.
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        try:

            '''
            ##########################################################################################################
            ##########################################################################################################
            while not self.MultiprocessingQueue_Rx.empty():
                DummyToDrainRemainingItemsInRxQueue = self.MultiprocessingQueue_Rx.get_nowait()
                #time.sleep(0.001)  #07/16/25: Might need to put this back to close properly.

            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            while not self.MultiprocessingQueue_Tx.empty():
                DummyToDrainRemainingItemsInTxQueue = self.MultiprocessingQueue_Tx.get_nowait()
                #time.sleep(0.001)  #07/16/25: Might need to put this back to close properly.

            ##########################################################################################################
            ##########################################################################################################
            '''

            #'''
            ##########################################################################################################
            ##########################################################################################################
            while True:
                try:
                    DummyToDrainRemainingItemsInRxQueue = self.MultiprocessingQueue_Rx.get_nowait()
                    #time.sleep(0.001)  #07/16/25: Might need to put this back to close properly.

                except Empty:
                    break
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            while True:
                try:
                    DummyToDrainRemainingItemsInTxQueue = self.MultiprocessingQueue_Tx.get_nowait()
                    #time.sleep(0.001)  #07/16/25: Might need to put this back to close properly.

                except Empty:
                    break
            ##########################################################################################################
            ##########################################################################################################
            #'''

            self.job_for_another_core.close()  # Added 03/10/25 @ 05:13pm
            self.job_for_another_core.join()  # Added 03/10/25 @ 05:13pm

        except:
            pass
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        print("Exited MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class.")

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
    def SendEndCommandToStandAloneProcess(self):

        try:
            self.MultiprocessingQueue_Rx.put(dict([("EndStandAloneProcessFlag", 1)]))
        except:
            pass

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def SendToggleAutoscaleCommandToStandAloneProcess(self):

        try:
            self.MultiprocessingQueue_Rx.put(dict([("ToggleAutoscale", 1)]))
        except:
            pass

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def SendFreezePlotCommandToStandAloneProcess(self):

        try:
            self.MultiprocessingQueue_Rx.put(dict([("FreezePlot", 1)]))
        except:
            pass

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def SendUnfreezePlotCommandToStandAloneProcess(self):

        try:
            self.MultiprocessingQueue_Rx.put(dict([("UnfreezePlot", 1)]))
        except:
            pass

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def SendToggleFreezePlotCommandToStandAloneProcess(self):

        try:
            self.MultiprocessingQueue_Rx.put(dict([("ToggleFreezePlot", 1)]))
        except:
            pass

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def SendSavePlotCommandToStandAloneProcess(self):

        try:
            self.MultiprocessingQueue_Rx.put(dict([("SavePlot", 1)]))
        except:
            pass

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def SendResetMinAndMaxCommandToStandAloneProcess(self):

        try:
            self.MultiprocessingQueue_Rx.put(dict([("ResetMinAndMax", 1)]))
        except:
            pass

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def SendClearPlotCommandToStandAloneProcess(self):

        try:
            self.MultiprocessingQueue_Rx.put(dict([("ClearPlot", 1)]))
        except:
            pass

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def ExternalAddPointOrListOfPointsToPlot(self, CurveNameStringList, XdataList, YdataList, OverrideCurveAndPointListsMustMatchInLengthFlag=0, PrintInfoForDebuggingFlag=0):

        ###########################################
        if self.IsInputList(CurveNameStringList) == 0:
            CurveNameStringList = [CurveNameStringList]
        ###########################################

        ###########################################
        if self.IsInputList(XdataList) == 0:
            XdataList = [XdataList]
        ###########################################

        ###########################################
        if self.IsInputList(YdataList) == 0:
            YdataList = [YdataList]
        ###########################################

        ###########################################
        if len(XdataList) != len(YdataList):
            print("ExternalAddPointOrListOfPointsToPlot: ERROR, length of XdataList (" + \
                  str(len(XdataList)) + "), and YdataList (" + \
                  str(len(YdataList)) + ") inputs must all match!")

            return
        ###########################################

        ###########################################
        if OverrideCurveAndPointListsMustMatchInLengthFlag == 0:
            if len(CurveNameStringList) != len(XdataList):
                print("ExternalAddPointOrListOfPointsToPlot: ERROR, length of CurveNameString (" +
                      str(len(CurveNameStringList)) + "), XdataList (" + \
                      str(len(XdataList)) + "), and YdataList (" + \
                      str(len(YdataList)) + ") inputs must all match!")

                return
        ###########################################

        ########################################### At this level, we don't have scope to check if CurveNameStringElement is contained in self.CurvesToPlotDictOfDicts
        for CurveIndex, CurveNameString in enumerate(CurveNameStringList):
            self.MultiprocessingQueue_Rx.put(dict([("CurveName", CurveNameString), ("x", XdataList[CurveIndex]), ("y", YdataList[CurveIndex])]))
        ###########################################

        if PrintInfoForDebuggingFlag == 1: print("ExternalAddPointOrListOfPointsToPlot event fired!")

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def ExternalUpdateSetupDict(self, SetupDict):

        if self.IsInputDict(SetupDict) == 1:

            self.MultiprocessingQueue_Rx.put(SetupDict)

        else:
            self.MultiprocessingQueue_Rx.put(dict())

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

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
    ##########################################################################################################
    ##########################################################################################################
    @staticmethod
    def RangeOfFloatNumberOfIncrements_PurePythonNoNumpy(StartValue, StopValue, NumberOfIndices):
        # Reuben modified from https://stackoverflow.com/questions/6683690/making-a-list-of-evenly-spaced-numbers-in-a-certain-range-in-python

        StartValue = float(StartValue)  # Otherwise we'll get incorrect results sometimes.
        StopValue = float(StopValue)  # Otherwise we'll get incorrect results sometimes.
        NumberOfIndices = int(NumberOfIndices)  # Range function only accepts ints

        # ListToReturn = [StopValue + x*(StartValue-StopValue)/(NumberOfIndices-1) for x in range(NumberOfIndices)] #Returns a list in the opposite order from what we want
        ListToReturn = [StopValue + x * (StartValue - StopValue) / (NumberOfIndices - 1) for x in range(NumberOfIndices - 1, -1, -1)]  # Have to change the range inputs to get the correct order in the list

        return ListToReturn
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def TellWhichFileWereIn(self):

        # We used to use this method, but it gave us the root calling file, not the class calling file
        # absolute_file_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        # filename = absolute_file_path[absolute_file_path.rfind("\\") + 1:]

        frame = inspect.stack()[1]
        filename = frame[1][frame[1].rfind("\\") + 1:]
        filename = filename.replace(".py", "")

        return filename
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

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

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def GetMostRecentDataDict(self):

        try:
            if self.MultiprocessingQueue_Tx.empty() != 1:
                return self.MultiprocessingQueue_Tx.get(FALSE)
            else:
                return dict()

        except:
            exceptions = sys.exc_info()[0]
            print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class, GetMostRecentDataDict, Exceptions: %s" % exceptions)
            # traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_CalculatedFromGUIthread(self):

        try:
            self.LoopDeltaT_CalculatedFromGUIthread = self.CurrentTime_CalculatedFromGUIthread - self.LastTime_CalculatedFromGUIthread

            ##########################
            if self.LoopDeltaT_CalculatedFromGUIthread != 0.0:
                self.LoopFrequency_CalculatedFromGUIthread = 1.0 / self.LoopDeltaT_CalculatedFromGUIthread
            ##########################

            self.LastTime_CalculatedFromGUIthread = self.CurrentTime_CalculatedFromGUIthread

        except:
            exceptions = sys.exc_info()[0]
            self.MyPrint_WithoutLogFile("UpdateFrequencyCalculation_CalculatedFromGUIthread ERROR, exceptions: %s" % exceptions)

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_CalculatedFromStandAlonePlottingProcess(self):

        try:
            self.LoopDeltaT_CalculatedFromStandAlonePlottingProcess = self.CurrentTime_CalculatedFromStandAlonePlottingProcess - self.LastTime_CalculatedFromStandAlonePlottingProcess

            ##########################
            if self.LoopDeltaT_CalculatedFromStandAlonePlottingProcess != 0.0:
                self.LoopFrequency_CalculatedFromStandAlonePlottingProcess = 1.0 / self.LoopDeltaT_CalculatedFromStandAlonePlottingProcess
            ##########################

            self.LastTime_CalculatedFromStandAlonePlottingProcess = self.CurrentTime_CalculatedFromStandAlonePlottingProcess

        except:
            exceptions = sys.exc_info()[0]
            self.MyPrint_WithoutLogFile("UpdateFrequencyCalculation_CalculatedFromStandAlonePlottingProcess ERROR, exceptions: %s" % exceptions)

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def AddCurveToPlot(self, CurveName, Color, MarkerSize=3, LineWidth=3, IncludeInXaxisAutoscaleCalculation=1, IncludeInYaxisAutoscaleCalculation=1):

        if CurveName not in self.CurvesToPlotDictOfDicts:

            self.CurvesToPlotDictOfDicts[CurveName] = (dict([("CurveName", CurveName),
                                                             ("Color", Color),
                                                             ("MarkerSize", MarkerSize),
                                                             ("LineWidth", LineWidth),
                                                             ("IncludeInXaxisAutoscaleCalculation", IncludeInXaxisAutoscaleCalculation),
                                                             ("IncludeInYaxisAutoscaleCalculation", IncludeInYaxisAutoscaleCalculation),
                                                             ("PointToDrawList", []),
                                                             ("PointToDrawList_IDforCreateOval", [-1]*self.NumberOfDataPointToPlot),
                                                             ("PointToDrawList_IDforCreateLine", [-1]*self.NumberOfDataPointToPlot),
                                                             ("AddPointOrListOfPointsToPlot_TimeLastCalled", -11111.0)]))
            return 1

        else:
            self.MyPrint_WithoutLogFile("AddCurveToPlot ERROR: '" + CurveName + "' already in the CurvesToPlotDictOfDicts.")
            return 0

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def __AddPointOrListOfPointsToPlot(self, CurveName, x, y, PrintCallingFunctionTooQuicklyWarningFlag=0):

        if self.IsInputList(x) == 0:
            x = list([x])

        if self.IsInputList(y) == 0:
            y = list([y])

        # print("__AddPointOrListOfPointsToPlot: CurveName = " + str(CurveName) + ",\nx = " + str(x) + ",\ny = " + str(y))

        temp_AddPointOrListOfPointsToPlot_CurrentTime = self.getPreciseSecondsTimeStampString()

        if temp_AddPointOrListOfPointsToPlot_CurrentTime - self.CurvesToPlotDictOfDicts[CurveName]["AddPointOrListOfPointsToPlot_TimeLastCalled"] >= self.GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents / 1000.0:

            if CurveName in self.CurvesToPlotDictOfDicts:
                ############################################
                for i in range(0, len(x)):  # Cycle through points in list
                    # print("i: " + str(i) + ", x: " + str(x[i]) + ", y: " + str(y[i]))

                    if len(self.CurvesToPlotDictOfDicts[CurveName]["PointToDrawList"]) < self.NumberOfDataPointToPlot:
                        self.CurvesToPlotDictOfDicts[CurveName]["PointToDrawList"].append([x[i], y[i]])

                    else:
                        self.CurvesToPlotDictOfDicts[CurveName]["PointToDrawList"].append(self.CurvesToPlotDictOfDicts[CurveName]["PointToDrawList"].pop(0))
                        self.CurvesToPlotDictOfDicts[CurveName]["PointToDrawList"][-1] = [x[i], y[i]]

                self.CurvesToPlotDictOfDicts[CurveName]["AddPointOrListOfPointsToPlot_TimeLastCalled"] = temp_AddPointOrListOfPointsToPlot_CurrentTime

                return 1
                ############################################
            else:
                self.MyPrint_WithoutLogFile("__AddPointOrListOfPointsToPlot ERROR: '" + CurveName + "' not in CurvesToPlotDictOfDicts.")
                return 0
        else:
            if PrintCallingFunctionTooQuicklyWarningFlag == 1:
                self.MyPrint_WithoutLogFile("__AddPointOrListOfPointsToPlot: ERROR, calling function too quickly (must be less frequently than GUI_RootAfterCallbackInterval_Milliseconds of " + str(self.GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents) + " ms).")

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def ExitProgram_Callback(self):

        print("Exiting all threads for MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class object")

        self.EXIT_PROGRAM_FLAG = 1

        self.SendEndCommandToStandAloneProcess()

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def StartGUI(self):

        self.GUI_Thread_ThreadingObject = threading.Thread(target=self.GUI_Thread, daemon=True) #Daemon=True means that the GUI thread is destroyed automatically when the main thread is destroyed.
        self.GUI_Thread_ThreadingObject.start()

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## unicorn
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def RootConfigurationUpdate(self):

        ###################################################
        ###################################################
        self.root.title(self.GraphCanvasWindowTitle)
        self.root.protocol("WM_DELETE_WINDOW", self.ExitProgram_Callback)
        self.root.geometry('%dx%d+%d+%d' % (self.GraphCanvasWidth, self.GraphCanvasHeight + 80, self.GraphCanvasWindowStartingX, self.GraphCanvasWindowStartingY))  # +50 for Debug_Label
        self.root.after(self.GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents, self.__GUI_update_clock)
        ###################################################
        ###################################################

        ###################################################
        ###################################################
        self.root.resizable(bool(self.AllowResizingOfWindowFlag), bool(self.AllowResizingOfWindowFlag))  #horizontal, vertical
        self.root.overrideredirect(bool(self.RemoveTitleBorderCloseButtonAndDisallowWindowMoveFlag))  # Removes title bar, border, and close-button. Disallows movement of the window.
        self.root.wm_attributes('-topmost', bool(self.KeepPlotterWindowAlwaysOnTopFlag))
        ###################################################
        ###################################################

        ################################################### SET THE DEFAULT FONT FOR ALL WIDGETS CREATED AFTTER/BELOW THIS CALL
        ###################################################
        default_font = tkFont.nametofont("TkDefaultFont")  # TkTextFont, TkFixedFont
        default_font.configure(size=8)
        self.root.option_add("*Font", default_font)
        ###################################################
        ###################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def GUI_Thread(self):

        ###################################################
        ###################################################
        self.root = Tk()
        ###################################################
        ###################################################

        ###################################################
        ###################################################
        self.myFrame = Frame(self.root, bg="white")
        self.myFrame.grid()
        ###################################################
        ###################################################

        ###################################################
        ###################################################
        self.RootConfigurationUpdate()
        ###################################################
        ###################################################

        ###################################################
        ###################################################
        self.LineIDlist = []
        ###################################################
        ###################################################

        ###################################################
        ###################################################
        self.CanvasForDrawingGraph = Canvas(self.myFrame, width=self.GraphCanvasWidth, height=self.GraphCanvasHeight, bg="white")
        self.CanvasForDrawingGraph["highlightthickness"] = 0  # Remove light grey border around the Canvas
        self.CanvasForDrawingGraph["bd"] = 0  # Setting "bd", along with "highlightthickness" to 0 makes the Canvas be in the (0,0) pixel location instead of offset by those thicknesses
        '''
        From https://stackoverflow.com/questions/4310489/how-do-i-remove-the-light-grey-border-around-my-canvas-widget
        The short answer is, the Canvas has two components which affect the edges: the border (borderwidth attribute) and highlight ring (highlightthickness attribute).
        If you have a border width of zero and a highlight thickness of zero, the canvas coordinates will begin at 0,0. Otherwise, these two components of the canvas infringe upon the coordinate space.
        What I most often do is set these attributes to zero. Then, if I actually want a border I'll put that canvas inside a frame and give the frame a border.
        '''

        self.CanvasForDrawingGraph.bind("<Button-1>", lambda event: self.OnCanvasClickCallbackFunction(event))
        self.CanvasForDrawingGraph.grid(row=0, column=0, padx=0, pady=0)
        ###################################################
        ###################################################

        ###################################################
        ###################################################
        self.Debug_Label = Label(self.myFrame, text="Debug_Label", width=100, bg="white")
        self.Debug_Label.grid(row=1, column=0, padx=0, pady=0, columnspan=1, rowspan=1, sticky="w")
        ###################################################
        ###################################################

        ###################################################
        ###################################################
        self.PlotControlsFrame = Frame(self.myFrame, bg="white")
        self.PlotControlsFrame.grid(row=2, column=0, padx=1, pady=1, columnspan=1, rowspan=1, sticky="w")
        ###################################################
        ###################################################

        self.ButtonWidth = 15

        ###################################################
        ###################################################
        self.ToggleAutoscale_Button = Button(self.PlotControlsFrame, text='Toggle Autoscale', state="normal", width=self.ButtonWidth, font=("Helvetica", 8), command=lambda i=1: self.ToggleAutoscale_ButtonResponse())
        self.ToggleAutoscale_Button.grid(row=0, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
        ###################################################
        ###################################################

        ###################################################
        ###################################################
        self.ToggleFreezePlot_Button = Button(self.PlotControlsFrame, text='Freeze Plot', state="normal", width=self.ButtonWidth, font=("Helvetica", 8), command=lambda i=1: self.ToggleFreezePlot_ButtonResponse())
        self.ToggleFreezePlot_Button.grid(row=1, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
        ###################################################
        ###################################################

        ###################################################
        ###################################################
        self.SavePlot_Button = Button(self.PlotControlsFrame, text='Save Plot', state="normal", width=self.ButtonWidth, font=("Helvetica", 8), command=lambda i=1: self.SavePlot_ButtonResponse())
        self.SavePlot_Button.grid(row=0, column=1, padx=1, pady=1, columnspan=1, rowspan=1)

        if self.pyautogui_ModuleImportedFlag == 0:
            self.SavePlot_Button["state"] = "disabled"
            self.SavePlot_Button["text"] = "NoSave"
        ###################################################
        ###################################################

        ###################################################
        ###################################################
        self.Y_min_label = Label(self.PlotControlsFrame, text="Y_min", width=15, bg="white")
        self.Y_min_label.grid(row=0, column=3, padx=1, pady=1, columnspan=1, rowspan=1)

        self.Y_min_StringVar = StringVar()
        self.Y_min_StringVar.set(float(self.RemoveLeadingZerosFromString(self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.Y_min, self.GraphNumberOfLeadingZeros, self.GraphNumberOfDecimalPlaces))))
        self.Y_min_Entry = Entry(self.PlotControlsFrame, width=15, state="normal", textvariable=self.Y_min_StringVar)
        self.Y_min_Entry.grid(row=0, column=4, padx=1, pady=1, columnspan=1, rowspan=1)
        self.Y_min_Entry.bind('<Return>', lambda event: self.Y_min_Entry_Response(event))
        ###################################################
        ###################################################

        ###################################################
        ###################################################
        self.Y_max_label = Label(self.PlotControlsFrame, text="Y_max", width=15, bg="white")
        self.Y_max_label.grid(row=1, column=3, padx=1, pady=1, columnspan=1, rowspan=1)

        self.Y_max_StringVar = StringVar()
        self.Y_max_StringVar.set(float(self.RemoveLeadingZerosFromString(self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.Y_max, self.GraphNumberOfLeadingZeros, self.GraphNumberOfDecimalPlaces))))
        self.Y_max_Entry = Entry(self.PlotControlsFrame, width=15, state="normal", textvariable=self.Y_max_StringVar)
        self.Y_max_Entry.grid(row=1, column=4, padx=1, pady=1, columnspan=1, rowspan=1)
        self.Y_max_Entry.bind('<Return>', lambda event: self.Y_max_Entry_Response(event))
        ###################################################
        ###################################################

        ###################################################
        ###################################################
        self.ResetMinAndMax_Button = Button(self.PlotControlsFrame, text='ResetMinMax', state="normal", width=self.ButtonWidth, font=("Helvetica", 8), command=lambda i=1: self.ResetMinAndMax_ButtonResponse())
        self.ResetMinAndMax_Button.grid(row=0, column=7, padx=1, pady=1, columnspan=1, rowspan=1)
        ###################################################
        ###################################################

        ###################################################
        ###################################################
        self.ClearPlot_Button = Button(self.PlotControlsFrame, text='Clear', state="normal", width=self.ButtonWidth, font=("Helvetica", 8), command=lambda i=1: self.ClearPlot_ButtonResponse())
        self.ClearPlot_Button.grid(row=1, column=1, padx=1, pady=1, columnspan=1, rowspan=1)
        ###################################################
        ###################################################

        ###################################################
        ###################################################
        self.PrintToGui_Label = Label(self.myFrame, text="PrintToGui_Label", width=100, bg="white")
        if self.EnableInternal_MyPrint_Flag == 1:
            self.PrintToGui_Label.grid(row=3, column=0, padx=0, pady=0, columnspan=1, rowspan=1)
        ###################################################
        ###################################################

        ###################################################
        ###################################################
        self.StartingTime_CalculatedFromGUIthread = self.getPreciseSecondsTimeStampString()

        self.GUI_ready_to_be_updated_flag = 1

        self.root.mainloop()  # THIS MUST BE THE LAST LINE IN THE GUI THREAD SETUP BECAUSE IT'S BLOCKING!!!!
        ###################################################
        ###################################################

        #################################################
        #################################################
        #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def ToggleAutoscale_ButtonResponse(self):

        self.ToggleAutoscale()

        # print("ToggleAutoscale_ButtonResponse event fired!")

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def ToggleAutoscale(self):

        if self.YaxisAutoscaleFlag == 1:
            self.YaxisAutoscaleFlag = 0

        else:
            self.YaxisAutoscaleFlag = 1

        # print("ToggleAutoscale event fired!")

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def ToggleFreezePlot_ButtonResponse(self):

        self.ToggleFreezePlot()

        # print("ToggleFreezePlot_ButtonResponse event fired!")

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def FreezePlot(self):

        self.FreezePlotFlag = 1

        # print("FreezePlot event fired!")

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def UnfreezePlot(self):

        self.FreezePlotFlag = 0

        # print("UnfreezePlot event fired!")

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def ToggleFreezePlot(self):

        if self.FreezePlotFlag == 1:
            self.FreezePlotFlag = 0
        else:
            self.FreezePlotFlag = 1

        # print("ToggleFreezePlot event fired!")

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def SavePlot_ButtonResponse(self):

        self.SavePlotFlag = 1

        # print("SavePlot_ButtonResponse event fired!")

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def Y_min_Entry_Response(self, event):

        try:
            temp = float(self.Y_min_StringVar.get())

            self.Y_min = temp

            print("Y_min_Entry_Response: self.Y_min = " + str(self.Y_min))

        except:
            exceptions = sys.exc_info()[0]
            print("Y_min_Entry_Response, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def Y_max_Entry_Response(self, event):

        try:
            temp = float(self.Y_max_StringVar.get())

            self.Y_max = temp

            print("Y_max_Entry_Response: self.Y_max = " + str(self.Y_max))

        except:
            exceptions = sys.exc_info()[0]
            print("Y_max_Entry_Response, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def ResetMinAndMax_ButtonResponse(self):

        self.ResetMinAndMax()

        # print("ResetMinAndMax_ButtonResponse event fired!")

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def ResetMinAndMax(self):

        self.X_min = self.X_min_StoredFrom__ProcessVariablesThatCanBeLiveUpdated
        self.X_max = self.X_max_StoredFrom__ProcessVariablesThatCanBeLiveUpdated
        self.Y_min = self.Y_min_StoredFrom__ProcessVariablesThatCanBeLiveUpdated
        self.Y_max = self.Y_max_StoredFrom__ProcessVariablesThatCanBeLiveUpdated

        #######################################################
        self.Y_min_StringVar.set(float(self.RemoveLeadingZerosFromString(self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.Y_min, self.GraphNumberOfLeadingZeros, self.GraphNumberOfDecimalPlaces))))
        #######################################################

        #######################################################
        self.Y_max_StringVar.set(float(self.RemoveLeadingZerosFromString(self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.Y_max, self.GraphNumberOfLeadingZeros, self.GraphNumberOfDecimalPlaces))))
        #######################################################

        # print("ResetMinAndMax_ButtonResponse event fired!")

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def ClearPlot_ButtonResponse(self):

        self.ClearPlot()

        # print("ClearPlot_ButtonResponse event fired!")

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def ClearPlot(self):

        self.CanvasForDrawingGraph.delete("all")
        self.CanvasForDrawingGraph.update_idletasks()

        self.CanvasForDrawingGraph.config(width=self.GraphCanvasWidth, height=self.GraphCanvasHeight)

        self.__ProcessVariablesThatCanBeLiveUpdated(self.SetupDict, PrintInfoForDebuggingFlag=0) #Have to repopulate it.

        print("$$$$$$$$$$$ ClearPlot event fired! $$$$$$$$$$$")
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def OnCanvasClickCallbackFunction(self, event):

        print("OnCanvasClickCallbackFunction: Clicked at position [" + str(event.x) + ", " + str(event.y) + "]")

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def ConvertMathPointToCanvasCoordinates(self, PointListXY):

        try:

            x = PointListXY[0]
            y = PointListXY[1]

            W = self.GraphCanvasWidth * 0.8  # #If we use the whole width, then we'll clip labels, tick marks, etc.
            H = self.GraphCanvasHeight * 0.9  # #If we use the whole width, then we'll clip labels, tick marks, etc.

            m_Xaxis = ((W - self.GraphBoxOutline_X0) / (self.X_max - self.X_min))
            b_Xaxis = W - m_Xaxis * self.X_max

            X_out = m_Xaxis * x + b_Xaxis

            m_Yaxis = ((H - self.GraphBoxOutline_Y0) / (self.Y_max - self.Y_min))
            b_Yaxis = H - m_Yaxis * self.Y_max

            Y_out = m_Yaxis * y + b_Yaxis

            X_out = X_out
            Y_out = self.GraphCanvasHeight - Y_out  # Flip y-axis

            return [X_out, Y_out]

        except:
            exceptions = sys.exc_info()[0]
            print("ConvertMathPointToCanvasCoordinates, for input " + str(PointListXY) + " of type " + str(type(PointListXY)) + ", exceptions: %s" % exceptions)
            return PointListXY
            # traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def DrawTextInMathCoordinates(self,
                                  TextToDraw_MathCoord,
                                  CanvasCoordOffset=[0.0, 0.0],
                                  TextString = "",
                                  ColorString = "Black",
                                  FontString = "Helvetica 12 bold",
                                  IDforCreateText = -1,
                                  PrintInfoForDebuggingFlag = 1):

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        try:

            TextToDraw_CanvasCoord = self.ConvertMathPointToCanvasCoordinates([TextToDraw_MathCoord[0], TextToDraw_MathCoord[1]])

            X0 = TextToDraw_CanvasCoord[0] + CanvasCoordOffset[0]
            Y0 = TextToDraw_CanvasCoord[1] + CanvasCoordOffset[1]

            ##########################################################################################################
            if IDforCreateText == -1:

                IDforCreateText_NEW = self.CanvasForDrawingGraph.create_text(X0, Y0, fill = ColorString, text=TextString, font=FontString) #angle=90, #, width=1 WILL FORCE WRAPPING

                if PrintInfoForDebuggingFlag == 1:  print("DrawTextInMathCoordinates: NEVER seen this TEXT object before.")

                return IDforCreateText_NEW
            ##########################################################################################################

            ##########################################################################################################
            else:

                self.CanvasForDrawingGraph.coords(IDforCreateText, X0, Y0)
                self.CanvasForDrawingGraph.itemconfig(IDforCreateText, text=TextString)

                if PrintInfoForDebuggingFlag == 1:  print("DrawTextInMathCoordinates: We've SEEN this TEXT object before. ")

                return -1
            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        except:
            exceptions = sys.exc_info()[0]
            print("DrawTextInMathCoordinates, exceptions: %s" % exceptions)
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
    def DrawLineBetween2pointListsInMathCoordinates(self, PointListXY0_MathCoord, PointListXY1_MathCoord, Color = "Black", LineWidth = 3, IDforCreateLine = -1, PrintInfoForDebuggingFlag = 0):

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            ##########################################################################################################
            if LineWidth > 0:

                PointListXY0_CanvasCoord = self.ConvertMathPointToCanvasCoordinates(PointListXY0_MathCoord)
                PointListXY1_CanvasCoord = self.ConvertMathPointToCanvasCoordinates(PointListXY1_MathCoord)

                X0 = PointListXY0_CanvasCoord[0]
                Y0 = PointListXY0_CanvasCoord[1]

                X1 = PointListXY1_CanvasCoord[0]
                Y1 = PointListXY1_CanvasCoord[1]

                ##########################################################################################################
                if IDforCreateLine == -1:

                    IDforCreateLine_NEW = self.CanvasForDrawingGraph.create_line(X0, Y0, X1, Y1, fill=Color, width=LineWidth)

                    if PrintInfoForDebuggingFlag == 1: print("DrawLineBetween2pointListsInMathCoordinates: NEVER seen this LINE object before.")

                    return IDforCreateLine_NEW
                ##########################################################################################################

                ##########################################################################################################
                else:

                    self.CanvasForDrawingGraph.coords(IDforCreateLine, X0, Y0, X1, Y1)

                    if PrintInfoForDebuggingFlag == 1: print("DrawLineBetween2pointListsInMathCoordinates: We've SEEN this LINE object before.")

                    return -1
                ##########################################################################################################

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
            print("DrawLineBetween2pointListsInMathCoordinates, exceptions: %s" % exceptions)
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
    def DrawOnePoint_MathCoord(self, PointToDraw_MathCoord, Color = "Black", MarkerSize = 1, IDforCreateOval = -1, PrintInfoForDebuggingFlag = 1):

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        try:

            if MarkerSize > 0:

                PointToDraw_CanvasCoord = self.ConvertMathPointToCanvasCoordinates(PointToDraw_MathCoord)

                X0 = PointToDraw_CanvasCoord[0] - MarkerSize
                Y0 = PointToDraw_CanvasCoord[1] - MarkerSize
                X1 = PointToDraw_CanvasCoord[0] + MarkerSize
                Y1 = PointToDraw_CanvasCoord[1] + MarkerSize

                ##########################################################################################################
                if IDforCreateOval == -1:

                    IDforCreateOval_NEW = self.CanvasForDrawingGraph.create_oval(X0, Y0, X1, Y1, fill=Color, outline=Color)

                    if PrintInfoForDebuggingFlag == 1:  print("DrawOnePoint_MathCoord: NEVER seen this POINT/OVAL object before.")

                    return IDforCreateOval_NEW
                ##########################################################################################################

                ##########################################################################################################
                else:

                    self.CanvasForDrawingGraph.coords(IDforCreateOval, X0, Y0, X1, Y1)

                    if PrintInfoForDebuggingFlag == 1:  print("DrawOnePoint_MathCoord: We've seen this POINT/OVAL object before.")

                    return -1
                ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        except:
            exceptions = sys.exc_info()[0]
            print("DrawOnePoint_MathCoord, exceptions: %s" % exceptions)
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
    def DrawAllPoints_MathCoord(self, temp_CurvesToPlotDictOfDicts, DrawLinesBetweenPointsFlag = 1):

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            for CurveName in temp_CurvesToPlotDictOfDicts:

                TempListOfPointToDraw = temp_CurvesToPlotDictOfDicts[CurveName]["PointToDrawList"]
                TempColor = temp_CurvesToPlotDictOfDicts[CurveName]["Color"]
                TempMarkerSize = temp_CurvesToPlotDictOfDicts[CurveName]["MarkerSize"]
                TempLineWidth = temp_CurvesToPlotDictOfDicts[CurveName]["LineWidth"]
                TempPointToDrawList_IDforCreateOval = temp_CurvesToPlotDictOfDicts[CurveName]["PointToDrawList_IDforCreateOval"]
                TempPointToDrawList_IDforCreateLine = temp_CurvesToPlotDictOfDicts[CurveName]["PointToDrawList_IDforCreateLine"]

                ##########################################################################################################
                ##########################################################################################################
                if len(TempListOfPointToDraw) > 0:

                    PointToDraw_MathCoord_LAST = []

                    ##########################################################################################################
                    for Index, PointToDraw_MathCoord in enumerate(TempListOfPointToDraw):

                        ################################################# DRAW POINT
                        ReturnedIDforCreateOval = self.DrawOnePoint_MathCoord(PointToDraw_MathCoord = PointToDraw_MathCoord,
                                                                                Color = TempColor,
                                                                                MarkerSize = TempMarkerSize,
                                                                                IDforCreateOval = temp_CurvesToPlotDictOfDicts[CurveName]["PointToDrawList_IDforCreateOval"][Index],
                                                                                PrintInfoForDebuggingFlag = 0)

                        if ReturnedIDforCreateOval != -1:
                            temp_CurvesToPlotDictOfDicts[CurveName]["PointToDrawList_IDforCreateOval"][Index] = ReturnedIDforCreateOval
                        #################################################

                        ################################################# DRAW LINE
                        if DrawLinesBetweenPointsFlag == 1:

                            if Index >= 1 and TempLineWidth > 0:

                                ReturnedIDforCreateLine = self.DrawLineBetween2pointListsInMathCoordinates(PointListXY0_MathCoord = PointToDraw_MathCoord,
                                                                                                         PointListXY1_MathCoord = PointToDraw_MathCoord_LAST,
                                                                                                         Color = TempColor,
                                                                                                         LineWidth=TempLineWidth,
                                                                                                         IDforCreateLine = temp_CurvesToPlotDictOfDicts[CurveName]["PointToDrawList_IDforCreateLine"][Index],
                                                                                                         PrintInfoForDebuggingFlag=0)

                                if ReturnedIDforCreateLine != -1:
                                    temp_CurvesToPlotDictOfDicts[CurveName]["PointToDrawList_IDforCreateLine"][Index] = ReturnedIDforCreateLine
                        #################################################

                        ################################################# UPDATE RECORD
                        PointToDraw_MathCoord_LAST = PointToDraw_MathCoord
                        #################################################

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
        except:
            exceptions = sys.exc_info()[0]
            print("DrawAllPoints_MathCoord, exceptions: %s" % exceptions)
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
    def DrawAxes(self, temp_CurvesToPlotDictOfDicts, temp_X_min, temp_X_max, temp_Y_min, temp_Y_max):

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        try:

            #print("self.AxesAllLines_IDforCreateLine: len = " + str(len(self.AxesAllLines_IDforCreateLine)) +", data = " + str(self.AxesAllLines_IDforCreateLine))

            ########################################################################################################## Compute where to place the X axis
            ##########################################################################################################
            if self.XaxisDrawnAtBottomOfGraph == 1:
                XaxisVerticalCoord_MathCoord = temp_Y_min  #Draw x-axis at the bottom of the graph

            else:
                XaxisVerticalCoord_MathCoord = 0.0  #Draw x-axis at the zero-crossing of the y-axis
            ##########################################################################################################
            ##########################################################################################################

            ########################################################################################################## Compute axis tick-mark locations
            ##########################################################################################################
            XaxisTickMarksList = self.RangeOfFloatNumberOfIncrements_PurePythonNoNumpy(temp_X_min, temp_X_max, self.XaxisNumberOfTickMarks)
            YaxisTickMarksList = self.RangeOfFloatNumberOfIncrements_PurePythonNoNumpy(temp_Y_min, temp_Y_max, self.YaxisNumberOfTickMarks)

            #print("XaxisTickMarksList: " + str(XaxisTickMarksList))
            ##########################################################################################################
            ##########################################################################################################

            ########################################################################################################## Compute info for tick-mark line and label placement
            ########################################################################################################## Must compute tick-mark length of X and Y axes separately as they scale differently
            XaxisTickMarkLength_MathCoord = 0.01 * abs(temp_Y_max - temp_Y_min)
            YaxisTickMarkLength_MathCoord = 0.01 * abs(temp_X_max - temp_X_min)

            YaxisTickMarkLabelXcoord_MathCoord = temp_X_min - 0.03 * abs(temp_X_max - temp_X_min)
            XaxisTickMarkLabelYcoord_MathCoord = XaxisVerticalCoord_MathCoord - 0.03 * abs(temp_Y_max - temp_Y_min)
            ##########################################################################################################
            ##########################################################################################################

            ########################################################################################################## Draw the X axis (a single line)
            ##########################################################################################################
            ReturnedIDforCreateLine = self.DrawLineBetween2pointListsInMathCoordinates(PointListXY0_MathCoord=[temp_X_min, XaxisVerticalCoord_MathCoord],
                                                                                       PointListXY1_MathCoord=[temp_X_max, XaxisVerticalCoord_MathCoord],
                                                                                       Color="Black",
                                                                                       LineWidth=1,
                                                                                       IDforCreateLine=self.AxesAllLines_IDforCreateLine[0],
                                                                                       PrintInfoForDebuggingFlag=0)  # Draw X-axis but NOT the tick marks

            if ReturnedIDforCreateLine != -1:
                self.AxesAllLines_IDforCreateLine[0] = ReturnedIDforCreateLine
            ##########################################################################################################
            ##########################################################################################################

            ########################################################################################################## Draw the Y axis (a single line)
            ##########################################################################################################
            ReturnedIDforCreateLine = self.DrawLineBetween2pointListsInMathCoordinates(PointListXY0_MathCoord=[temp_X_min, temp_Y_min],
                                                                                       PointListXY1_MathCoord=[temp_X_min, temp_Y_max],
                                                                                       Color="Black",
                                                                                       LineWidth=1,
                                                                                       IDforCreateLine=self.AxesAllLines_IDforCreateLine[1],
                                                                                       PrintInfoForDebuggingFlag=0)  #Draw Y-axis at the left of the graph but NOT the tick marks

            if ReturnedIDforCreateLine != -1:
                self.AxesAllLines_IDforCreateLine[1] = ReturnedIDforCreateLine
            ##########################################################################################################
            ##########################################################################################################

            ########################################################################################################## Draw X axis text label
            ##########################################################################################################
            XaxisLabelStartX_MathCoord = temp_X_min + 1.1 * abs(temp_X_max - temp_X_min)
            XaxisLabelStartY_MathCoord = temp_Y_min

            ReturnedIDforCreateText = self.DrawTextInMathCoordinates(TextToDraw_MathCoord = [XaxisLabelStartX_MathCoord, XaxisLabelStartY_MathCoord],
                                                                      CanvasCoordOffset = [0.0, 0.0],
                                                                      TextString = self.XaxisLabelString,
                                                                      ColorString = "Black",
                                                                      FontString = "Helvetica "+ str(self.LargeTextSize) + " bold",
                                                                      IDforCreateText = self.AxesAllText_IDforCreateText[0],
                                                                      PrintInfoForDebuggingFlag = 0)

            if ReturnedIDforCreateText != -1:
                self.AxesAllText_IDforCreateText[0] = ReturnedIDforCreateText
            ##########################################################################################################
            ##########################################################################################################

            ########################################################################################################## Draw Y axis text label
            ##########################################################################################################
            YaxisLabelStartX_MathCoord = temp_X_min + 0.05 * abs(temp_X_max - temp_X_min)
            YaxisLabelStartY_MathCoord = temp_Y_min + 1.05 * abs(temp_Y_max - temp_Y_min)

            ReturnedIDforCreateText = self.DrawTextInMathCoordinates(TextToDraw_MathCoord = [YaxisLabelStartX_MathCoord, YaxisLabelStartY_MathCoord],
                                                                      CanvasCoordOffset=[0.0, 0.0],
                                                                      TextString = self.YaxisLabelString,
                                                                      ColorString = "Black",
                                                                      FontString = "Helvetica "+ str(self.LargeTextSize) + " bold",
                                                                      IDforCreateText = self.AxesAllText_IDforCreateText[1],
                                                                      PrintInfoForDebuggingFlag = 0)

            if ReturnedIDforCreateText != -1:
                self.AxesAllText_IDforCreateText[1] = ReturnedIDforCreateText
            ##########################################################################################################
            ##########################################################################################################

            ########################################################################################################## Draw X-axis tick marks AND labels
            ##########################################################################################################
            for Index, x in enumerate(XaxisTickMarksList):

                ##########################################################################################################
                ReturnedIDforCreateLine = self.DrawLineBetween2pointListsInMathCoordinates(PointListXY0_MathCoord=[x, XaxisVerticalCoord_MathCoord - XaxisTickMarkLength_MathCoord],
                                                                                           PointListXY1_MathCoord=[x, XaxisVerticalCoord_MathCoord + XaxisTickMarkLength_MathCoord],
                                                                                           Color="Black",
                                                                                           LineWidth=1,
                                                                                           IDforCreateLine=self.AxesAllLines_IDforCreateLine[2 + Index],
                                                                                           PrintInfoForDebuggingFlag=0)  # For drawing the x-axis at the bottom of the graph

                if ReturnedIDforCreateLine != -1:
                    self.AxesAllLines_IDforCreateLine[2 + Index] = ReturnedIDforCreateLine
                ##########################################################################################################

                ##########################################################################################################
                ReturnedIDforCreateText = self.DrawTextInMathCoordinates(TextToDraw_MathCoord = [x, XaxisTickMarkLabelYcoord_MathCoord],
                                                                          CanvasCoordOffset=[0.0, 0.0],
                                                                          TextString = round(Decimal(x), self.XaxisNumberOfDecimalPlacesForLabels),
                                                                          ColorString = "Black",
                                                                          FontString = "Helvetica "+ str(self.SmallTextSize), #font="Times 20 italic bold", angle=90, #, width=1 WILL FORCE WRAPPING
                                                                          IDforCreateText = self.AxesAllText_IDforCreateText[2 + Index],
                                                                          PrintInfoForDebuggingFlag = 0)

                if ReturnedIDforCreateText != -1:
                    self.AxesAllText_IDforCreateText[2 + Index] = ReturnedIDforCreateText
                ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################

            ########################################################################################################## Draw Y-axis tick marks AND labels
            ##########################################################################################################
            for Index, y in enumerate(YaxisTickMarksList):

                ##########################################################################################################
                ReturnedIDforCreateLine = self.DrawLineBetween2pointListsInMathCoordinates(PointListXY0_MathCoord=[temp_X_min - YaxisTickMarkLength_MathCoord, y],
                                                                                           PointListXY1_MathCoord=[temp_X_min + YaxisTickMarkLength_MathCoord, y],
                                                                                           Color="Black",
                                                                                           LineWidth=1,
                                                                                           IDforCreateLine = self.AxesAllLines_IDforCreateLine[2 + self.XaxisNumberOfTickMarks + Index],
                                                                                           PrintInfoForDebuggingFlag=0)

                if ReturnedIDforCreateLine != -1:
                    self.AxesAllLines_IDforCreateLine[2 + self.XaxisNumberOfTickMarks + Index] = ReturnedIDforCreateLine
                ##########################################################################################################

                ##########################################################################################################
                ReturnedIDforCreateText = self.DrawTextInMathCoordinates(TextToDraw_MathCoord = [YaxisTickMarkLabelXcoord_MathCoord, y],
                                                                          CanvasCoordOffset=[0.0, 0.0],
                                                                          TextString = round(Decimal(y), self.YaxisNumberOfDecimalPlacesForLabels),
                                                                          ColorString = "Black",
                                                                          FontString = "Helvetica "+ str(self.SmallTextSize),
                                                                          IDforCreateText = self.AxesAllText_IDforCreateText[2 + self.XaxisNumberOfTickMarks + Index],
                                                                          PrintInfoForDebuggingFlag = 0)

                if ReturnedIDforCreateText != -1:
                    self.AxesAllText_IDforCreateText[2 + self.XaxisNumberOfTickMarks + Index] = ReturnedIDforCreateText
                ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################

            ########################################################################################################## Draw legend
            ##########################################################################################################
            if self.ShowLegendFlag == 1:
                CurveNameLabelsStartX_MathCoord = temp_X_min + 1.1 * abs(temp_X_max - temp_X_min)
                CurveNameLabelsStartY_MathCoord = temp_Y_min + 0.5 * abs(temp_Y_max - temp_Y_min)

                for Index, CurveName in enumerate(temp_CurvesToPlotDictOfDicts):

                    ReturnedIDforCreateText = self.DrawTextInMathCoordinates(TextToDraw_MathCoord = [CurveNameLabelsStartX_MathCoord, CurveNameLabelsStartY_MathCoord],
                                                                          CanvasCoordOffset=[0.0, 20*Index], #Shift each cruve name downward from the last
                                                                          TextString = temp_CurvesToPlotDictOfDicts[CurveName]["CurveName"],
                                                                          ColorString = temp_CurvesToPlotDictOfDicts[CurveName]["Color"],
                                                                          FontString = "Helvetica " + str(self.LargeTextSize) + " bold",
                                                                          IDforCreateText = self.AxesAllText_IDforCreateText[2 + self.XaxisNumberOfTickMarks + self.YaxisNumberOfTickMarks + Index],
                                                                          PrintInfoForDebuggingFlag = 0)

                    if ReturnedIDforCreateText != -1:
                        self.AxesAllText_IDforCreateText[2 + self.XaxisNumberOfTickMarks + self.YaxisNumberOfTickMarks + Index] = ReturnedIDforCreateText
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
            print("MyPlotterPureTkinterStandAloneProcess, DrawAxes: exceptions: %s" % exceptions)
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
    def UpdateNewXandYlimits(self, temp_CurvesToPlotDictOfDicts, temp_X_min, temp_X_max, temp_Y_min, temp_Y_max):

        X_min_NEW = temp_X_min
        X_max_NEW = temp_X_max
        Y_min_NEW = temp_Y_min
        Y_max_NEW = temp_Y_max

        try:
            temp_AllPointsXlist = list()
            temp_AllPointsYlist = list()
            for CurveName in temp_CurvesToPlotDictOfDicts:
                TempListOfPointToDrawForThisCurve = temp_CurvesToPlotDictOfDicts[CurveName]["PointToDrawList"]

                for temp_Point in TempListOfPointToDrawForThisCurve:

                    if temp_CurvesToPlotDictOfDicts[CurveName]["IncludeInXaxisAutoscaleCalculation"] == 1:
                        temp_AllPointsXlist.append(temp_Point[0])

                    if temp_CurvesToPlotDictOfDicts[CurveName]["IncludeInYaxisAutoscaleCalculation"] == 1:
                        temp_AllPointsYlist.append(temp_Point[1])

            if len(temp_AllPointsXlist) > 0:
                # print temp_AllPointsXlist

                X_min_temp = min(temp_AllPointsXlist)
                X_max_temp = max(temp_AllPointsXlist)
                Y_min_temp = min(temp_AllPointsYlist)
                Y_max_temp = max(temp_AllPointsYlist)

                if X_min_temp != X_max_temp and self.XaxisAutoscaleFlag == 1:
                    X_min_NEW = X_min_temp
                    X_max_NEW = X_max_temp

                if Y_min_temp != Y_max_temp and self.YaxisAutoscaleFlag == 1:
                    Y_min_NEW = Y_min_temp
                    Y_max_NEW = Y_max_temp

            # print("X_min_NEW: " + str(X_min_NEW) + ", X_max_NEW: " + str(X_max_NEW) + ", Len: " + str(len(TempListOfPointToDraw)))
            # print("Y_min_NEW: " + str(Y_min_NEW) + ", Y_max_NEW: " + str(Y_max_NEW) + ", Len: " + str(len(TempListOfPointToDraw)))

        except:
            exceptions = sys.exc_info()[0]
            print("UpdateNewXandYlimits, exceptions: %s" % exceptions)
            # traceback.print_exc()

        if abs(X_max_NEW - X_min_NEW) < self.AxisMinMaxEpsilon:
            X_max_NEW = X_min_NEW + self.AxisMinMaxEpsilon

        if abs(Y_max_NEW - Y_min_NEW) < self.AxisMinMaxEpsilon:
            Y_max_NEW = Y_min_NEW + self.AxisMinMaxEpsilon

        return [X_min_NEW, X_max_NEW, Y_min_NEW, Y_max_NEW]
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def CreateNewDirectoryIfItDoesntExist(self, directory):
        try:
            # print("CreateNewDirectoryIfItDoesntExist, directory: " + directory)
            if os.path.isdir(directory) == 0:  # No directory with this name exists
                os.makedirs(directory)

            return 1
        except:
            exceptions = sys.exc_info()[0]
            print("CreateNewDirectoryIfItDoesntExist, Exceptions: %s" % exceptions)
            return 0
            # traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## Def GUI
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def __GUI_update_clock(self):  # THIS FUNCTION NEEDS TO BE CALLED INTERNALLY BY THE CLASS, NOT EXTERNALLY LIKE WE NORMALLY DO BECAUSE WE'RE FIRING THESE ROOT.AFTER CALLBACKS FASTER THAN THE PARENT ROOT GUI

        if self.EXIT_PROGRAM_FLAG == 0:

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            if self.GUI_ready_to_be_updated_flag == 1:

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                self.CurrentTime_CalculatedFromGUIthread = self.getPreciseSecondsTimeStampString() - self.StartingTime_CalculatedFromGUIthread
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                if self.FreezePlotFlag == 1:
                    if self.ToggleFreezePlot_Button["text"] != "Unfreeze":
                        self.ToggleFreezePlot_Button["text"] = "Unfreeze"
                else:
                    if self.ToggleFreezePlot_Button["text"] != "Freeze":
                        self.ToggleFreezePlot_Button["text"] = "Freeze"
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                if self.RootGeometryHasBeenModifiedFlag == 1:

                    self.RootConfigurationUpdate()

                    if self.RootGeometryHasBeenModified_HasThisEventFiredBeforeFlag == 1:
                        self.ClearPlot()
                        self.FreezePlotFlag = 0 #Make sure that the plot isn't frozen so that we can redraw it.

                    self.RootGeometryHasBeenModified_HasThisEventFiredBeforeFlag = 1
                    self.RootGeometryHasBeenModifiedFlag = 0
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                if self.FreezePlotFlag == 0:

                    ##########################################################################################################
                    ##########################################################################################################
                    temp_CurvesToPlotDictOfDicts = dict(self.CurvesToPlotDictOfDicts)  # Make local copy so that adding new points from external program won't change anything mid-plotting.

                    temp_X_min = float(self.X_min)
                    temp_X_max = float(self.X_max)
                    temp_Y_min = float(self.Y_min)
                    temp_Y_max = float(self.Y_max)

                    [self.X_min, self.X_max, self.Y_min, self.Y_max] = self.UpdateNewXandYlimits(temp_CurvesToPlotDictOfDicts, temp_X_min, temp_X_max, temp_Y_min, temp_Y_max)

                    temp_X_min = float(self.X_min)
                    temp_X_max = float(self.X_max)
                    temp_Y_min = float(self.Y_min)
                    temp_Y_max = float(self.Y_max)
                    ##########################################################################################################
                    ##########################################################################################################

                    ########################################################################################################## unicorn
                    ##########################################################################################################
                    self.DrawAxes(temp_CurvesToPlotDictOfDicts, temp_X_min, temp_X_max, temp_Y_min, temp_Y_max)
                    self.DrawAllPoints_MathCoord(temp_CurvesToPlotDictOfDicts, DrawLinesBetweenPointsFlag=1)
                    ##########################################################################################################
                    ##########################################################################################################

                    ########################################################################################################## TEST AREA FOR PLOTTING KNOWN POINTS
                    ##########################################################################################################
                    '''
                    self.DrawOnePoint_MathCoord(PointToDraw_MathCoord = [self.X_min, self.Y_min], Color = "Green", IDforCreateOval = -1, PrintInfoForDebuggingFlag = 0)
                    self.DrawOnePoint_MathCoord(PointToDraw_MathCoord = [self.X_min, self.Y_max], Color = "Green", IDforCreateOval = -1, PrintInfoForDebuggingFlag = 0)
                    self.DrawOnePoint_MathCoord(PointToDraw_MathCoord = [self.X_max, self.Y_min], Color = "Green", IDforCreateOval = -1, PrintInfoForDebuggingFlag = 0)
                    self.DrawOnePoint_MathCoord(PointToDraw_MathCoord = [self.X_max, self.Y_max], Color = "Green", IDforCreateOval = -1, PrintInfoForDebuggingFlag = 0)
                    '''
                    ##########################################################################################################
                    ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                self.Debug_Label["text"] = "P.PID = " + str(self.ParentPID) + \
                                            ", SelfPID = " + str(self.SelfPID) + \
                                            ", Time: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.CurrentTime_CalculatedFromGUIthread, 0, 1) + \
                                            ", Freq: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.LoopFrequency_CalculatedFromGUIthread, 2, 3) + \
                                            ", CPU %: " + str(self.MemoryUsageOfProcessByPID_Dict["CPUusage_Percent"]) + \
                                            ", MEM %: " + str(self.MemoryUsageOfProcessByPID_Dict["MemoryUsage_Percent"]) + \
                                            ", #: " + str(len(self.CanvasForDrawingGraph.find_all())) + \
                                            ", Watchdog: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.TimeIntoWatchdogTimer, 0, 3)

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                self.ToggleAutoscale_Button["text"] = "Autoscale: " + str(self.YaxisAutoscaleFlag)
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                if self.YaxisAutoscaleFlag == 1:

                    #######################################################
                    if self.Y_min_Entry["state"] != "disabled":
                        self.Y_min_Entry["state"] = "disabled"
                    #######################################################

                    #######################################################
                    if self.Y_max_Entry["state"] != "disabled":
                        self.Y_max_Entry["state"] = "disabled"
                    #######################################################

                    #######################################################
                    if self.ResetMinAndMax_Button["state"] != "disabled":
                        self.ResetMinAndMax_Button["state"] = "disabled"
                    #######################################################

                    #######################################################
                    self.Y_min_StringVar.set(float(self.RemoveLeadingZerosFromString(self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.Y_min,
                                                                                                                                         self.GraphNumberOfLeadingZeros,
                                                                                                                                         self.GraphNumberOfDecimalPlaces))))
                    #######################################################

                    #######################################################
                    self.Y_max_StringVar.set(float(self.RemoveLeadingZerosFromString(self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.Y_max,
                                                                                                                                         self.GraphNumberOfLeadingZeros,
                                                                                                                                         self.GraphNumberOfDecimalPlaces))))
                    #######################################################

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                else:
                    #######################################################
                    if self.Y_min_Entry["state"] != "normal":
                        self.Y_min_Entry["state"] = "normal"
                    #######################################################

                    #######################################################
                    if self.Y_max_Entry["state"] != "normal":
                        self.Y_max_Entry["state"] = "normal"
                    #######################################################

                    #######################################################
                    if self.ResetMinAndMax_Button["state"] != "normal":
                        self.ResetMinAndMax_Button["state"] = "normal"
                    #######################################################

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                self.PrintToGui_Label.config(text=self.PrintToGui_Label_TextInput_Str)
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                self.UpdateFrequencyCalculation_CalculatedFromGUIthread()
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                if self.SavePlotFlag == 1:

                    if self.pyautogui_ModuleImportedFlag == 1:

                        try:

                            self.CreateNewDirectoryIfItDoesntExist(self.SavePlot_DirectoryPath)

                            self.ImageFilenameFullDirectoryPathWithExtension = self.SavePlot_DirectoryPath + "//MyPlot_" + str(self.getTimeStampString()) + ".png"
                            print("Saving screenshot: " + self.ImageFilenameFullDirectoryPathWithExtension)

                            # self.CanvasForDrawingGraph.postscript(file="canvas_output.ps")

                            x = self.CanvasForDrawingGraph.winfo_rootx()
                            y = self.CanvasForDrawingGraph.winfo_rooty()
                            w = self.CanvasForDrawingGraph.winfo_width()
                            h = self.CanvasForDrawingGraph.winfo_height()

                            screenshot = pyautogui.screenshot(region=(x, y, w, h))
                            screenshot.save(self.ImageFilenameFullDirectoryPathWithExtension)

                        except:
                            exceptions = sys.exc_info()[0]
                            print("MyPlotterPureTkinterStandAloneProcess, SavePlotFlag, exceptions: %s" % exceptions)
                            traceback.print_exc()

                    self.SavePlotFlag = 0
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                self.root.after(self.GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents, self.__GUI_update_clock)
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

            # input_string = input_string.replace("\n", "").replace("\r", "")

            ################################ Write to console
            # Some people said that print crashed for pyinstaller-built-applications and that sys.stdout.write fixed this.
            # http://stackoverflow.com/questions/13429924/pyinstaller-packaged-application-works-fine-in-console-mode-crashes-in-window-m
            if self.PrintToConsoleFlag == 1:
                sys.stdout.write(input_string + "\n")
            ################################

            ################################ Write to GUI
            self.PrintToGui_Label_TextInputHistory_List.append(self.PrintToGui_Label_TextInputHistory_List.pop(0))  # Shift the list
            self.PrintToGui_Label_TextInputHistory_List[-1] = str(input_string)  # Add the latest value

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
    ##########################################################################################################
    ##########################################################################################################
    def IsInputList(self, InputToCheck):

        result = isinstance(InputToCheck, list)
        return result

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def IsInputDict(self, InputToCheck):

        result = isinstance(InputToCheck, dict)
        return result

    ##########################################################################################################
    ##########################################################################################################
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
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
