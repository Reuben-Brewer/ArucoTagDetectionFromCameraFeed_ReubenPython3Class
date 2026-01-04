# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision AA, 12/22/2025

Verified working on: Python 3.11/12/13 for Windows 10/11 64-bit, Ubuntu 20.04, and Raspberry Pi Bookworm.
'''

__author__ = 'reuben.brewer'

##########################################################################################################
##########################################################################################################

#########################################################
import ReubenGithubCodeModulePaths #Replaces the need to have "ReubenGithubCodeModulePaths.pth" within "C:\Anaconda3\Lib\site-packages", which slows down the start of a Python interpreter if your code directories are in Google Drive.
ReubenGithubCodeModulePaths.Enable()
#########################################################

#########################################################
from MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class import *
#########################################################

#########################################################
import os
import sys
import platform
import time
import datetime
import threading
import collections
import math
import traceback
import re
import keyboard
import random
from random import randint
import signal #for CTRLc_HandlerFunction
#########################################################

#########################################################
from tkinter import *
import tkinter.font as tkFont
from tkinter import ttk
#########################################################

#########################################################
import platform
if platform.system() == "Windows":
    import ctypes
    winmm = ctypes.WinDLL('winmm')
    winmm.timeBeginPeriod(1) #Set minimum timer resolution to 1ms so that time.sleep(0.001) behaves properly.
#########################################################

##########################################################################################################
##########################################################################################################

########################################################################################################## MUST ISSUE CTRLc_RegisterHandlerFunction() AT START OF PROGRAM
##########################################################################################################
def CTRLc_RegisterHandlerFunction():

    CurrentHandlerRegisteredForSIGINT = signal.getsignal(signal.SIGINT)
    #print("CurrentHandlerRegisteredForSIGINT: " + str(CurrentHandlerRegisteredForSIGINT))

    defaultish = (signal.SIG_DFL, signal.SIG_IGN, None, getattr(signal, "default_int_handler", None)) #Treat Python's built-in default handler as "unregistered"

    if CurrentHandlerRegisteredForSIGINT in defaultish: # Only install if it's default/ignored (i.e., nobody set it yet)
        signal.signal(signal.SIGINT, CTRLc_HandlerFunction)
        print("test_program_for_MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class.py, CTRLc_RegisterHandlerFunction event fired!")

    else:
        print("test_program_for_MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class.py, could not register CTRLc_RegisterHandlerFunction (already registered previously)")
##########################################################################################################
##########################################################################################################

########################################################################################################## MUST ISSUE CTRLc_RegisterHandlerFunction() AT START OF PROGRAM
##########################################################################################################
def CTRLc_HandlerFunction(signum, frame):

    print("CTRLc_HandlerFunction event firing!")

    ExitProgram_Callback()

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
def GetLatestWaveformValue(CurrentTime, MinValue, MaxValue, Period, WaveformTypeString="Sine"):
    
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            ##########################################################################################################
            OutputValue = 0.0
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            WaveformTypeString_ListOfAcceptableValues = ["Sine", "Cosine", "Triangular", "Square"]
        
            if WaveformTypeString not in WaveformTypeString_ListOfAcceptableValues:
                print("GetLatestWaveformValue: Error, WaveformTypeString must be in " + str(WaveformTypeString_ListOfAcceptableValues))
                return -11111.0
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            if WaveformTypeString == "Sine":
    
                TimeGain = math.pi/Period
                OutputValue = (MaxValue + MinValue)/2.0 + 0.5*abs(MaxValue - MinValue)*math.sin(TimeGain*CurrentTime)
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            elif WaveformTypeString == "Cosine":
    
                TimeGain = math.pi/Period
                OutputValue = (MaxValue + MinValue)/2.0 + 0.5*abs(MaxValue - MinValue)*math.cos(TimeGain*CurrentTime)
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            elif WaveformTypeString == "Triangular":
                TriangularInput_TimeGain = 1.0
                TriangularInput_MinValue = -5
                TriangularInput_MaxValue = 5.0
                TriangularInput_PeriodInSeconds = 2.0
        
                #TriangularInput_Height0toPeak = abs(TriangularInput_MaxValue - TriangularInput_MinValue)
                #TriangularInput_CalculatedValue_1 = abs((TriangularInput_TimeGain*CurrentTime_CalculatedFromMainThread % PeriodicInput_PeriodInSeconds) - TriangularInput_Height0toPeak) + TriangularInput_MinValue
        
                A = abs(MaxValue - MinValue)
                P = Period
    
                #https://stackoverflow.com/questions/1073606/is-there-a-one-line-function-that-generates-a-triangle-wave
                OutputValue = (A / (P / 2)) * ((P / 2) - abs(CurrentTime % (2 * (P / 2)) - P / 2)) + MinValue
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            elif WaveformTypeString == "Square":
    
                TimeGain = math.pi/Period
                MeanValue = (MaxValue + MinValue)/2.0
                SinusoidalValue =  MeanValue + 0.5*abs(MaxValue - MinValue)*math.sin(TimeGain*CurrentTime)
                
                if SinusoidalValue >= MeanValue:
                    OutputValue = MaxValue
                else:
                    OutputValue = MinValue
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            else:
                OutputValue = 0.0
            ##########################################################################################################
            ##########################################################################################################
            
            return OutputValue

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        except:
            exceptions = sys.exc_info()[0]
            print("GetLatestWaveformValue: Exceptions: %s" % exceptions)
            return -11111.0
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
def getPreciseSecondsTimeStampString():
    ts = time.time()

    return ts
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def ToggleAutoscale_ButtonResponse():
    global ToggleAutoscale_EventNeedsToBeFiredFlag
    
    ToggleAutoscale_EventNeedsToBeFiredFlag = 1

    #print("ToggleAutoscale_ButtonResponse event fired!")

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def ToggleFreezePlot_ButtonResponse():
    global ToggleFreezePlot_EventNeedsToBeFiredFlag
    
    ToggleFreezePlot_EventNeedsToBeFiredFlag = 1

    #print("ToggleFreezePlot_ButtonResponse event fired!")

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def SavePlot_ButtonResponse():
    global SavePlot_EventNeedsToBeFiredFlag
    
    SavePlot_EventNeedsToBeFiredFlag = 1

    #print("SavePlot_ButtonResponse event fired!")

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def ResetMinAndMax_ButtonResponse():
    global ResetMinAndMax_EventNeedsToBeFiredFlag
    
    ResetMinAndMax_EventNeedsToBeFiredFlag = 1

    #print("ResetMinAndMax_ButtonResponse event fired!")

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def ClearPlot_ButtonResponse():
    global ClearPlot_EventNeedsToBeFiredFlag

    ClearPlot_EventNeedsToBeFiredFlag = 1

    #print("ClearPlot_ButtonResponse event fired!")

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def ExternalUpdateSetupDict_ButtonResponse():
    global ExternalUpdateSetupDict_EventNeedsToBeFiredFlag

    ExternalUpdateSetupDict_EventNeedsToBeFiredFlag = 1

    # print("ExternalUpdateSetupDict_ButtonResponse event fired!")

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def GUI_update_clock():
    global root
    global EXIT_PROGRAM_FLAG
    global GUI_RootAfterCallbackInterval_Milliseconds
    global USE_GUI_FLAG

    global MyPlotterPureTkinterStandAloneProcess_Object
    global USE_MyPlotterPureTkinterStandAloneProcess_FLAG
    global MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG
    global SHOW_IN_GUI_MyPlotterPureTkinterStandAloneProcess_FLAG

    global PARENT_GUI_COUNTER

    if USE_GUI_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
        #########################################################
        #########################################################

            PARENT_GUI_COUNTER = PARENT_GUI_COUNTER + 1
            #print("PID = " + str(os.getpid()) + ", PARENT_GUI_COUNTER: " + str(PARENT_GUI_COUNTER))

            #########################################################
            #if USE_MyPlotterPureTkinterStandAloneProcess_FLAG == 1 and MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG == 1 and SHOW_IN_GUI_MyPlotterPureTkinterStandAloneProcess_FLAG == 1:
                #pass #DO NOT CALL MyPlotterPureTkinterStandAloneProcess_Object.GUI_update_clock() as the plotter is firing its own, internal root.after callbacks faster than in this parent root GUI loop.
            #########################################################

            root.after(GUI_RootAfterCallbackInterval_Milliseconds, GUI_update_clock)
            #########################################################

        #########################################################
        #########################################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def ExitProgram_Callback(OptionalArugment = 0):
    global EXIT_PROGRAM_FLAG

    print("Exiting all threads in test_program_for_MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class.")

    EXIT_PROGRAM_FLAG = 1
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def on_window_state_change(event):
    if root.state() == 'iconic':  # Means minimized
        root.after(10, root.deiconify)  # Bring it back up immediately
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
    global GUI_RootAfterCallbackInterval_Milliseconds

    ################################################# KEY GUI LINE
    #################################################
    root = Tk()

    root.protocol("WM_DELETE_WINDOW", ExitProgram_Callback)  # Set the callback function for when the window's closed.
    root.geometry('%dx%d+%d+%d' % (root_width, root_height, root_Xpos,root_Ypos))  # set the dimensions of the screen and where it is placed
    root.bind("<Unmap>", on_window_state_change)  # Fired when minimized or hidden
    #################################################
    #################################################

    #################################################
    #################################################
    AllButtonsGuiFrame = Frame(root)
    AllButtonsGuiFrame.grid(row=0, column=0, padx=1, pady=1, rowspan=1, columnspan=1, sticky='w')
    #################################################
    #################################################

    #################################################
    #################################################
    ToggleAutoscale_Button = Button(AllButtonsGuiFrame, text='Toggle Autoscale', state="normal", width=20, font=("Helvetica", 8), command=lambda i=1: ToggleAutoscale_ButtonResponse())
    ToggleAutoscale_Button.grid(row=0, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
    #################################################
    #################################################
    
    #################################################
    #################################################
    ToggleFreezePlot_Button = Button(AllButtonsGuiFrame, text='Freeze Plot', state="normal", width=20, font=("Helvetica", 8), command=lambda i=1: ToggleFreezePlot_ButtonResponse())
    ToggleFreezePlot_Button.grid(row=0, column=1, padx=1, pady=1, columnspan=1, rowspan=1)
    #################################################
    #################################################
    
    #################################################
    #################################################
    SavePlot_Button = Button(AllButtonsGuiFrame, text='Save Plot', state="normal", width=20, font=("Helvetica", 8), command=lambda i=1: SavePlot_ButtonResponse())
    SavePlot_Button.grid(row=0, column=2, padx=1, pady=1, columnspan=1, rowspan=1)
    #################################################
    #################################################

    #################################################
    #################################################
    ResetMinAndMax_Button = Button(AllButtonsGuiFrame, text='ResetMinAndMax', state="normal", width=20, font=("Helvetica", 8), command=lambda i=1: ResetMinAndMax_ButtonResponse())
    ResetMinAndMax_Button.grid(row=0, column=3, padx=1, pady=1, columnspan=1, rowspan=1)
    #################################################
    #################################################
    
    #################################################
    #################################################
    ClearPlot_Button = Button(AllButtonsGuiFrame, text='ClearPlot', state="normal", width=20, font=("Helvetica", 8), command=lambda i=1: ClearPlot_ButtonResponse())
    ClearPlot_Button.grid(row=0, column=4, padx=1, pady=1, columnspan=1, rowspan=1)
    #################################################
    #################################################
    
    #################################################
    #################################################
    ExternalUpdateSetupDict_Button = Button(AllButtonsGuiFrame, text='ExternalUpdateSetupDict', state="normal", width=20, font=("Helvetica", 8), command=lambda i=1: ExternalUpdateSetupDict_ButtonResponse())
    ExternalUpdateSetupDict_Button.grid(row=0, column=5, padx=1, pady=1, columnspan=1, rowspan=1)
    #################################################
    #################################################

    #################################################
    #################################################
    root.after(GUI_RootAfterCallbackInterval_Milliseconds, GUI_update_clock)
    root.mainloop()
    #################################################
    #################################################

    #################################################
    #################################################
    root.quit() #Stop the GUI thread, MUST BE CALLED FROM GUI_Thread
    root.destroy() #Close down the GUI thread, MUST BE CALLED FROM GUI_Thread
    #################################################
    #################################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
if __name__ == '__main__':

    ##########################################################################################################
    ##########################################################################################################
    global EXIT_PROGRAM_FLAG
    EXIT_PROGRAM_FLAG = 0
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    CTRLc_RegisterHandlerFunction()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    random.seed() #For random-number-generation
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
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
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    global USE_MyPlotterPureTkinterStandAloneProcess_FLAG
    USE_MyPlotterPureTkinterStandAloneProcess_FLAG = 1

    global USE_GUI_FLAG
    USE_GUI_FLAG = 1

    global USE_KEYBOARD_FLAG
    USE_KEYBOARD_FLAG = 1

    global TEST_WATCHDOG_FLAG
    TEST_WATCHDOG_FLAG = 1
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    global SHOW_IN_GUI_MyPlotterPureTkinterStandAloneProcess_FLAG
    SHOW_IN_GUI_MyPlotterPureTkinterStandAloneProcess_FLAG = 1
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    global root

    global root_Xpos
    root_Xpos = 0

    global root_Ypos
    root_Ypos = 0

    global root_width
    root_width = 1280

    global root_height
    root_height = 50

    global GUI_RootAfterCallbackInterval_Milliseconds
    GUI_RootAfterCallbackInterval_Milliseconds = 30

    global PARENT_GUI_COUNTER
    PARENT_GUI_COUNTER = 0
    
    global CurrentTime_CalculatedFromMainThread
    CurrentTime_CalculatedFromMainThread = -11111.0

    global StartingTime_CalculatedFromMainThread
    StartingTime_CalculatedFromMainThread = -11111.0

    global LoopCounter_CalculatedFromMainThread
    LoopCounter_CalculatedFromMainThread = 0

    global PeriodicInput_AcceptableValues
    PeriodicInput_AcceptableValues = ["GUI", "Sine", "Cosine", "Triangular", "Square"]

    global PeriodicInput_Type_1
    PeriodicInput_Type_1 = "Sine"

    global PeriodicInput_MinValue_1
    PeriodicInput_MinValue_1 = -1.0

    global PeriodicInput_MaxValue_1
    PeriodicInput_MaxValue_1 = 1.0

    global PeriodicInput_Period_1
    PeriodicInput_Period_1 = 1.0

    global PeriodicInput_CalculatedValue_1
    PeriodicInput_CalculatedValue_1 = 0.0

    global PeriodicInput_Type_2
    PeriodicInput_Type_2 = "Sine"

    global PeriodicInput_MinValue_2
    PeriodicInput_MinValue_2 = -1.0

    global PeriodicInput_MaxValue_2
    PeriodicInput_MaxValue_2 = 1.0

    global PeriodicInput_Period_2
    PeriodicInput_Period_2 = 1.0

    global PeriodicInput_CalculatedValue_2
    PeriodicInput_CalculatedValue_2 = 0.0
    
    global NoiseCounter
    NoiseCounter = 0

    global NoiseCounter_FireEveryNth
    NoiseCounter_FireEveryNth = 5

    global NoiseAmplitude_Percent0to1OfPeriodicInputAmplitude
    NoiseAmplitude_Percent0to1OfPeriodicInputAmplitude = 0.25

    global ToggleAutoscale_EventNeedsToBeFiredFlag
    ToggleAutoscale_EventNeedsToBeFiredFlag = 0
    
    global ToggleFreezePlot_EventNeedsToBeFiredFlag
    ToggleFreezePlot_EventNeedsToBeFiredFlag = 0
    
    global SavePlot_EventNeedsToBeFiredFlag
    SavePlot_EventNeedsToBeFiredFlag = 0
    
    global ResetMinAndMax_EventNeedsToBeFiredFlag
    ResetMinAndMax_EventNeedsToBeFiredFlag = 0
    
    global ClearPlot_EventNeedsToBeFiredFlag
    ClearPlot_EventNeedsToBeFiredFlag = 0
    
    global ExternalUpdateSetupDict_EventNeedsToBeFiredFlag
    ExternalUpdateSetupDict_EventNeedsToBeFiredFlag = 0

    global ExternalUpdateSetupDict_EventCounter
    ExternalUpdateSetupDict_EventCounter = 1
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    global MyPlotterPureTkinterStandAloneProcess_Object

    global MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG
    MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG = -1

    global MyPlotterPureTkinterStandAloneProcess_MostRecentDict
    MyPlotterPureTkinterStandAloneProcess_MostRecentDict = dict()

    global MyPlotterPureTkinterStandAloneProcess_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag
    MyPlotterPureTkinterStandAloneProcess_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag = -1

    global LastTime_CalculatedFromMainThread_MyPlotterPureTkinterStandAloneProcess
    LastTime_CalculatedFromMainThread_MyPlotterPureTkinterStandAloneProcess = -11111.0
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################  KEY GUI LINE
    ##########################################################################################################
    if USE_GUI_FLAG == 1:
        print("Starting GUI thread...")
        GUI_Thread_ThreadingObject = threading.Thread(target=GUI_Thread, daemon=True) #Daemon=True means that the GUI thread is destroyed automatically when the main thread is destroyed.
        GUI_Thread_ThreadingObject.start()
    else:
        root = None
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    global MyPlotterPureTkinterStandAloneProcess_GUIparametersDict
    MyPlotterPureTkinterStandAloneProcess_GUIparametersDict = dict([("EnableInternal_MyPrint_Flag", 1),
                                                                    ("NumberOfPrintLines", 10),
                                                                    ("GraphCanvasWidth", 1280),
                                                                    ("GraphCanvasHeight", 700),
                                                                    ("GraphCanvasWindowStartingX", 0),
                                                                    ("GraphCanvasWindowStartingY", 110),
                                                                    ("GraphCanvasWindowTitle", "My plotting example!"),
                                                                    ("GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents", 30)])


    global MyPlotterPureTkinterStandAloneProcess_SetupDict
    MyPlotterPureTkinterStandAloneProcess_SetupDict = dict([("GUIparametersDict", MyPlotterPureTkinterStandAloneProcess_GUIparametersDict),
                                                            ("ParentPID", os.getpid()),
                                                            ("WatchdogTimerDurationSeconds_ExpirationWillEndStandAlonePlottingProcess", 5.0),
                                                            ("CurvesToPlotNamesAndColorsDictOfLists", dict([("NameList", ["PlotCurve1", "PlotCurve2", "PlotCurve3"]),
                                                                                                        ("MarkerSizeList", [3, 2, 1]),
                                                                                                        ("LineWidthList", [2, 1, 0]),
                                                                                                        ("IncludeInXaxisAutoscaleCalculationList", [1, 1, 1]),
                                                                                                        ("IncludeInYaxisAutoscaleCalculationList", [1, 1, 1]),
                                                                                                        ("ColorList", ["Red", "Green", "Blue"])])),
                                                            ("SmallTextSize", 7),
                                                            ("LargeTextSize", 12),
                                                            ("NumberOfDataPointToPlot", 100),
                                                            ("XaxisNumberOfTickMarks", 10),
                                                            ("YaxisNumberOfTickMarks", 10),
                                                            ("XaxisNumberOfDecimalPlacesForLabels", 3),
                                                            ("YaxisNumberOfDecimalPlacesForLabels", 3),
                                                            ("XaxisAutoscaleFlag", 1),
                                                            ("YaxisAutoscaleFlag", 0),
                                                            ("X_min", 0.0),
                                                            ("X_max", 5.0),
                                                            ("Y_min", -5.0),
                                                            ("Y_max", 5.0),
                                                            ("XaxisDrawnAtBottomOfGraph", 0),
                                                            ("XaxisLabelString", "Time (sec)"),
                                                            ("YaxisLabelString", "Y-units (units)"),
                                                            ("ShowLegendFlag", 1),
                                                            ("GraphNumberOfLeadingZeros", 0),
                                                            ("GraphNumberOfDecimalPlaces", 3),
                                                            ("SavePlot_DirectoryPath", os.path.join(os.getcwd(), "SavedImagesFolder")),
                                                            ("KeepPlotterWindowAlwaysOnTopFlag", 0),
                                                            ("RemoveTitleBorderCloseButtonAndDisallowWindowMoveFlag", 0),
                                                            ("AllowResizingOfWindowFlag", 1)])
    
    if USE_MyPlotterPureTkinterStandAloneProcess_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            MyPlotterPureTkinterStandAloneProcess_Object = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class(MyPlotterPureTkinterStandAloneProcess_SetupDict)
            MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG = MyPlotterPureTkinterStandAloneProcess_Object.OBJECT_CREATED_SUCCESSFULLY_FLAG
            
        except:
            exceptions = sys.exc_info()[0]
            print("MyPlotterPureTkinterStandAloneProcess_Object, exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    if USE_MyPlotterPureTkinterStandAloneProcess_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG != 1:
                print("Failed to open MyPlotterPureTkinterClass_Object.")
                ExitProgram_Callback()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    if USE_KEYBOARD_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        keyboard.on_press_key("esc", ExitProgram_Callback)
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    if EXIT_PROGRAM_FLAG == 0:
        print("$$$$$$$$$$$$$$ Starting test_program_for_MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class.py $$$$$$$$$$$$$$")
        StartingTime_CalculatedFromMainThread = getPreciseSecondsTimeStampString()
    ##########################################################################################################
    ##########################################################################################################

    #####################################################################################################
    #####################################################################################################
    #####################################################################################################
    while(EXIT_PROGRAM_FLAG == 0):

        #####################################################################################################
        #####################################################################################################
        CurrentTime_CalculatedFromMainThread = getPreciseSecondsTimeStampString() - StartingTime_CalculatedFromMainThread
        LoopCounter_CalculatedFromMainThread = LoopCounter_CalculatedFromMainThread + 1

        if CurrentTime_CalculatedFromMainThread > 60:
            ExitProgram_Callback()
        #####################################################################################################
        #####################################################################################################

        ######################################################################################################
        ######################################################################################################
        AmplitudeScalar = GetLatestWaveformValue(CurrentTime_CalculatedFromMainThread, 
                                                                1.0, 
                                                                10.0, 
                                                                PeriodicInput_Period_1, 
                                                                PeriodicInput_Type_1)
                                                                
        PeriodicInput_CalculatedValue_1 = GetLatestWaveformValue(CurrentTime_CalculatedFromMainThread, 
                                                                AmplitudeScalar*PeriodicInput_MinValue_1, 
                                                                AmplitudeScalar*PeriodicInput_MaxValue_1, 
                                                                PeriodicInput_Period_1, 
                                                                PeriodicInput_Type_1)
        ######################################################################################################
        ######################################################################################################

        ######################################################################################################
        ######################################################################################################

        ######################################################################################################
        PeriodicInput_CalculatedValue_2 = PeriodicInput_CalculatedValue_1*2.0 + 3.0
        ######################################################################################################

        ######################################################################################################
        NoiseCounter = NoiseCounter + 1
        if NoiseCounter == NoiseCounter_FireEveryNth:
            NoiseAmplitude = NoiseAmplitude_Percent0to1OfPeriodicInputAmplitude * abs(PeriodicInput_MaxValue_1 - PeriodicInput_MinValue_1)
            NoiseValue = random.uniform(-1.0 * NoiseAmplitude, NoiseAmplitude)
            PeriodicInput_CalculatedValue_2 = PeriodicInput_CalculatedValue_2 + NoiseValue
            NoiseCounter = 0
        ######################################################################################################
        
        ######################################################################################################
        ######################################################################################################

        ######################################################################################################
        ######################################################################################################
        if MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG == 1:
                
            #####################################################################################################
            if ToggleAutoscale_EventNeedsToBeFiredFlag == 1:
                MyPlotterPureTkinterStandAloneProcess_Object.SendToggleAutoscaleCommandToStandAloneProcess()
                ToggleAutoscale_EventNeedsToBeFiredFlag = 0
            #####################################################################################################
            
            #####################################################################################################
            if ToggleFreezePlot_EventNeedsToBeFiredFlag == 1:
                MyPlotterPureTkinterStandAloneProcess_Object.SendToggleFreezePlotCommandToStandAloneProcess()
                ToggleFreezePlot_EventNeedsToBeFiredFlag = 0
            #####################################################################################################
                
            #####################################################################################################
            if SavePlot_EventNeedsToBeFiredFlag == 1:
                MyPlotterPureTkinterStandAloneProcess_Object.SendSavePlotCommandToStandAloneProcess()
                SavePlot_EventNeedsToBeFiredFlag = 0
            #####################################################################################################
                
            #####################################################################################################
            if ResetMinAndMax_EventNeedsToBeFiredFlag == 1:
                MyPlotterPureTkinterStandAloneProcess_Object.SendResetMinAndMaxCommandToStandAloneProcess()
                ResetMinAndMax_EventNeedsToBeFiredFlag = 0
            #####################################################################################################

            #####################################################################################################
            if ClearPlot_EventNeedsToBeFiredFlag == 1:
                MyPlotterPureTkinterStandAloneProcess_Object.SendClearPlotCommandToStandAloneProcess()
                ClearPlot_EventNeedsToBeFiredFlag = 0
            #####################################################################################################

            #####################################################################################################
            if ExternalUpdateSetupDict_EventNeedsToBeFiredFlag == 1:

                if ExternalUpdateSetupDict_EventCounter % 2 == 0: #even
                    MyPlotterPureTkinterStandAloneProcess_SetupDict["CurvesToPlotNamesAndColorsDictOfLists"]["ColorList"] = ["Red", "Green", "Blue"]
                    MyPlotterPureTkinterStandAloneProcess_SetupDict["KeepPlotterWindowAlwaysOnTopFlag"] = 0
                    MyPlotterPureTkinterStandAloneProcess_SetupDict["RemoveTitleBorderCloseButtonAndDisallowWindowMoveFlag"] = 0
                    MyPlotterPureTkinterStandAloneProcess_SetupDict["AllowResizingOfWindowFlag"] = 1

                else:
                    MyPlotterPureTkinterStandAloneProcess_SetupDict["CurvesToPlotNamesAndColorsDictOfLists"]["ColorList"] = ["Purple", "Orange", "Yellow"]
                    MyPlotterPureTkinterStandAloneProcess_SetupDict["KeepPlotterWindowAlwaysOnTopFlag"] = 1
                    MyPlotterPureTkinterStandAloneProcess_SetupDict["RemoveTitleBorderCloseButtonAndDisallowWindowMoveFlag"] = 1
                    MyPlotterPureTkinterStandAloneProcess_SetupDict["AllowResizingOfWindowFlag"] = 0

                MyPlotterPureTkinterStandAloneProcess_Object.ExternalUpdateSetupDict(MyPlotterPureTkinterStandAloneProcess_SetupDict)
                ExternalUpdateSetupDict_EventCounter = ExternalUpdateSetupDict_EventCounter + 1
                ExternalUpdateSetupDict_EventNeedsToBeFiredFlag = 0
            #####################################################################################################
            
        ######################################################################################################
        ######################################################################################################
        
        ###################################################################################################### SET's
        ######################################################################################################
        if MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG == 1:

            ######################################################################################################
            try:
                MyPlotterPureTkinterStandAloneProcess_MostRecentDict = MyPlotterPureTkinterStandAloneProcess_Object.GetMostRecentDataDict()

                if "StandAlonePlottingProcess_ReadyForWritingFlag" in MyPlotterPureTkinterStandAloneProcess_MostRecentDict:
                    MyPlotterPureTkinterStandAloneProcess_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag = MyPlotterPureTkinterStandAloneProcess_MostRecentDict["StandAlonePlottingProcess_ReadyForWritingFlag"]

                    if MyPlotterPureTkinterStandAloneProcess_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag == 1:
                        if CurrentTime_CalculatedFromMainThread - LastTime_CalculatedFromMainThread_MyPlotterPureTkinterStandAloneProcess >= MyPlotterPureTkinterStandAloneProcess_GUIparametersDict["GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents"]/1000.0 + 0.001:
                            MyPlotterPureTkinterStandAloneProcess_Object.ExternalAddPointOrListOfPointsToPlot(["PlotCurve1",
                                                                                                             "PlotCurve2"],
                                                                                                            [CurrentTime_CalculatedFromMainThread]*2,
                                                                                                            [PeriodicInput_CalculatedValue_1,
                                                                                                            PeriodicInput_CalculatedValue_2],
                                                                                                            PrintInfoForDebuggingFlag=0)

                            LastTime_CalculatedFromMainThread_MyPlotterPureTkinterStandAloneProcess = CurrentTime_CalculatedFromMainThread
            ######################################################################################################

            ######################################################################################################
            except:
                exceptions = sys.exc_info()[0]
                print("MyPlotterPureTkinterStandAloneProcess, exceptions: %s" % exceptions)
                #traceback.print_exc()
            ######################################################################################################

        ######################################################################################################
        ######################################################################################################

        time.sleep(0.030) #unicorn

    #####################################################################################################
    #####################################################################################################
    #####################################################################################################

    ########################################################################################################## THIS IS THE EXIT ROUTINE!
    ##########################################################################################################
    print("$$$$$$$$$$$$$$ Ending test_program_for_MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class.py $$$$$$$$$$$$$$")

    ##########################################################################################################
    if MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG == 1:

        if TEST_WATCHDOG_FLAG == 0:
            MyPlotterPureTkinterStandAloneProcess_Object.ExitProgram_Callback()
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
