# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision G, 02/02/2025

Verified working on: Python 3.12 for Windows 11 64-bit.
'''

__author__ = 'reuben.brewer'

#########################################################
#https://github.com/Reuben-Brewer/ArucoTagDetectionFromCameraFeed_ReubenPython3Class
from ArucoTagDetectionFromCameraFeed_ReubenPython3Class import *

#https://github.com/Reuben-Brewer/CSVdataLogger_ReubenPython3Class
from CSVdataLogger_ReubenPython3Class import *

#https://github.com/Reuben-Brewer/LowPassFilterForDictsOfLists_ReubenPython2and3Class
from LowPassFilterForDictsOfLists_ReubenPython2and3Class import *

#https://github.com/Reuben-Brewer/MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class
from MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class import *

#https://github.com/Reuben-Brewer/MyPrint_ReubenPython2and3Class
from MyPrint_ReubenPython2and3Class import *
#########################################################

#########################################################
import os
import sys
import platform
import time
import datetime
import threading
import collections
import argparse
import json
import numpy
import cv2
from circle_fitting_3d import Circle3D #pip install circle-fitting-3d
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

#######################################################################################################################
#######################################################################################################################
global ParametersToBeLoaded_Directory_Windows
ParametersToBeLoaded_Directory_Windows = os.getcwd().replace("\\", "//") + "//ParametersToBeLoaded"

global LogFile_Directory_Windows
LogFile_Directory_Windows = os.getcwd().replace("\\", "//") + "//Logs"

global ParametersToBeLoaded_Directory_LinuxNonRaspberryPi
ParametersToBeLoaded_Directory_LinuxNonRaspberryPi = os.getcwd().replace("\\", "//") + "//ParametersToBeLoaded"

global LogFile_Directory_LinuxNonRaspberryPi
LogFile_Directory_LinuxNonRaspberryPi = os.getcwd().replace("\\", "//") + "//Logs"

global ParametersToBeLoaded_Directory_Mac
ParametersToBeLoaded_Directory_Mac = os.getcwd().replace("\\", "//") + "//ParametersToBeLoaded"

global LogFile_Directory_Mac
LogFile_Directory_Mac = os.getcwd().replace("\\", "//") + "//Logs"
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def getPreciseSecondsTimeStampString():
    ts = time.time()

    return ts
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def getTimeStampString():

    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%m_%d_%Y---%H_%M_%S')

    return st
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def GetMyPlatform():
    my_platform = "other"

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

    return my_platform
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def ParseARGV_USE_GUI_and_SOFTWARE_LAUNCH_METHOD():

    try:
        USE_GUI_FLAG_ARGV_OVERRIDE = -1
        SOFTWARE_LAUNCH_METHOD = -1

        if len(sys.argv) >= 2:
            ARGV_1 = sys.argv[1].strip().lower()

            print("ARGV_1: " + str(ARGV_1))
            ARGV_1_ParsedDict = ParseColonCommaSeparatedVariableString(ARGV_1)

            if "use_gui_flag" in ARGV_1_ParsedDict:
                USE_GUI_FLAG_ARGV_OVERRIDE = PassThrough0and1values_ExitProgramOtherwise("USE_GUI_FLAG_ARGV_OVERRIDE", int(ARGV_1_ParsedDict["use_gui_flag"]))

            if "software_launch_method" in ARGV_1_ParsedDict:
                SOFTWARE_LAUNCH_METHOD = ARGV_1_ParsedDict["software_launch_method"]

    except:
        exceptions = sys.exc_info()[0]
        print("Parsing ARGV_1, exceptions: %s" % exceptions)
        traceback.print_exc()
        time.sleep(0.25)

    #print("ARGV_1, USE_GUI_FLAG_ARGV_OVERRIDE: " + str(USE_GUI_FLAG_ARGV_OVERRIDE))
    #print("ARGV_1, SOFTWARE_LAUNCH_METHOD: " + str(SOFTWARE_LAUNCH_METHOD))

    return [USE_GUI_FLAG_ARGV_OVERRIDE, SOFTWARE_LAUNCH_METHOD]

#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def ParseColonCommaSeparatedVariableString(line, print_line_flag = 0, numeric_values_only = 0):

    if print_line_flag == 1:
        print("ParseColonCommaSeparatedVariableString input: " + line)

    line_as_dict = dict()

    if len(line) > 0:
        try:
            line = line.replace("\n", "").replace("\r", "")
            line_as_list = filter(None, re.split("[,:]+", line))
            #print(line_as_list)

            toggle_counter = 0
            key = ""
            for element in line_as_list:
                if toggle_counter == 0:  # Every other element is a key, every other element is the value
                    key = element.strip()
                    toggle_counter = 1
                else:
                    if numeric_values_only == 1:
                        try:
                            line_as_dict[key] = float(element)
                            #print(key + " , " + element)
                        except:
                            line_as_dict[key] = "ERROR"
                    else:
                        line_as_dict[key] = element
                    toggle_counter = 0

            return line_as_dict
        except:
            exceptions = sys.exc_info()[0]
            print("ParseColonCommaSeparatedVariableString ERROR: Exceptions: %s" % exceptions)
            traceback.print_exc()
            return line_as_dict
    else:
        print("ParseColonCommaSeparatedVariableString WARNING: input string was zero-length")
        return line_as_dict
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def IsTheTimeCurrentlyAM():
    ts = time.time()
    hour = int(datetime.datetime.fromtimestamp(ts).strftime('%H'))
    if hour < 12:
        return 1
    else:
        return 0
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def PassThrough0and1values_ExitProgramOtherwise(InputNameString, InputNumber):

    try:
        InputNumber_ConvertedToFloat = float(InputNumber)
    except:
        exceptions = sys.exc_info()[0]
        print("PassThrough0and1values_ExitProgramOtherwise Error. InputNumber for variable_name '" + InputNameString + "' must be a float value, Exceptions: %s" % exceptions)
        input("Press any key to continue")
        sys.exit()

    try:
        if InputNumber_ConvertedToFloat == 0.0 or InputNumber_ConvertedToFloat == 1:
            return InputNumber_ConvertedToFloat
        else:
            input("PassThrough0and1values_ExitProgramOtherwise Error. '" + InputNameString + "' must be 0 or 1 (value was " + str(InputNumber_ConvertedToFloat) + "). Press any key (and enter) to exit.")
            sys.exit()
    except:
        exceptions = sys.exc_info()[0]
        print("PassThrough0and1values_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)
        input("Press any key to continue")
        sys.exit()

#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def PassThroughFloatValuesInRange_ExitProgramOtherwise(InputNameString, InputNumber, RangeMinValue, RangeMaxValue):

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
            input("PassThroughFloatValuesInRange_ExitProgramOtherwise Error. '" + InputNameString + "' must be in the range [" + str(RangeMinValue) + ", " + str(RangeMaxValue) + "] (value was " + str(InputNumber_ConvertedToFloat) + "). Press any key (and enter) to exit.")
            sys.exit()
    except:
        exceptions = sys.exc_info()[0]
        print("PassThroughFloatValuesInRange_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)
        input("Press any key to continue")
        sys.exit()

#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def LoadAndParseJSONfile_UseClassesFlags():
    global ParametersToBeLoaded_UseClassesFlags_Dict

    print("Calling LoadAndParseJSONfile_UseClassesFlags().")

    #################################
    JSONfilepathFull_UseClassesFlags = ParametersToBeLoaded_Directory_TO_BE_USED + "//ParametersToBeLoaded_UseClassesFlags.json"

    ParametersToBeLoaded_UseClassesFlags_Dict = LoadAndParseJSONfile_AddDictKeysToGlobalsDict(globals(), JSONfilepathFull_UseClassesFlags, 1, 1)
    #################################

    #################################
    if USE_GUI_FLAG_ARGV_OVERRIDE != -1:
        USE_GUI_FLAG = USE_GUI_FLAG_ARGV_OVERRIDE
    else:
        USE_GUI_FLAG = PassThrough0and1values_ExitProgramOtherwise("USE_GUI_FLAG", ParametersToBeLoaded_UseClassesFlags_Dict["USE_GUI_FLAG"])
    #################################

#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def LoadAndParseJSONfile_GUIsettings():
    global ParametersToBeLoaded_GUIsettings_Dict

    print("Calling LoadAndParseJSONfile_GUIsettings().")

    #################################
    JSONfilepathFull_GUIsettings = ParametersToBeLoaded_Directory_TO_BE_USED + "//ParametersToBeLoaded_GUIsettings.json"

    ParametersToBeLoaded_GUIsettings_Dict = LoadAndParseJSONfile_AddDictKeysToGlobalsDict(globals(), JSONfilepathFull_GUIsettings, 1, 1)
    #################################

#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def LoadAndParseJSONfile_Camera():
    global ParametersToBeLoaded_Camera_Dict

    #################################
    JSONfilepathFull_Camera = ParametersToBeLoaded_Directory_TO_BE_USED + "//ParametersToBeLoaded_Camera.json"

    ParametersToBeLoaded_Camera_Dict = LoadAndParseJSONfile_AddDictKeysToGlobalsDict(globals(), JSONfilepathFull_Camera, 1, 1)
    #################################

    #################################
    for Key in CameraCalibrationParametersDict:
        if Key == "fx" or Key == "fy" or Key == "cx" or Key == "cy":
            CameraCalibrationParametersDict[Key] = CameraCalibrationResolutionScalarMultiplier*CameraCalibrationParametersDict[Key]
     #################################

    print("CameraCalibrationParametersDict: " + str(CameraCalibrationParametersDict))

#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def LoadAndParseJSONfile_ArucoTagParameters():
    global ParametersToBeLoaded_ArucoTagParameters_Dict
    global ArucoTag_MarkerIDToDetect_PrimaryMarker
    global ArucoTag_MarkerIDToDetect_SecondaryMarker

    #################################
    JSONfilepathFull_ArucoTagParameters = ParametersToBeLoaded_Directory_TO_BE_USED + "//ParametersToBeLoaded_ArucoTagParameters.json"

    ParametersToBeLoaded_ArucoTagParameters_Dict = LoadAndParseJSONfile_AddDictKeysToGlobalsDict(globals(), JSONfilepathFull_ArucoTagParameters, 1, 1)
    #################################

    ArucoTag_MarkerIDToDetect_PrimaryMarker = str(ArucoTag_MarkerIDToDetect_PrimaryMarker)
    ArucoTag_MarkerIDToDetect_SecondaryMarker = str(ArucoTag_MarkerIDToDetect_SecondaryMarker)

#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def LoadAndParseJSONfile_SavingSettings():
    global ParametersToBeLoaded_SavingSettings_Dict

    print("Calling LoadAndParseJSONfile_SavingSettings().")

    #################################
    JSONfilepathFull_SavingSettings = ParametersToBeLoaded_Directory_TO_BE_USED + "//ParametersToBeLoaded_SavingSettings.json"

    ParametersToBeLoaded_SavingSettings_Dict = LoadAndParseJSONfile_AddDictKeysToGlobalsDict(globals(), JSONfilepathFull_SavingSettings, 1, 1)
    #################################

#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def LoadAndParseJSONfile_MyPlotterPureTkinterStandAloneProcess():
    global ParametersToBeLoaded_MyPlotterPureTkinterStandAloneProcess_Dict

    print("Calling LoadAndParseJSONfile_MyPlotterPureTkinterStandAloneProcess().")

    #################################
    JSONfilepathFull_MyPlotterPureTkinterStandAloneProcess = ParametersToBeLoaded_Directory_TO_BE_USED + "//ParametersToBeLoaded_MyPlotterPureTkinterStandAloneProcess.json"

    ParametersToBeLoaded_MyPlotterPureTkinterStandAloneProcess_Dict = LoadAndParseJSONfile_AddDictKeysToGlobalsDict(globals(), JSONfilepathFull_MyPlotterPureTkinterStandAloneProcess, 1, 1)
    #################################

#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def LoadAndParseJSONfile_AddDictKeysToGlobalsDict(GlobalsDict, JSONfilepathFull, USE_PassThrough0and1values_ExitProgramOtherwise_FOR_FLAGS = 0, PrintResultsFlag = 0):

    try:
        #################################

        ##############
        with open(JSONfilepathFull) as ParametersToBeLoaded_JSONfileObject:
            ParametersToBeLoaded_JSONfileParsedIntoDict = json.load(ParametersToBeLoaded_JSONfileObject)

        ParametersToBeLoaded_JSONfileObject.close()
        ##############

        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        ##############
        for key, value in ParametersToBeLoaded_JSONfileParsedIntoDict.items():
            if USE_PassThrough0and1values_ExitProgramOtherwise_FOR_FLAGS == 1:
                if key.upper().find("_FLAG") != -1:
                    GlobalsDict[key] = PassThrough0and1values_ExitProgramOtherwise(key, value)
                else:
                    GlobalsDict[key] = value
            else:
                GlobalsDict[key] = value

            if PrintResultsFlag == 1:
                print(key + ": " + str(value))

        ##############
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

        return ParametersToBeLoaded_JSONfileParsedIntoDict
        #################################
    except:
        #################################
        exceptions = sys.exc_info()[0]
        print("LoadAndParseJSONfile_Advanced Error, Exceptions: %s" % exceptions)
        traceback.print_exc()
        return dict()
        #################################

#######################################################################################################################
#######################################################################################################################

##########################################################################################################
##########################################################################################################
def GUI_update_clock():
    global root
    global EXIT_PROGRAM_FLAG
    global GUI_RootAfterCallbackInterval_Milliseconds
    global USE_GUI_FLAG

    global ArucoTagDetectionFromCameraFeed_ReubenPython3ClassObject
    global ArucoTag_OPEN_FLAG
    global SHOW_IN_GUI_ArucoTag_FLAG

    global CSVdataLogger_ReubenPython3ClassObject
    global CSVdataLogger_OPEN_FLAG
    global SHOW_IN_GUI_CSVdataLogger_FLAG

    global MyPrint_ReubenPython2and3ClassObject
    global MyPrint_OPEN_FLAG
    global SHOW_IN_GUI_MyPrint_FLAG

    if USE_GUI_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
        #########################################################
        #########################################################

            #########################################################
            if ArucoTag_OPEN_FLAG == 1 and SHOW_IN_GUI_ArucoTag_FLAG == 1:
                ArucoTagDetectionFromCameraFeed_ReubenPython3ClassObject.GUI_update_clock()
            #########################################################

            #########################################################
            if CSVdataLogger_OPEN_FLAG == 1 and SHOW_IN_GUI_CSVdataLogger_FLAG == 1:
                CSVdataLogger_ReubenPython3ClassObject.GUI_update_clock()
            #########################################################

            #########################################################
            if MyPrint_OPEN_FLAG == 1 and SHOW_IN_GUI_MyPrint_FLAG == 1:
                MyPrint_ReubenPython2and3ClassObject.GUI_update_clock()
            #########################################################

            root.after(GUI_RootAfterCallbackInterval_Milliseconds, GUI_update_clock)
        #########################################################
        #########################################################

##########################################################################################################
##########################################################################################################

#######################################################################################################################
#######################################################################################################################
def ExitProgram_Callback():
    global EXIT_PROGRAM_FLAG
    global CSVdataLogger_ReubenPython3ClassObject
    global CSVdataLogger_OPEN_FLAG
    global ArucoTagDetectionFromCameraFeed_ReubenPython3ClassObject
    global ArucoTag_OPEN_FLAG

    print("ExitProgram_Callback event fired!")

    if (CSVdataLogger_OPEN_FLAG == 1 and CSVdataLogger_ReubenPython3ClassObject.IsSaving() == 0) and (ArucoTag_OPEN_FLAG == 1 and ArucoTagDetectionFromCameraFeed_ReubenPython3ClassObject.IsSaving() == 0):
        EXIT_PROGRAM_FLAG = 1
    else:
        print("ExitProgram_Callback, ERROR! Still saving data.")
#######################################################################################################################
#######################################################################################################################

##########################################################################################################
##########################################################################################################
def GUI_Thread():
    global my_platform
    global root
    global root_Xpos
    global root_Ypos
    global root_width
    global root_height
    global GUItitleString
    global GUI_RootAfterCallbackInterval_Milliseconds
    global GUIbuttonWidth
    global GUIbuttonPadX
    global GUIbuttonPadY
    global GUIbuttonFontSize
    global USE_GUI_FLAG
    global TKinter_LightRedColor
    global TKinter_LightGreenColor
    global TKinter_LightBlueColor
    global TKinter_LightYellowColor
    global TKinter_DefaultGrayColor
    global SHOW_IN_GUI_UR5arm_MostRecentDict_FLAG

    ########################################################### KEY GUI LINE
    ###########################################################
    root = Tk()
    ###########################################################
    ###########################################################

    ###########################################################SET THE DEFAULT FONT FOR ALL WIDGETS CREATED AFTTER/BELOW THIS CALL
    ###########################################################
    default_font = tkFont.nametofont("TkDefaultFont")
    default_font.configure(size=8)
    root.option_add("*Font", default_font)
    ###########################################################
    ###########################################################

    ###########################################################
    ###########################################################
    TKinter_LightRedColor = '#%02x%02x%02x' % (255, 150, 150)  # RGB
    TKinter_LightGreenColor = '#%02x%02x%02x' % (150, 255, 150)  # RGB
    TKinter_LightBlueColor = '#%02x%02x%02x' % (150, 150, 255)  # RGB
    TKinter_LightYellowColor = '#%02x%02x%02x' % (255, 255, 150)  # RGB
    TKinter_DefaultGrayColor = '#%02x%02x%02x' % (240, 240, 240)  # RGB
    ###########################################################
    ###########################################################

    ############################################
    ############################################
    global TabControlObject
    global Tab_MainControls
    global Tab_ArucoTagDetection
    global Tab_MyPrint

    TabControlObject = ttk.Notebook(root)

    Tab_ArucoTagDetection = ttk.Frame(TabControlObject)
    TabControlObject.add(Tab_ArucoTagDetection, text='   ArucoTagDetection  ')

    Tab_MainControls = ttk.Frame(TabControlObject)
    TabControlObject.add(Tab_MainControls, text='   Main Controls   ')

    Tab_MyPrint = ttk.Frame(TabControlObject)
    TabControlObject.add(Tab_MyPrint, text='   MyPrint Terminal   ')

    TabControlObject.pack(expand=1, fill="both")  # CANNOT MIX PACK AND GRID IN THE SAME FRAME/TAB, SO ALL .GRID'S MUST BE CONTAINED WITHIN THEIR OWN FRAME/TAB.

    ############# #Set the tab header font
    TabStyle = ttk.Style()
    TabStyle.configure('TNotebook.Tab', font=('Helvetica', '12', 'bold'))
    #############

    #################################################
    #################################################

    ############################################
    ############################################
    global JSONfiles_NeedsToBeLoadedFlagButton
    JSONfiles_NeedsToBeLoadedFlagButton = Button(Tab_MainControls, text="Load JSON files", state="normal", width=GUIbuttonWidth, command=lambda i=1: JSONfiles_NeedsToBeLoadedFlag_ButtonResponse())
    JSONfiles_NeedsToBeLoadedFlagButton.grid(row=0, column=1, padx=GUIbuttonPadX, pady=GUIbuttonPadY, columnspan=1, rowspan=1,)
    JSONfiles_NeedsToBeLoadedFlagButton.config(font=("Helvetica", GUIbuttonFontSize))
    ############################################
    ############################################

    ########################################################### THIS BLOCK MUST COME 2ND-TO-LAST IN def  GUI_Thread() IF USING TABS.
    ###########################################################
    root.protocol("WM_DELETE_WINDOW", ExitProgram_Callback)  # Set the callback function for when the window's closed.
    root.title(GUItitleString)
    root.after(GUI_RootAfterCallbackInterval_Milliseconds, GUI_update_clock)
    root.geometry('%dx%d+%d+%d' % (
    root_width, root_height, root_Xpos, root_Ypos))  # set the dimensions of the screen and where it is placed
    root.mainloop()
    ###########################################################
    ###########################################################

    ###########################################################
    ########################################################### THIS BLOCK MUST COME LAST IN def  GUI_Thread() REGARDLESS OF CODE.
    root.quit()  # Stop the GUI thread, MUST BE CALLED FROM GUI_Thread
    root.destroy()  # Close down the GUI thread, MUST BE CALLED FROM GUI_Thread
    ###########################################################
    ###########################################################

##########################################################################################################
##########################################################################################################

#######################################################################################################################
#######################################################################################################################
def JSONfiles_NeedsToBeLoadedFlag_ButtonResponse():
    global JSONfiles_NeedsToBeLoadedFlag

    JSONfiles_NeedsToBeLoadedFlag = 1

    MyPrint_ReubenPython2and3ClassObject.my_print("JSONfiles_NeedsToBeLoadedFlag_ButtonResponse event fired!")
#######################################################################################################################
#######################################################################################################################

##########################################################################################################
##########################################################################################################
def GetImageSizeAsHeightWidthNumberOfChannelsList(InputImageAsNumpyArray):

    try:

        ################################################
        if len(InputImageAsNumpyArray.shape) == 2:
            Height, Width = InputImageAsNumpyArray.shape
            NumberOfChannels = 1
        elif len(InputImageAsNumpyArray.shape) == 3:
            Height, Width, NumberOfChannels = InputImageAsNumpyArray.shape
        else:
            print("GetImageSizeAsHeightWidthNumberOfChannelsList, error: len(InputImageAsNumpyArray.shape) should be 2 or 3.")
            return [-1, -1, -1]

        return [Height, Width, NumberOfChannels]
        ################################################

    except:
        exceptions = sys.exc_info()[0]
        print("GetImageSizeAsHeightWidthNumberOfChannelsList, Exceptions: %s" % exceptions)
        #traceback.print_exc()
        return [-1, -1, -1]

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
if __name__ == '__main__':

    ################################################
    ################################################
    global EXIT_PROGRAM_FLAG
    EXIT_PROGRAM_FLAG = 0
    ################################################
    ################################################

    ################################################
    ################################################
    global my_platform
    global ParametersToBeLoaded_Directory_TO_BE_USED
    global LogFile_Directory_TO_BE_USED

    my_platform = GetMyPlatform()

    if my_platform == "windows":
        ParametersToBeLoaded_Directory_TO_BE_USED = ParametersToBeLoaded_Directory_Windows
        LogFile_Directory_TO_BE_USED = LogFile_Directory_Windows

    elif my_platform == "linux":
        ParametersToBeLoaded_Directory_TO_BE_USED = ParametersToBeLoaded_Directory_LinuxNonRaspberryPi
        LogFile_Directory_TO_BE_USED = LogFile_Directory_LinuxNonRaspberryPi

    elif my_platform == "mac":
        ParametersToBeLoaded_Directory_TO_BE_USED = ParametersToBeLoaded_Directory_Mac
        LogFile_Directory_TO_BE_USED = LogFile_Directory_Mac

    else:
        "test_program_for_ArucoTagDetectionFromCameraFeed_ReubenPython3Class.py.py: ERROR, OS must be Windows, LinuxNonRaspberryPi, or Mac!"
        ExitProgram_Callback()

    print("ParametersToBeLoaded_Directory_TO_BE_USED: " + ParametersToBeLoaded_Directory_TO_BE_USED)
    print("LogFile_Directory_TO_BE_USED: " + LogFile_Directory_TO_BE_USED)
    ################################################
    ################################################

    ################################################
    ################################################
    global USE_GUI_FLAG_ARGV_OVERRIDE
    global SOFTWARE_LAUNCH_METHOD

    [USE_GUI_FLAG_ARGV_OVERRIDE, SOFTWARE_LAUNCH_METHOD] =  ParseARGV_USE_GUI_and_SOFTWARE_LAUNCH_METHOD()

    print("test_program_for_ArucoTagDetectionFromCameraFeed_ReubenPython3Class.py, USE_GUI_FLAG_ARGV_OVERRIDE: " + str(USE_GUI_FLAG_ARGV_OVERRIDE) + ", SOFTWARE_LAUNCH_METHOD: " + str(SOFTWARE_LAUNCH_METHOD))

    '''
    if SOFTWARE_LAUNCH_METHOD == -1:
        print("test_program_for_ArucoTagDetectionFromCameraFeed_ReubenPython3Class.py ERROR, must launch software via command terminal/BAT-file, not IDE!")
        time.sleep(5.0)
        sys.exit()
    '''
    ################################################
    ################################################

    ################################################
    ################################################
    AMflag = IsTheTimeCurrentlyAM()
    if AMflag == 1:
        AMorPMstring = "AM"
    else:
        AMorPMstring = "PM"

    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print("Starting 'test_program_for_ArucoTagDetectionFromCameraFeed_ReubenPython3Class.py.py' at " + getTimeStampString() + AMorPMstring)
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    ################################################
    ################################################

    ##################################################
    #################################################
    global JSONfiles_NeedsToBeLoadedFlag
    JSONfiles_NeedsToBeLoadedFlag = 0

    #################################################
    global UseClassesFlags_Directions
    global USE_ArucoTag_FLAG
    global USE_CSVdataLogger_FLAG
    global USE_MyPlotterPureTkinterStandAloneProcess_FLAG
    global USE_MyPrint_FLAG
    global USE_GUI_FLAG

    LoadAndParseJSONfile_UseClassesFlags()
    #################################################

    #################################################
    global GUIsettings_Directions

    global SHOW_IN_GUI_ArucoTag_FLAG
    global SHOW_IN_GUI_CSVdataLogger_FLAG
    global SHOW_IN_GUI_MyPrint_FLAG
    global SHOW_IN_GUI_MyPlotterPureTkinterStandAloneProcess_FLAG

    global GUItitleString
    global GUI_RootAfterCallbackInterval_Milliseconds
    global root_Xpos
    global root_Ypos
    global root_width
    global root_height
    global GUIbuttonWidth
    global GUIbuttonPadX
    global GUIbuttonPadY
    global GUIbuttonFontSize

    global GUI_ROW_ArucoTagDetection
    global GUI_COLUMN_ArucoTagDetection
    global GUI_PADX_ArucoTagDetection
    global GUI_PADY_ArucoTagDetection
    global GUI_ROWSPAN_ArucoTagDetection
    global GUI_COLUMNSPAN_ArucoTagDetection

    global GUI_ROW_CSVdataLogger
    global GUI_COLUMN_CSVdataLogger
    global GUI_PADX_CSVdataLogger
    global GUI_PADY_CSVdataLogger
    global GUI_ROWSPAN_CSVdataLogger
    global GUI_COLUMNSPAN_CSVdataLogger

    global GUI_ROW_MyPrint
    global GUI_COLUMN_MyPrint
    global GUI_PADX_MyPrint
    global GUI_PADY_MyPrint
    global GUI_ROWSPAN_MyPrint
    global GUI_COLUMNSPAN_MyPrint

    LoadAndParseJSONfile_GUIsettings()
    #################################################

    #################################################
    global camera_selection_number
    global camera_TkinterPreviewImageScalingFactor
    global camera_Dshow_EnglishName
    global CameraCaptureThread_TimeToSleepEachLoop
    global CameraEncodeThread_TimeToSleepEachLoop
    global ImageSavingThread_TimeToSleepEachLoop
    global camera_frame_rate
    global image_width
    global image_height
    global image_jpg_encoding_quality
    global CameraSetting_Autofocus
    global CameraSetting_Autoexposure
    global CameraSetting_exposure
    global CameraSetting_gain
    global CameraSetting_brightness
    global CameraSetting_contrast
    global CameraSetting_saturation
    global CameraSetting_hue
    global DrawCircleAtImageCenterFlag
    global EnableCameraEncodeThreadFlag
    global EnableImageSavingThreadFlag
    global RemoveFisheyeDistortionFromImage_Flag
    global CameraCalibrationParametersDict
    global CameraCalibrationResolutionScalarMultiplier
    global ShowOpenCVwindowsFlag
    global OpenCVwindowPosX
    global OpenCVwindowPosY
    global OpenCVwindow_UpdateEveryNmilliseconds
    global test_program_for_ArucoTagDetectionFromCameraFeed_ReubenPython3Class_MainThread_TimeToSleepEachLoop
    global OpenCVbackendToUseEnglishName

    LoadAndParseJSONfile_Camera()
    #################################################

    #################################################
    global ArucoTag_user_notes
    global ArucoTag_TkinterPreviewImageScalingFactor
    global ArucoTag_DictType_EnglishString
    global ArucoTag_MarkerLengthInMillimeters
    global ArucoTag_AxesToDrawLengthInMillimeters
    global ArucoTag_TranslationVectorOfMarkerCenter_ExponentialSmoothingFilterLambda
    global ArucoTag_RotationVectorOfMarkerCenter_ExponentialSmoothingFilterLambda
    global ArucoTag_CircleDetection_ExponentialSmoothingFilterLambda

    LoadAndParseJSONfile_ArucoTagParameters()
    #################################################

    #################################################
    global SavingSettings_user_notes
    global Camera_SavedImages_LocalDirectoryNameNoSlashes
    global Camera_SavedImages_FilenamePrefix
    global ArucoTag_SavedImages_LocalDirectoryNameNoSlashes
    global ArucoTag_SavedImages_FilenamePrefix

    LoadAndParseJSONfile_SavingSettings()
    #################################################

    #################################################
    global MyPlotterPureTkinterStandAloneProcess_Directions
    global MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_GUIparametersDict
    global MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_setup_dict
    global MyPlotterPureTkinterStandAloneProcess_RefreshDurationInSeconds

    LoadAndParseJSONfile_MyPlotterPureTkinterStandAloneProcess()
    #################################################

    #################################################
    #################################################

    #################################################
    #################################################
    global root

    global TabControlObject
    global Tab_MainControls
    global Tab_ArucoTagDetection
    global Tab_MyPrint

    global CurrentTime_MainLoopThread
    CurrentTime_MainLoopThread = -11111.0

    global StartingTime_MainLoopThread
    StartingTime_MainLoopThread = -11111.0

    global ArucoTag_TranslationVectorOfMarkerCenter_PythonList_PrimaryMarker
    ArucoTag_TranslationVectorOfMarkerCenter_PythonList_PrimaryMarker = [-11111.0]*3

    global ArucoTag_RotationVectorOfMarkerCenter_EulerAnglesXYZrollPitchYawInDegrees_PythonList_PrimaryMarker
    ArucoTag_RotationVectorOfMarkerCenter_EulerAnglesXYZrollPitchYawInDegrees_PythonList_PrimaryMarker = [-11111.0] * 3

    global ArucoTag_RotationVectorOfMarkerCenter_EulerAnglesXYZrollPitchYawInRadians_PythonList_PrimaryMarker
    ArucoTag_RotationVectorOfMarkerCenter_EulerAnglesXYZrollPitchYawInRadians_PythonList_PrimaryMarker = [-11111.0] * 3

    global ArucoTag_DetectionTimeInMilliseconds_PrimaryMarker
    ArucoTag_DetectionTimeInMilliseconds_PrimaryMarker = -11111.0

    global ArucoTag_TranslationVectorOfMarkerCenter_PythonList_SecondaryMarker
    ArucoTag_TranslationVectorOfMarkerCenter_PythonList_SecondaryMarker = [-11111.0] * 3

    global ArucoTag_RotationVectorOfMarkerCenter_EulerAnglesXYZrollPitchYawInDegrees_PythonList_SecondaryMarker
    ArucoTag_RotationVectorOfMarkerCenter_EulerAnglesXYZrollPitchYawInDegrees_PythonList_SecondaryMarker = [-11111.0] * 3

    global ArucoTag_RotationVectorOfMarkerCenter_EulerAnglesXYZrollPitchYawInRadians_PythonList_SecondaryMarker
    ArucoTag_RotationVectorOfMarkerCenter_EulerAnglesXYZrollPitchYawInRadians_PythonList_SecondaryMarker = [-11111.0] * 3

    global ArucoTag_DetectionTimeInMilliseconds_SecondaryMarker
    ArucoTag_DetectionTimeInMilliseconds_SecondaryMarker = -11111.0

    global LineFromPrimaryMarkerToSecondaryMarker_NumpyArray
    LineFromPrimaryMarkerToSecondaryMarker_NumpyArray = numpy.array([-11111.0]*3)

    global LineFromPrimaryMarkerToSecondaryMarker_DistanceMM
    LineFromPrimaryMarkerToSecondaryMarker_DistanceMM = -11111.0

    global LineFromPrimaryMarkerToSecondaryMarker_AngleWRTground
    LineFromPrimaryMarkerToSecondaryMarker_AngleWRTground = -11111.0

    CircleCenterX = -11111
    CircleCenterY = -11111
    #################################################
    #################################################

    #################################################
    #################################################
    global ArucoTagDetectionFromCameraFeed_ReubenPython3ClassObject

    global ArucoTag_OPEN_FLAG
    ArucoTag_OPEN_FLAG = -1

    global ArucoTag_MostRecentDict
    ArucoTag_MostRecentDict = dict()

    global ArucoTag_MostRecentDict_DataStreamingFrequency_CalculatedFromMainThread
    ArucoTag_MostRecentDict_DataStreamingFrequency_CalculatedFromMainThread = -11111.0

    global ArucoTag_MostRecentDict_Time
    ArucoTag_MostRecentDict_Time = -11111.0

    global ArucoTag_MostRecentDict_DetectedArucoTag_InfoDict
    ArucoTag_MostRecentDict_DetectedArucoTag_InfoDict = dict()
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
    global MyPrint_ReubenPython2and3ClassObject

    global MyPrint_OPEN_FLAG
    MyPrint_OPEN_FLAG = -1
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
        StartingTime_CalculatedFromGUIthread = getPreciseSecondsTimeStampString()
        print("Starting GUI thread...")

        global GUI_Thread_ThreadingObject
        GUI_Thread_ThreadingObject = threading.Thread(target=GUI_Thread)
        GUI_Thread_ThreadingObject.setDaemon(True)  # Should mean that the GUI thread is destroyed automatically when the main thread is destroyed.
        GUI_Thread_ThreadingObject.start()
        time.sleep(0.5)  # Allow enough time for 'root' to be created that we can then pass it into other classes.
    else:
        root = None
        Tab_MainControls = None
        Tab_ArucoTagDetection = None
        Tab_MyPrint = None
    #################################################
    #################################################

    ################################################
    ################################################
    global CameraStreamerClass_ReubenPython2and3ClassObject_setup_dict
    CameraStreamerClass_ReubenPython2and3ClassObject_setup_dict = dict([("MainThread_TimeToSleepEachLoop", 0.030),
                                                                        ("NameToDisplay_UserSet", "Camera"),
                                                                        ("TkinterPreviewImageScalingFactor", camera_TkinterPreviewImageScalingFactor),
                                                                        ("camera_selection_number", camera_selection_number),
                                                                        ("CameraCaptureThread_TimeToSleepEachLoop", CameraCaptureThread_TimeToSleepEachLoop),
                                                                        ("CameraEncodeThread_TimeToSleepEachLoop", CameraEncodeThread_TimeToSleepEachLoop),
                                                                        ("ImageSavingThread_TimeToSleepEachLoop", ImageSavingThread_TimeToSleepEachLoop),
                                                                        ("camera_frame_rate", camera_frame_rate),
                                                                        ("image_width", image_width),
                                                                        ("image_height", image_height),
                                                                        ("image_jpg_encoding_quality", image_jpg_encoding_quality),
                                                                        ("CameraSetting_Autofocus", CameraSetting_Autofocus),
                                                                        ("CameraSetting_Autoexposure", CameraSetting_Autoexposure),
                                                                        ("CameraSetting_exposure", CameraSetting_exposure),
                                                                        ("CameraSetting_gain", CameraSetting_gain),
                                                                        ("CameraSetting_brightness", CameraSetting_brightness),
                                                                        ("CameraSetting_contrast", CameraSetting_contrast),
                                                                        ("CameraSetting_saturation", CameraSetting_saturation),
                                                                        ("CameraSetting_hue", CameraSetting_hue),
                                                                        ("DrawCircleAtImageCenterFlag", DrawCircleAtImageCenterFlag),
                                                                        ("EnableCameraEncodeThreadFlag", EnableCameraEncodeThreadFlag),
                                                                        ("EnableImageSavingThreadFlag", EnableImageSavingThreadFlag),
                                                                        ("RemoveFisheyeDistortionFromImage_Flag", RemoveFisheyeDistortionFromImage_Flag),
                                                                        ("CameraCalibrationParametersDict", CameraCalibrationParametersDict),
                                                                        ("OpenCVbackendToUseEnglishName", OpenCVbackendToUseEnglishName),
                                                                        ("Camera_SavedImages_LocalDirectoryNameNoSlashes", Camera_SavedImages_LocalDirectoryNameNoSlashes),
                                                                        ("Camera_SavedImages_FilenamePrefix", Camera_SavedImages_FilenamePrefix)])

    global ArucoTagDetectionFromCameraFeed_ReubenPython3Class_GUIparametersDict
    ArucoTagDetectionFromCameraFeed_ReubenPython3Class_GUIparametersDict = dict([("USE_GUI_FLAG", 1),
                                    ("root", Tab_ArucoTagDetection),
                                    ("EnableInternal_MyPrint_Flag", 0),
                                    ("NumberOfPrintLines", 10),
                                    ("UseBorderAroundThisGuiObjectFlag", 0),
                                    ("GUI_ROW", GUI_ROW_ArucoTagDetection),
                                    ("GUI_COLUMN", GUI_COLUMN_ArucoTagDetection),
                                    ("GUI_PADX", GUI_PADX_ArucoTagDetection),
                                    ("GUI_PADY", GUI_PADY_ArucoTagDetection),
                                    ("GUI_ROWSPAN", GUI_ROWSPAN_ArucoTagDetection),
                                    ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_ArucoTagDetection)])

    global ArucoTagDetectionFromCameraFeed_ReubenPython3Class_setup_dict
    ArucoTagDetectionFromCameraFeed_ReubenPython3Class_setup_dict = dict([("GUIparametersDict", ArucoTagDetectionFromCameraFeed_ReubenPython3Class_GUIparametersDict),
                                                                ("CameraStreamerClass_ReubenPython2and3ClassObject_setup_dict", CameraStreamerClass_ReubenPython2and3ClassObject_setup_dict),
                                                                ("NameToDisplay_UserSet", "ArucoTagDetectionFromCameraFeed"),
                                                                ("ShowOpenCVwindowsFlag", ShowOpenCVwindowsFlag),
                                                                ("OpenCVwindowPosX", OpenCVwindowPosX),
                                                                ("OpenCVwindowPosY", OpenCVwindowPosY),
                                                                ("OpenCVwindow_UpdateEveryNmilliseconds", OpenCVwindow_UpdateEveryNmilliseconds),
                                                                ("MainThread_TimeToSleepEachLoop", test_program_for_ArucoTagDetectionFromCameraFeed_ReubenPython3Class_MainThread_TimeToSleepEachLoop),
                                                                ("ArucoTag_DictType_EnglishString", ArucoTag_DictType_EnglishString),
                                                                ("ArucoTag_MarkerLengthInMillimeters", ArucoTag_MarkerLengthInMillimeters),
                                                                ("ArucoTag_AxesToDrawLengthInMillimeters", ArucoTag_AxesToDrawLengthInMillimeters),
                                                                ("ArucoTag_TranslationVectorOfMarkerCenter_ExponentialSmoothingFilterLambda", ArucoTag_TranslationVectorOfMarkerCenter_ExponentialSmoothingFilterLambda),
                                                                ("ArucoTag_RotationVectorOfMarkerCenter_ExponentialSmoothingFilterLambda", ArucoTag_RotationVectorOfMarkerCenter_ExponentialSmoothingFilterLambda),
                                                                ("TkinterPreviewImageScalingFactor", ArucoTag_TkinterPreviewImageScalingFactor),
                                                                ("ArucoTag_SavedImages_LocalDirectoryNameNoSlashes", ArucoTag_SavedImages_LocalDirectoryNameNoSlashes),
                                                                ("ArucoTag_SavedImages_FilenamePrefix", ArucoTag_SavedImages_FilenamePrefix),
                                                                ("ArucoTag_DetectInvertedMarkersAsWellAsNormalOnesFlag", ArucoTag_DetectInvertedMarkersAsWellAsNormalOnesFlag)])


    ###@@@
    CameraStreamerClass_ReubenPython2and3ClassObject_setup_dict["camera_selection_number"] = int(camera_selection_number)
    ArucoTagDetectionFromCameraFeed_ReubenPython3Class_setup_dict["CameraStreamerClass_ReubenPython2and3ClassObject_setup_dict"] = CameraStreamerClass_ReubenPython2and3ClassObject_setup_dict
    ###@@@

    if USE_ArucoTag_FLAG == 1:
        try:
            ArucoTagDetectionFromCameraFeed_ReubenPython3ClassObject = ArucoTagDetectionFromCameraFeed_ReubenPython3Class(ArucoTagDetectionFromCameraFeed_ReubenPython3Class_setup_dict)
            ArucoTag_OPEN_FLAG = ArucoTagDetectionFromCameraFeed_ReubenPython3ClassObject.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("ArucoTagDetectionFromCameraFeed_ReubenPython3ClassObject __init__: Exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    global CSVdataLogger_ReubenPython3ClassObject_GUIparametersDict
    CSVdataLogger_ReubenPython3ClassObject_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_CSVdataLogger_FLAG),
                                    ("root", Tab_MainControls),
                                    ("EnableInternal_MyPrint_Flag", 1),
                                    ("NumberOfPrintLines", 10),
                                    ("UseBorderAroundThisGuiObjectFlag", 0),
                                    ("GUI_ROW", GUI_ROW_CSVdataLogger),
                                    ("GUI_COLUMN", GUI_COLUMN_CSVdataLogger),
                                    ("GUI_PADX", GUI_PADX_CSVdataLogger),
                                    ("GUI_PADY", GUI_PADY_CSVdataLogger),
                                    ("GUI_ROWSPAN", GUI_ROWSPAN_CSVdataLogger),
                                    ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_CSVdataLogger)])

    global CSVdataLogger_ReubenPython3ClassObject_setup_dict
    CSVdataLogger_ReubenPython3ClassObject_setup_dict = dict([("GUIparametersDict", CSVdataLogger_ReubenPython3ClassObject_GUIparametersDict),
                                                                                ("NameToDisplay_UserSet", "CSVdataLogger"),
                                                                                ("CSVfile_DirectoryPath", "G:\\My Drive\\CodeReuben\\ArucoTagDetectionFromCameraFeed_ReubenPython3Class\\SavedCSVfiles"),
                                                                                ("FileNamePrefix", "Aruco_"),
                                                                                ("VariableNamesForHeaderList", ["Time",
                                                                                                                "X0",
                                                                                                                "Y0",
                                                                                                                "Z0",
                                                                                                                "X1",
                                                                                                                "Y1",
                                                                                                                "Z1",
                                                                                                                "LineFromPrimaryMarkerToSecondaryMarker_DistanceMM",
                                                                                                                "LineFromPrimaryMarkerToSecondaryMarker_AngleWRTground"]),
                                                                                ("MainThread_TimeToSleepEachLoop", 0.002),
                                                                                ("SaveOnStartupFlag", 0)])

    if USE_CSVdataLogger_FLAG == 1:
        try:
            CSVdataLogger_ReubenPython3ClassObject = CSVdataLogger_ReubenPython3Class(CSVdataLogger_ReubenPython3ClassObject_setup_dict)
            CSVdataLogger_OPEN_FLAG = CSVdataLogger_ReubenPython3ClassObject.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("CSVdataLogger_ReubenPython3ClassObject __init__: Exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_MyPrint_FLAG == 1:

        MyPrint_ReubenPython2and3ClassObject_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_MyPrint_FLAG),
                                                                        ("root", Tab_MyPrint),
                                                                        ("UseBorderAroundThisGuiObjectFlag", 0),
                                                                        ("GUI_ROW", GUI_ROW_MyPrint),
                                                                        ("GUI_COLUMN", GUI_COLUMN_MyPrint),
                                                                        ("GUI_PADX", GUI_PADX_MyPrint),
                                                                        ("GUI_PADY", GUI_PADY_MyPrint),
                                                                        ("GUI_ROWSPAN", GUI_ROWSPAN_MyPrint),
                                                                        ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_MyPrint)])

        MyPrint_ReubenPython2and3ClassObject_setup_dict = dict([("NumberOfPrintLines", 10),
                                                                ("WidthOfPrintingLabel", 200),
                                                                ("PrintToConsoleFlag", 1),
                                                                ("LogFileNameFullPath", os.getcwd() + "//TestLog.txt"),
                                                                ("GUIparametersDict", MyPrint_ReubenPython2and3ClassObject_GUIparametersDict)])

        try:
            MyPrint_ReubenPython2and3ClassObject = MyPrint_ReubenPython2and3Class(MyPrint_ReubenPython2and3ClassObject_setup_dict)
            time.sleep(0.25)
            MyPrint_OPEN_FLAG = MyPrint_ReubenPython2and3ClassObject.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("MyPrint_ReubenPython2and3ClassObject __init__: Exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    global MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_GUIparametersDict
    MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_GUIparametersDict = dict([("EnableInternal_MyPrint_Flag", 1),
                                                                                                ("NumberOfPrintLines", 10),
                                                                                                ("UseBorderAroundThisGuiObjectFlag", 0),
                                                                                                ("GraphCanvasWidth", 890),
                                                                                                ("GraphCanvasHeight", 700),
                                                                                                ("GraphCanvasWindowStartingX", 0),
                                                                                                ("GraphCanvasWindowStartingY", 0),
                                                                                                ("GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents", 20)])

    global MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_setup_dict
    MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_setup_dict = dict([("GUIparametersDict", MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_GUIparametersDict),
                                                                                        ("ParentPID", os.getpid()),
                                                                                        ("WatchdogTimerExpirationDurationSeconds_StandAlonePlottingProcess", 5.0),
                                                                                        ("MarkerSize", 3),
                                                                                        ("CurvesToPlotNamesAndColorsDictOfLists", dict([("NameList", ["Channel0", "Channel1", "Channel2"]),("ColorList", ["Red", "Green", "Blue"])])),
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

    if USE_MyPlotterPureTkinterStandAloneProcess_FLAG == 1:
        try:
            MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class(MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_setup_dict)
            MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject, exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    ####################################################
    ####################################################
    try:

        DictOfVariableFilterSettings = dict([("CircleCenterX", dict([("UseMedianFilterFlag", 1), ("UseExponentialSmoothingFilterFlag", 1),("ExponentialSmoothingFilterLambda", ArucoTag_CircleDetection_ExponentialSmoothingFilterLambda)])), #new_filtered_value = k * raw_sensor_value + (1 - k) * old_filtered_value
                                             ("CircleCenterY", dict([("UseMedianFilterFlag", 1), ("UseExponentialSmoothingFilterFlag", 1),("ExponentialSmoothingFilterLambda", ArucoTag_CircleDetection_ExponentialSmoothingFilterLambda)])),
                                             ("CircleRadius",  dict([("UseMedianFilterFlag", 1), ("UseExponentialSmoothingFilterFlag", 1),("ExponentialSmoothingFilterLambda", ArucoTag_CircleDetection_ExponentialSmoothingFilterLambda)]))])

        #LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject_setup_dict = dict([("DictOfVariableFilterSettings", DictOfVariableFilterSettings)])
        LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject_setup_dict = dict()

        LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject = LowPassFilterForDictsOfLists_ReubenPython2and3Class(LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject_setup_dict)
        LOWPASSFILTER_OPEN_FLAG = LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject.OBJECT_CREATED_SUCCESSFULLY_FLAG

        LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject.AddDictOfVariableFilterSettingsFromExternalProgram(DictOfVariableFilterSettings)

    except:
        exceptions = sys.exc_info()[0]
        print("LowPassFilterForDictsOfLists_ReubenPython2and3Class __init__: Exceptions: %s" % exceptions)
####################################################
    ####################################################

    #################################################
    #################################################
    if USE_ArucoTag_FLAG == 1 and ArucoTag_OPEN_FLAG != 1:
        print("Failed to open ArucoTagDetectionFromCameraFeed_ReubenPython3Class.")
        ExitProgram_Callback()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_CSVdataLogger_FLAG == 1 and CSVdataLogger_OPEN_FLAG != 1:
        print("Failed to open CSVdataLogger_ReubenPython3Class.")
        ExitProgram_Callback()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_MyPrint_FLAG == 1 and MyPrint_OPEN_FLAG != 1:
        print("Failed to open MyPrint_ReubenPython2and3ClassObject.")
        ExitProgram_Callback()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_MyPlotterPureTkinterStandAloneProcess_FLAG == 1 and MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG != 1:
        print("Failed to open MyPlotterPureTkinterClass_Object.")
        ExitProgram_Callback()
    #################################################
    #################################################

    #################################################
    #################################################
    #################################################
    #################################################
    print("Starting main loop 'test_program_for_ArucoTagDetectionFromCameraFeed_ReubenPython3Class.py.")
    StartingTime_MainLoopThread = getPreciseSecondsTimeStampString()

    while(EXIT_PROGRAM_FLAG == 0):

        #################################################
        #################################################
        #################################################
        CurrentTime_MainLoopThread = getPreciseSecondsTimeStampString() - StartingTime_MainLoopThread
        #################################################
        #################################################
        #################################################

        ################################################### GET's
        ###################################################
        if JSONfiles_NeedsToBeLoadedFlag == 1:
            LoadAndParseJSONfile_GUIsettings()

            ###################################################
            LoadAndParseJSONfile_ArucoTagParameters()

            DictOfVariableFilterSettings = dict([("CircleCenterX", dict([("UseMedianFilterFlag", 1), ("UseExponentialSmoothingFilterFlag", 1),("ExponentialSmoothingFilterLambda", ArucoTag_CircleDetection_ExponentialSmoothingFilterLambda)])), #new_filtered_value = k * raw_sensor_value + (1 - k) * old_filtered_value
                                     ("CircleCenterY", dict([("UseMedianFilterFlag", 1), ("UseExponentialSmoothingFilterFlag", 1),("ExponentialSmoothingFilterLambda", ArucoTag_CircleDetection_ExponentialSmoothingFilterLambda)])),
                                     ("CircleRadius",  dict([("UseMedianFilterFlag", 1), ("UseExponentialSmoothingFilterFlag", 1),("ExponentialSmoothingFilterLambda", ArucoTag_CircleDetection_ExponentialSmoothingFilterLambda)]))])

            print(ArucoTag_CircleDetection_ExponentialSmoothingFilterLambda)
            LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject.AddDictOfVariableFilterSettingsFromExternalProgram(DictOfVariableFilterSettings)
            ###################################################

            '''
            UPDATE PARAMETERS HERE UPON RELOADING JSON FILE
            '''

            print("LoadAndParseJSONfile_ArucoTagParameters loaded!")

            JSONfiles_NeedsToBeLoadedFlag = 0
        ###################################################
        ###################################################

        #################################################
        #################################################
        #################################################
        if USE_ArucoTag_FLAG == 1:

            ################################################# GET's
            #################################################
            ArucoTag_MostRecentDict = ArucoTagDetectionFromCameraFeed_ReubenPython3ClassObject.GetMostRecentDataDict()
            #print("ArucoTag_MostRecentDict: " + str(ArucoTag_MostRecentDict))

            if "Time" in ArucoTag_MostRecentDict:

                #################################################
                ArucoTag_MostRecentDict_DataStreamingFrequency_CalculatedFromMainThread = ArucoTag_MostRecentDict["Frequency"]
                ArucoTag_MostRecentDict_Time = ArucoTag_MostRecentDict["Time"]
                ArucoTag_MostRecentDict_DetectedArucoTag_InfoDict = ArucoTag_MostRecentDict["DetectedArucoTag_InfoDict"]
                ArucoTag_MostRecentDict_OriginalImage = ArucoTag_MostRecentDict["OriginalImage"]
                ArucoTag_MostRecentDict_CameraImage_Color_ArucoDetected = ArucoTag_MostRecentDict["CameraImage_Color_ArucoDetected"]

                ArucoTag_MostRecentDict_CameraCalibration_Kmatrix_CameraIntrinsicsMatrix = ArucoTag_MostRecentDict["CameraCalibration_Kmatrix_CameraIntrinsicsMatrix"]
                ArucoTag_MostRecentDict_CameraCalibration_Darray_DistortionCoefficients = ArucoTag_MostRecentDict["CameraCalibration_Darray_DistortionCoefficients"]

                [Height, Width, NumberOfChannels] = GetImageSizeAsHeightWidthNumberOfChannelsList(ArucoTag_MostRecentDict_CameraImage_Color_ArucoDetected)
                #################################################

                #################################################
                MarkerCentersInEuclideanSpaceList = list()
                MarkersRotationVectorOfMarkerCenter_RodriguesAxisAngleList = list()
                MarkerDetectionTimeInMillisecondsList = list()
                MarkerCornersList = list()
                CenterOfMarkersInImageCoordinatesList = list()
                for Index in ArucoTag_MostRecentDict_DetectedArucoTag_InfoDict:
                    InfoDict = ArucoTag_MostRecentDict_DetectedArucoTag_InfoDict[Index]

                    ArucoTag_DetectedArucoTags_CornersList = InfoDict["ArucoTag_DetectedArucoTags_CornersList_ImageCoordinates"]
                    FirstCorner = ArucoTag_DetectedArucoTags_CornersList[0][0]
                    CenterOfMarker = InfoDict["ArucoTag_DetectedArucoTags_CenterOfMarker_ImageCoordinates"]

                    if ArucoTag_MostRecentDict_Time - InfoDict["ArucoTag_DetectionTimeInMilliseconds"] < 0.04 :
                        MarkerCentersInEuclideanSpaceList.append(InfoDict["ArucoTag_TranslationVectorOfMarkerCenter_PythonList"])
                        MarkersRotationVectorOfMarkerCenter_RodriguesAxisAngleList.append(InfoDict["ArucoTag_RotationVectorOfMarkerCenter_RodriguesAxisAngle_PythonList"])
                        MarkerDetectionTimeInMillisecondsList.append(InfoDict["ArucoTag_DetectionTimeInMilliseconds"])
                        CenterOfMarkersInImageCoordinatesList.append(numpy.array([CenterOfMarker[0], CenterOfMarker[1], 0.0]))
                        MarkerCornersList.append(ArucoTag_DetectedArucoTags_CornersList)

                        #Plot middle of marker
                        #cv2.circle(ArucoTag_MostRecentDict_CameraImage_Color_ArucoDetected, (round(CenterOfMarker[0]), round(CenterOfMarker[1])), radius=10, color=(255, 0, 0), thickness=-1) #thickness=-1 means it's filled-in

                #################################################

                #print("CenterOfMarkersInImageCoordinatesList: " + str(CenterOfMarkersInImageCoordinatesList))

                MarkerCentersInEuclideanSpaceList_NumpyMean = numpy.mean(MarkerCentersInEuclideanSpaceList, 0).tolist()
                #print("MarkerCentersInEuclideanSpaceList_NumpyMean: " + str(MarkerCentersInEuclideanSpaceList_NumpyMean))

                RodriguesAxisAngle_NumpyMean = numpy.mean(MarkersRotationVectorOfMarkerCenter_RodriguesAxisAngleList, 0).tolist()
                #print("RodriguesAxisAngle_NumpyMean: " + str(RodriguesAxisAngle_NumpyMean))

                CenterOfMarkersInImageCoordinatesList_NumpyMean = numpy.mean(CenterOfMarkersInImageCoordinatesList, 0).tolist()
                #print("CenterOfMarkersInImageCoordinatesList_NumpyMean: " + str(CenterOfMarkersInImageCoordinatesList_NumpyMean))

                if len(CenterOfMarkersInImageCoordinatesList) >= 3:
                    #################################################
                    #circle_3d = Circle3D(numpy.array(MarkerCentersInEuclideanSpaceList)) #If using Euclidean space
                    circle_3d = Circle3D(numpy.array(CenterOfMarkersInImageCoordinatesList))


                    #CircleCenterZ = round(circle_3d.center[2])
                    #CircleRadius = round(circle_3d.radius)

                    #print("(circle_3d: " + str(circle_3d.center) + ", Radius = " + str(circle_3d.radius))
                    CircleCenterX_raw = round(circle_3d.center[0])
                    CircleCenterY_raw = round(circle_3d.center[1])
                    CircleRadius_raw = round(circle_3d.radius)
                    LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject_MostRecentDict = LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject.AddDataDictFromExternalProgram(dict([("CircleCenterX", CircleCenterX_raw),
                                                                                                                            ("CircleCenterY", CircleCenterY_raw),
                                                                                                                            ("CircleRadius", CircleRadius_raw)]))
                    #Raw_1 = LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject_MostRecentDict["desired_angle_deg_1"]["Raw_MostRecentValuesList"]
                    CircleCenterX = round(LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject_MostRecentDict["CircleCenterX"]["Filtered_MostRecentValuesList"][0])
                    CircleCenterY = round(LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject_MostRecentDict["CircleCenterY"]["Filtered_MostRecentValuesList"][0])
                    CircleRadius = round(LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject_MostRecentDict["CircleRadius"]["Filtered_MostRecentValuesList"][0])
                    #################################################


                    #################################################


                    TransformedPoints, jacobian = cv2.projectPoints(objectPoints=numpy.array([circle_3d.center]), \
                                        tvec=numpy.array([0.0, 0.0, 0.0]), \
                                        rvec=numpy.array([0.0, 0.0, 0.0]), \
                                        cameraMatrix=ArucoTag_MostRecentDict_CameraCalibration_Kmatrix_CameraIntrinsicsMatrix, \
                                        distCoeffs=ArucoTag_MostRecentDict_CameraCalibration_Darray_DistortionCoefficients)

                    #CircleCenterX = round(TransformedPoints[0][0][0])
                    #CircleCenterY = round(TransformedPoints[0][0][1])



                    #CircleCenterX = round(Width/2.0)
                    #CircleCenterY = round(Height/2.0)
                    #CircleRadius = round(Height/2.0)

                    #print("TransformedPoints: " + str(TransformedPoints[0][0]))
                if CircleCenterX != -11111:
                    overlay = ArucoTag_MostRecentDict_CameraImage_Color_ArucoDetected.copy()
                    cv2.circle(overlay, (CircleCenterX, CircleCenterY), radius=CircleRadius, color=(0, 0, 255), thickness=-1) #thickness=-1 means it's filled-in

                    alpha = 0.4  # Transparency factor.

                    # Following line overlays transparent rectangle
                    # over the image
                    image_new = cv2.addWeighted(overlay, alpha, ArucoTag_MostRecentDict_CameraImage_Color_ArucoDetected, 1 - alpha, 0)
                    cv2.circle(image_new, (CircleCenterX, CircleCenterY), radius=round(CircleRadius*0.1), color=(0, 0, 255), thickness=-1) #thickness=-1 means it's filled-in

                    #################################################

                #################################################
                    cv2.imshow('ArucoTag_MostRecentDict_CameraImage_Color_ArucoDetected', image_new)
                    cv2.waitKey(1)

                #################################################



            #################################################
            #################################################

            ################################################# SET's
            #################################################

            #################################################
            #################################################

            ################################################# SET's
            #################################################
            if CSVdataLogger_OPEN_FLAG == 1:

                if ArucoTag_MarkerIDToDetect_PrimaryMarker in ArucoTag_MostRecentDict_DetectedArucoTag_InfoDict and ArucoTag_MarkerIDToDetect_SecondaryMarker in ArucoTag_MostRecentDict_DetectedArucoTag_InfoDict:
                    if 1:
                        CSVdataLogger_ReubenPython3ClassObject.AddDataToCSVfile_ExternalFunctionCall([ArucoTag_MostRecentDict_Time])

            #################################################
            #################################################

            #################################################
            #################################################
            if MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG == 1:

                #################################################
                MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject.GetMostRecentDataDict()

                if "StandAlonePlottingProcess_ReadyForWritingFlag" in MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict:
                    MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict["StandAlonePlottingProcess_ReadyForWritingFlag"]

                    if MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag == 1:
                        if CurrentTime_MainLoopThread - LastTime_MainLoopThread_MyPlotterPureTkinterStandAloneProcess >= MyPlotterPureTkinterStandAloneProcess_RefreshDurationInSeconds:

                            if ArucoTag_MarkerIDToDetect_PrimaryMarker in ArucoTag_MostRecentDict_DetectedArucoTag_InfoDict and ArucoTag_MarkerIDToDetect_SecondaryMarker in ArucoTag_MostRecentDict_DetectedArucoTag_InfoDict:
                                if 1:#(LineFromPrimaryMarkerToSecondaryMarker_DistanceMM < ArucoTag_DistanceBetweenPrimaryMarkerAndSecondaryMarker + ArucoTag_DistanceBetweenPrimaryMarkerAndSecondaryMarker_ClosenessThreshold) and (LineFromPrimaryMarkerToSecondaryMarker_DistanceMM > ArucoTag_DistanceBetweenPrimaryMarkerAndSecondaryMarker - ArucoTag_DistanceBetweenPrimaryMarkerAndSecondaryMarker_ClosenessThreshold):

                                    #MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject.ExternalAddPointOrListOfPointsToPlot(["Channel0", "Channel1"], [CurrentTime_MainLoopThread]*2, ArucoTag_TranslationVectorOfMarkerCenter_PythonList_PrimaryMarker[0:2])
                                    MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject.ExternalAddPointOrListOfPointsToPlot(["Channel0", "Channel1"], [CurrentTime_MainLoopThread]*2, [LineFromPrimaryMarkerToSecondaryMarker_DistanceMM, LineFromPrimaryMarkerToSecondaryMarker_AngleWRTground])


                                    LastTime_MainLoopThread_MyPlotterPureTkinterStandAloneProcess = CurrentTime_MainLoopThread
                #################################################

            ####################################################
            ####################################################

        #################################################
        #################################################
        #################################################

        time.sleep(0.030)
    #################################################
    #################################################
    #################################################
    #################################################

    ################################################# THIS IS THE EXIT ROUTINE!
    #################################################
    #################################################
    #################################################
    print("Exiting main program 'test_program_for_ArucoTagDetectionFromCameraFeed_ReubenPython3Class.py.")

    #################################################
    cv2.destroyAllWindows()
    #################################################

    #################################################
    if ArucoTag_OPEN_FLAG == 1:
        ArucoTagDetectionFromCameraFeed_ReubenPython3ClassObject.ExitProgram_Callback()
    #################################################

    #################################################
    if CSVdataLogger_OPEN_FLAG == 1:
        CSVdataLogger_ReubenPython3ClassObject.ExitProgram_Callback()
    #################################################

    #################################################
    if MyPrint_OPEN_FLAG == 1:
        MyPrint_ReubenPython2and3ClassObject.ExitProgram_Callback()
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