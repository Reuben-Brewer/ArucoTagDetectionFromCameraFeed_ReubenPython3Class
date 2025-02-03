# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision I, 02/02/2025

Verified working on: Python 3.12 for Windows 11 64-bit and Raspberry Pi Bullseye (Backend = "CAP_ANY", Camera = ELP USB).
'''

__author__ = 'reuben.brewer'

#########################################################
from CameraStreamerClass_ReubenPython2and3Class import *
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
import numpy
import argparse
import json
import keyboard
#########################################################

#########################################################
if sys.version_info[0] < 3:
    from Tkinter import * #Python 2
    import tkFont
    import ttk
else:
    from tkinter import * #Python 3
    import tkinter.font as tkFont #Python 3
    from tkinter import ttk
#########################################################

#########################################################
import platform
if platform.system() == "Windows":
    import ctypes
    winmm = ctypes.WinDLL('winmm')
    winmm.timeBeginPeriod(1) #Set minimum timer resolution to 1ms so that time.sleep(0.001) behaves properly.
#########################################################

#########################################################
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
#########################################################

#######################################################################################################################
#######################################################################################################################
global ParametersToBeLoaded_Directory_Windows
ParametersToBeLoaded_Directory_Windows = os.getcwd().replace("\\", "//") + "//ParametersToBeLoaded"

global ParametersToBeLoaded_Directory_LinuxNonRaspberryPi
ParametersToBeLoaded_Directory_LinuxNonRaspberryPi = os.getcwd().replace("\\", "//") + "//ParametersToBeLoaded"

global ParametersToBeLoaded_Directory_LinuxRaspberryPi
ParametersToBeLoaded_Directory_LinuxRaspberryPi = "//home//pinis//Desktop//CameraStreamerClass_ReubenPython2and3Class_PythonDeploymentFiles//ParametersToBeLoaded"

global ParametersToBeLoaded_Directory_Mac
ParametersToBeLoaded_Directory_Mac = os.getcwd().replace("\\", "//") + "//ParametersToBeLoaded"
#######################################################################################################################
#######################################################################################################################

##########################################################################################################
##########################################################################################################
def getPreciseSecondsTimeStampString():
    ts = time.time()

    return ts
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def LoadAndParseJSONfile_CameraStreamerClass():
    global ParametersToBeLoaded_CameraStreamerClass_Dict

    print("Calling LoadAndParseJSONfile_CameraStreamerClass().")

    #################################
    JSONfilepathFull_CameraStreamerClass = ParametersToBeLoaded_Directory_TO_BE_USED + "//ParametersToBeLoaded_CameraStreamerClass.json"

    #def LoadAndParseJSONfile_AddDictKeysToGlobalsDict(GlobalsDict, JSONfilepathFull, USE_PassThrough0and1values_ExitProgramOtherwise_FORS = 0, PrintResultsFlag = 0):
    ParametersToBeLoaded_CameraStreamerClass_Dict = LoadAndParseJSONfile_AddDictKeysToGlobalsDict(globals(), JSONfilepathFull_CameraStreamerClass, 1, 1)
    #################################

    return ParametersToBeLoaded_CameraStreamerClass_Dict

##########################################################################################################
##########################################################################################################

#######################################################################################################################
#######################################################################################################################
def LoadAndParseJSONfile_AddDictKeysToGlobalsDict(GlobalsDict, JSONfilepathFull, USE_PassThrough0and1values_ExitProgramOtherwise_FOR_FLAGS = 0, PrintResultsFlag = 0, PauseForInputOnException = 1):

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
        print("LoadAndParseJSONfile_AddDictKeysToGlobalsDict failed for " + JSONfilepathFull + ", Current Key = " + key + ", exceptions: %s" % exceptions)
        traceback.print_exc()

        if PauseForInputOnException == 1:
            input("Please press any key to continue")

        return dict()
        #################################

#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def TellWhichFileWereIn():
    # We used to use this method, but it gave us the root calling file, not the class calling file
    # absolute_file_path = os.path.dirname(os.path.realpath(sys.argv[0]))
    # filename = absolute_file_path[absolute_file_path.rfind("\\") + 1:]

    frame = inspect.stack()[1]
    filename = frame[1][frame[1].rfind("\\") + 1:]
    filename = filename.replace(".py", "")

    return filename
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
def PassThrough0and1values_ExitProgramOtherwise(InputNameString, InputNumber, ExitProgramIfFailureFlag = 0):

    #######################################################################################################################
    #######################################################################################################################
    try:

        #######################################################################################################################
        InputNumber_ConvertedToFloat = float(InputNumber)
        #######################################################################################################################

    except:

        #######################################################################################################################
        exceptions = sys.exc_info()[0]
        print(TellWhichFileWereIn() + ", PassThrough0and1values_ExitProgramOtherwise Error. InputNumber '" + InputNameString + "' must be a numerical value, Exceptions: %s" % exceptions)

        ##########################
        if ExitProgramIfFailureFlag == 1:
            sys.exit()
        else:
            return -1
        ##########################

        #######################################################################################################################

    #######################################################################################################################
    #######################################################################################################################

    #######################################################################################################################
    #######################################################################################################################
    try:

        #######################################################################################################################
        if InputNumber_ConvertedToFloat == 0.0 or InputNumber_ConvertedToFloat == 1.0:
            return InputNumber_ConvertedToFloat

        else:

            print(TellWhichFileWereIn() + ", PassThrough0and1values_ExitProgramOtherwise Error. '" +
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

        #######################################################################################################################

    except:

        #######################################################################################################################
        exceptions = sys.exc_info()[0]
        print(TellWhichFileWereIn() + ", PassThrough0and1values_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)

        ##########################
        if ExitProgramIfFailureFlag == 1:
            sys.exit()
        else:
            return -1
        ##########################

        #######################################################################################################################

    #######################################################################################################################
    #######################################################################################################################

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
def PassThroughFloatValuesInRange_ExitProgramOtherwise(InputNameString, InputNumber, RangeMinValue, RangeMaxValue, ExitProgramIfFailureFlag = 0):

    #######################################################################################################################
    #######################################################################################################################
    try:
        #######################################################################################################################
        InputNumber_ConvertedToFloat = float(InputNumber)
        #######################################################################################################################

    except:
        #######################################################################################################################
        exceptions = sys.exc_info()[0]
        print(TellWhichFileWereIn() + ", PassThroughFloatValuesInRange_ExitProgramOtherwise Error. InputNumber '" + InputNameString + "' must be a float value, Exceptions: %s" % exceptions)
        traceback.print_exc()

        ##########################
        if ExitProgramIfFailureFlag == 1:
            sys.exit()
        else:
            return -11111.0
        ##########################

        #######################################################################################################################

    #######################################################################################################################
    #######################################################################################################################

    #######################################################################################################################
    #######################################################################################################################
    try:

        #######################################################################################################################
        InputNumber_ConvertedToFloat_Limited = LimitNumber_FloatOutputOnly(RangeMinValue, RangeMaxValue, InputNumber_ConvertedToFloat)

        if InputNumber_ConvertedToFloat_Limited != InputNumber_ConvertedToFloat:
            print(TellWhichFileWereIn() + ", PassThroughFloatValuesInRange_ExitProgramOtherwise Error. '" +
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
        #######################################################################################################################

    except:
        #######################################################################################################################
        exceptions = sys.exc_info()[0]
        print(TellWhichFileWereIn() + ", PassThroughFloatValuesInRange_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)
        traceback.print_exc()

        ##########################
        if ExitProgramIfFailureFlag == 1:
            sys.exit()
        else:
            return -11111.0
        ##########################

        #######################################################################################################################

    #######################################################################################################################
    #######################################################################################################################

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

##########################################################################################################
##########################################################################################################
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
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def GUI_update_clock():
    global root
    global EXIT_PROGRAM_FLAG
    global GUI_RootAfterCallbackInterval_Milliseconds
    global USE_GUI_FLAG

    global CameraStreamerClass_ReubenPython2and3ClassObject
    global CameraStreamerClass_OPEN_FLAG
    global SHOW_IN_GUI_CameraStreamerClass_FLAG

    global MyPrint_ReubenPython2and3ClassObject
    global MyPrint_OPEN_FLAG
    global SHOW_IN_GUI_MyPrint_FLAG

    if USE_GUI_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
        #########################################################
        #########################################################

            #########################################################
            if CameraStreamerClass_OPEN_FLAG == 1 and SHOW_IN_GUI_CameraStreamerClass_FLAG == 1:
                CameraStreamerClass_ReubenPython2and3ClassObject.GUI_update_clock()
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

##########################################################################################################
##########################################################################################################
def ExitProgram_Callback(OptionalArugment = 0):
    global EXIT_PROGRAM_FLAG

    print("ExitProgram_Callback event fired!")

    EXIT_PROGRAM_FLAG = 1
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def GUI_Thread():
    global root
    global Camera_RootIfLaunchedStandalone_Xpos
    global Camera_RootIfLaunchedStandalone_Ypos
    global Camera_RootIfLaunchedStandalone_width
    global Camera_RootIfLaunchedStandalone_height
    global GUI_RootAfterCallbackInterval_Milliseconds
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
    global Tab_CameraStreamerClass
    global Tab_MyPrint

    if USE_TABS_IN_GUI_FLAG == 1:
        #################################################
        TabControlObject = ttk.Notebook(root)

        Tab_CameraStreamerClass = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_CameraStreamerClass, text='   CAMERA   ')

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
    else:
        #################################################
        Tab_MainControls = root
        Tab_CameraStreamerClass = root
        Tab_MyPrint = root
        #################################################

    #################################################
    #################################################

    ################################################# THIS BLOCK MUST COME 2ND-TO-LAST IN def GUI_Thread() IF USING TABS.
    root.protocol("WM_DELETE_WINDOW", ExitProgram_Callback)  # Set the callback function for when the window's closed.
    root.title("test_program_for_CameraStreamerClass_ReubenPython2and3Class")
    root.geometry('%dx%d+%d+%d' % (Camera_RootIfLaunchedStandalone_width, Camera_RootIfLaunchedStandalone_height, Camera_RootIfLaunchedStandalone_Xpos, Camera_RootIfLaunchedStandalone_Ypos)) # set the dimensions of the screen and where it is placed
    root.after(GUI_RootAfterCallbackInterval_Milliseconds, GUI_update_clock)
    root.mainloop()
    #################################################

    #################################################  THIS BLOCK MUST COME LAST IN def GUI_Thread() REGARDLESS OF CODE.
    root.quit() #Stop the GUI thread, MUST BE CALLED FROM GUI_Thread
    root.destroy() #Close down the GUI thread, MUST BE CALLED FROM GUI_Thread
    #################################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
if __name__ == '__main__':

    ################################################
    ################################################
    global my_platform
    global ParametersToBeLoaded_Directory_TO_BE_USED

    my_platform = GetMyPlatform()

    if my_platform == "windows":
        ParametersToBeLoaded_Directory_TO_BE_USED = ParametersToBeLoaded_Directory_Windows

    elif my_platform == "linux":
        ParametersToBeLoaded_Directory_TO_BE_USED = ParametersToBeLoaded_Directory_LinuxNonRaspberryPi

    elif my_platform == "pi":
        ParametersToBeLoaded_Directory_TO_BE_USED = ParametersToBeLoaded_Directory_LinuxRaspberryPi

    elif my_platform == "mac":
        ParametersToBeLoaded_Directory_TO_BE_USED = ParametersToBeLoaded_Directory_Mac

    else:
        "test_program_for_CameraStreamerClass_ReubenPython2and3Class.py: ERROR, OS must be Windows, LinuxNonRaspberryPi, or Mac!"
        ExitProgram_Callback()

    print("ParametersToBeLoaded_Directory_TO_BE_USED: " + ParametersToBeLoaded_Directory_TO_BE_USED)
    ################################################
    ################################################

    ##################################################
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
    global EnableCameraEncodeThreadFlag
    global EnableImageSavingThreadFlag
    global RemoveFisheyeDistortionFromImage_Flag
    global ShowOpenCVwindowsFlag
    global OpenCVwindowPosX
    global OpenCVwindowPosY
    global OpenCVwindow_UpdateEveryNmilliseconds
    global OpenCVbackendToUseEnglishName
    global Camera_SavedImages_FilenamePrefix
    global Camera_SavedImages_LocalDirectoryNameNoSlashes
    global Camera_RootIfLaunchedStandalone_Xpos
    global Camera_RootIfLaunchedStandalone_Ypos
    global Camera_RootIfLaunchedStandalone_width
    global Camera_RootIfLaunchedStandalone_height
    #################################################
    #################################################

    #################################################
    #################################################
    argparse_Object = argparse.ArgumentParser()
    #nargs='?', const='arg_was_not_given' is the key to allowing us to not input an argument (use Pycharm "run")
    argparse_Object.add_argument("-c", "--camera", nargs='?', const='arg_was_not_given', required=False, help="Camera number in the set [0, 1, ..., TotalNumberOfCameras]")
    argparse_Object.add_argument("-p", "--parametersfile", nargs='?', const='arg_was_not_given', required=False, help="Must pass the directory path of ParametersToBeLoaded_CameraStreamerClass.json")
    ARGV_Dict = vars(argparse_Object.parse_args())
    print("ARGV_Dict: " + str(ARGV_Dict))

    #################################################
    global parametersfile
    parametersfile = ""
    if ARGV_Dict["parametersfile"] != None:
        ParametersToBeLoaded_Directory_TO_BE_USED = str(ARGV_Dict["parametersfile"])
    else:
        ParametersToBeLoaded_Directory_TO_BE_USED = ParametersToBeLoaded_Directory_TO_BE_USED

    print("ParametersToBeLoaded_Directory_TO_BE_USED: " + str(ParametersToBeLoaded_Directory_TO_BE_USED))
    #################################################

    #################################################
    #################################################

    #################################################
    #################################################
    ReturnedDict = LoadAndParseJSONfile_CameraStreamerClass()
    print("ReturnedDict: " + str(ReturnedDict))

    if len(ReturnedDict) == 0:
        ################################################# CNA HARD-WIRE THE VALUES HERE WITHOUT USING AN INPUT FILE
        camera_TkinterPreviewImageScalingFactor =  0.70
        camera_selection_number =  0
        camera_Dshow_EnglishName  = ""
        CameraCaptureThread_TimeToSleepEachLoop = 0.030
        CameraEncodeThread_TimeToSleepEachLoop = 0.030
        ImageSavingThread_TimeToSleepEachLoop = 0.030
        camera_frame_rate = 30
        image_width = 640
        image_height = 480
        image_jpg_encoding_quality = 100
        CameraSetting_Autofocus = 0
        CameraSetting_Autoexposure = 0
        CameraSetting_exposure = -10
        CameraSetting_gain = 0
        CameraSetting_brightness = 0
        CameraSetting_contrast = 255
        CameraSetting_saturation = 50
        CameraSetting_hue = 0
        EnableCameraEncodeThreadFlag = 1
        EnableImageSavingThreadFlag = 1
        RemoveFisheyeDistortionFromImage_Flag = 0
        OpenCVwindow_UpdateEveryNmilliseconds = 30
        OpenCVbackendToUseEnglishName = "CAP_MSMF"
        Camera_SavedImages_LocalDirectoryNameNoSlashes =  "SavedImages"
        Camera_SavedImages_FilenamePrefix =  "Camera_"
        Camera_RootIfLaunchedStandalone_Xpos = 0
        Camera_RootIfLaunchedStandalone_Ypos = 0
        Camera_RootIfLaunchedStandalone_width = 1000
        Camera_RootIfLaunchedStandalone_height = 1000
        CameraCalibrationParametersDict = dict([("fx", 532.972485),
                                                    ("fy", 532.972485),
                                                    ("cx", 320.000000),
                                                    ("cy", 240.000000),
                                                    ("k1", -1.105115),
                                                    ("k2", 1.372161),
                                                    ("p1", -0.001400),
                                                    ("p2", -0.021523)])
        #################################################

    #################################################
    #################################################

    ################################################# PUTTING THIS AFTER EVERYTHING SO THAT WE CAN OVERRIDE -P FILE OPTIONS
    if ARGV_Dict["camera"] != None:
        camera_selection_number = int(ARGV_Dict["camera"])

    print("camera_selection_number: " + str(camera_selection_number))
    #################################################

    #################################################
    #################################################
    global USE_GUI_FLAG
    USE_GUI_FLAG = 1

    global USE_KEYBOARD_FLAG
    USE_KEYBOARD_FLAG = 1

    global USE_TABS_IN_GUI_FLAG
    USE_TABS_IN_GUI_FLAG = 1

    global USE_CameraStreamerClass_FLAG
    USE_CameraStreamerClass_FLAG = 1

    global USE_MyPrint_FLAG
    USE_MyPrint_FLAG = 1
    #################################################
    #################################################

    #################################################
    #################################################
    global SHOW_IN_GUI_CameraStreamerClass_FLAG
    SHOW_IN_GUI_CameraStreamerClass_FLAG = 1

    global SHOW_IN_GUI_MyPrint_FLAG
    SHOW_IN_GUI_MyPrint_FLAG = 1
    #################################################
    #################################################

    #################################################
    #################################################
    global GUI_ROW_CameraStreamerClass
    global GUI_COLUMN_CameraStreamerClass
    global GUI_PADX_CameraStreamerClass
    global GUI_PADY_CameraStreamerClass
    global GUI_ROWSPAN_CameraStreamerClass
    global GUI_COLUMNSPAN_CameraStreamerClass
    GUI_ROW_CameraStreamerClass = 1

    GUI_COLUMN_CameraStreamerClass = 0
    GUI_PADX_CameraStreamerClass = 1
    GUI_PADY_CameraStreamerClass = 10
    GUI_ROWSPAN_CameraStreamerClass = 1
    GUI_COLUMNSPAN_CameraStreamerClass = 1

    global GUI_ROW_MyPrint
    global GUI_COLUMN_MyPrint
    global GUI_PADX_MyPrint
    global GUI_PADY_MyPrint
    global GUI_ROWSPAN_MyPrint
    global GUI_COLUMNSPAN_MyPrint
    GUI_ROW_MyPrint = 2

    GUI_COLUMN_MyPrint = 0
    GUI_PADX_MyPrint = 1
    GUI_PADY_MyPrint = 10
    GUI_ROWSPAN_MyPrint = 1
    GUI_COLUMNSPAN_MyPrint = 1
    #################################################
    #################################################

    #################################################
    #################################################
    global EXIT_PROGRAM_FLAG
    EXIT_PROGRAM_FLAG = 0

    global root

    global CurrentTime_MainLoopThread
    CurrentTime_MainLoopThread = -11111.0

    global StartingTime_MainLoopThread
    StartingTime_MainLoopThread = -11111.0

    global TabControlObject
    global Tab_MainControls
    global Tab_CameraStreamerClass
    global Tab_MyPrint

    global GUI_RootAfterCallbackInterval_Milliseconds
    GUI_RootAfterCallbackInterval_Milliseconds = 30
    #################################################
    #################################################

    #################################################
    #################################################

    #################################################
    global CameraStreamerClass_ReubenPython2and3ClassObject

    global CameraStreamerClass_OPEN_FLAG
    CameraStreamerClass_OPEN_FLAG = -1

    global CameraStreamerClass_MostRecentDict
    CameraStreamerClass_MostRecentDict = dict()

    global CameraStreamerClass_MostRecentDict_OriginalImage
    #CameraStreamerClass_MostRecentDict_OriginalImage = numpy.zeros((image_height, image_width, 3), numpy.uint8)

    global CameraStreamerClass_MostRecentDict_Time
    CameraStreamerClass_MostRecentDict_Time = -11111.0
    #################################################

    #################################################
    #################################################

    #################################################
    #################################################
    global MyPrint_ReubenPython2and3ClassObject

    global MyPrint_OPEN_FLAG
    MyPrint_OPEN_FLAG = -1
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
        Tab_CameraStreamerClass = None
        Tab_MyPrint = None
    #################################################
    #################################################

    #################################################
    #################################################
    global CameraStreamerClass_ReubenPython2and3ClassObject_GUIparametersDict
    CameraStreamerClass_ReubenPython2and3ClassObject_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_CameraStreamerClass_FLAG),
                                    ("root", Tab_CameraStreamerClass),
                                    ("EnableInternal_MyPrint_Flag", 1),
                                    ("NumberOfPrintLines", 10),
                                    ("UseBorderAroundThisGuiObjectFlag", 0),
                                    ("GUI_ROW", GUI_ROW_CameraStreamerClass),
                                    ("GUI_COLUMN", GUI_COLUMN_CameraStreamerClass),
                                    ("GUI_PADX", GUI_PADX_CameraStreamerClass),
                                    ("GUI_PADY", GUI_PADY_CameraStreamerClass),
                                    ("GUI_ROWSPAN", GUI_ROWSPAN_CameraStreamerClass),
                                    ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_CameraStreamerClass)])

    global CameraStreamerClass_ReubenPython2and3ClassObject_setup_dict
    CameraStreamerClass_ReubenPython2and3ClassObject_setup_dict = dict([("GUIparametersDict", CameraStreamerClass_ReubenPython2and3ClassObject_GUIparametersDict),
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
                                                                        ("EnableCameraEncodeThreadFlag", EnableCameraEncodeThreadFlag),
                                                                        ("EnableImageSavingThreadFlag", EnableImageSavingThreadFlag),
                                                                        ("RemoveFisheyeDistortionFromImage_Flag", RemoveFisheyeDistortionFromImage_Flag),
                                                                        ("OpenCVbackendToUseEnglishName", OpenCVbackendToUseEnglishName),
                                                                        ("Camera_SavedImages_FilenamePrefix", Camera_SavedImages_FilenamePrefix),
                                                                        ("Camera_SavedImages_LocalDirectoryNameNoSlashes", Camera_SavedImages_LocalDirectoryNameNoSlashes)])

                                                                        #("RemoveFisheyeDistortionFromImage_Flag", RemoveFisheyeDistortionFromImage_Flag),
                                                                        #("CameraCalibrationParametersDict", CameraCalibrationParametersDict)

    if USE_CameraStreamerClass_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            CameraStreamerClass_ReubenPython2and3ClassObject = CameraStreamerClass_ReubenPython2and3Class(CameraStreamerClass_ReubenPython2and3ClassObject_setup_dict)
            CameraStreamerClass_OPEN_FLAG = CameraStreamerClass_ReubenPython2and3ClassObject.OBJECT_CREATED_SUCCESSFULLY_FLAG

            #################################################
            if USE_CameraStreamerClass_FLAG == 1 and CameraStreamerClass_OPEN_FLAG != 1:
                print("Failed to open CameraStreamerClass_ReubenPython2and3Class.")
                ExitProgram_Callback()
            #################################################

        except:
            exceptions = sys.exc_info()[0]
            print("CameraStreamerClass_ReubenPython2and3ClassObject __init__: Exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_MyPrint_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:

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
    if USE_KEYBOARD_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        keyboard.on_press_key("esc", ExitProgram_Callback)
    #################################################
    #################################################

    #################################################
    #################################################
    if EXIT_PROGRAM_FLAG == 0:
        print("Starting main loop 'test_program_for_CameraStreamerClass_ReubenPython2and3Class.")
        StartingTime_MainLoopThread = getPreciseSecondsTimeStampString()
    #################################################
    #################################################

    #################################################
    #################################################
    while(EXIT_PROGRAM_FLAG == 0):

        ###################################################
        CurrentTime_MainLoopThread = getPreciseSecondsTimeStampString() - StartingTime_MainLoopThread
        ###################################################

        ################################################### GET's
        if CameraStreamerClass_OPEN_FLAG == 1:

            CameraStreamerClass_MostRecentDict = CameraStreamerClass_ReubenPython2and3ClassObject.GetMostRecentDataDict()

            if "Time" in CameraStreamerClass_MostRecentDict:
                CameraStreamerClass_MostRecentDict_OriginalImage = CameraStreamerClass_MostRecentDict["OriginalImage"]
                CameraStreamerClass_MostRecentDict_Time = CameraStreamerClass_MostRecentDict["Time"]

                #print("CameraStreamerClass_MostRecentDict_Time: " + str(CameraStreamerClass_MostRecentDict_Time))
        ###################################################

        time.sleep(0.030)
    #################################################
    #################################################

    ################################################# THIS IS THE EXIT ROUTINE!
    #################################################
    print("Exiting main program 'test_program_for_CameraStreamerClass_ReubenPython2and3Class.")

    #################################################
    if CameraStreamerClass_OPEN_FLAG == 1:
        CameraStreamerClass_ReubenPython2and3ClassObject.ExitProgram_Callback()
    #################################################

    #################################################
    if MyPrint_OPEN_FLAG == 1:
        MyPrint_ReubenPython2and3ClassObject.ExitProgram_Callback()
    #################################################

    #################################################
    #################################################

##########################################################################################################
##########################################################################################################