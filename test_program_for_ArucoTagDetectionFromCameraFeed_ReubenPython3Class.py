# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision G, 02/02/2025

Verified working on: Python 3.12 for Windows 11 64-bit, Ubuntu 20.04, and Raspberry Pi Bullseye, Bookworm (Backend = "CAP_ANY", Camera = ELP USB).
'''

__author__ = 'reuben.brewer'

#########################################################
#https://github.com/Reuben-Brewer/ArucoTagDetectionFromCameraFeed_ReubenPython3Class
from ArucoTagDetectionFromCameraFeed_ReubenPython3Class import *

#https://github.com/Reuben-Brewer/CSVdataLogger_ReubenPython3Class
from CSVdataLogger_ReubenPython3Class import *

#https://github.com/Reuben-Brewer/MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class
from MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class import *

#https://github.com/Reuben-Brewer/MyPrint_ReubenPython2and3Class
from MyPrint_ReubenPython2and3Class import *

#https://github.com/Reuben-Brewer/UDPdataExchanger_ReubenPython3Class
from UDPdataExchanger_ReubenPython3Class import *
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
import re #for def ParseColonCommaSeparatedVariableString
import keyboard
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

global ParametersToBeLoaded_Directory_LinuxRaspberryPi
ParametersToBeLoaded_Directory_LinuxRaspberryPi = "//home//pinis//Desktop//ArucoTagDetectionFromCameraFeed_PythonDeploymentFiles//ParametersToBeLoaded"

global LogFile_Directory_LinuxRaspberryPi
LogFile_Directory_LinuxRaspberryPi = "//home//pinis//Desktop//ArucoTagDetectionFromCameraFeed_PythonDeploymentFiles//Logs"

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
        SOFTWARE_LAUNCH_METHOD = ""

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
        #traceback.print_exc()

    print("ARGV_1, USE_GUI_FLAG_ARGV_OVERRIDE: " + str(USE_GUI_FLAG_ARGV_OVERRIDE))
    print("ARGV_1, SOFTWARE_LAUNCH_METHOD: " + str(SOFTWARE_LAUNCH_METHOD))

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

    try:
        ProperlyFormattedStringForPrinting = ""
        ItemsPerLineCounter = 0

        for Key in DictToPrint:

            if isinstance(DictToPrint[Key], dict): #RECURSION
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                     str(Key) + ":\n" + \
                                                     ConvertDictToProperlyFormattedStringForPrinting(DictToPrint[Key], NumberOfDecimalsPlaceToUse, NumberOfEntriesPerLine, NumberOfTabsBetweenItems)

            else:
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                     str(Key) + ": " + \
                                                     ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(DictToPrint[Key], 0, NumberOfDecimalsPlaceToUse)

            if ItemsPerLineCounter < NumberOfEntriesPerLine - 1:
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\t"*NumberOfTabsBetweenItems
                ItemsPerLineCounter = ItemsPerLineCounter + 1
            else:
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\n"
                ItemsPerLineCounter = 0

        return ProperlyFormattedStringForPrinting

    except:
        exceptions = sys.exc_info()[0]
        print("ConvertDictToProperlyFormattedStringForPrinting, Exceptions: %s" % exceptions)
        return ""
        # traceback.print_exc()
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def LimitNumber_FloatOutputOnly(min_val, max_val, test_val):
    if test_val > max_val:
        test_val = max_val

    elif test_val < min_val:
        test_val = min_val

    else:
        test_val = test_val

    test_val = float(test_val)

    return test_val
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def LimitNumber_IntOutputOnly(min_val, max_val, test_val):
    if test_val > max_val:
        test_val = max_val

    elif test_val < min_val:
        test_val = min_val

    else:
        test_val = test_val

    test_val = int(test_val)

    return test_val
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def LimitTextEntryInput(min_val, max_val, test_val, TextEntryObject):

    test_val = float(test_val)  # MUST HAVE THIS LINE TO CATCH STRINGS PASSED INTO THE FUNCTION

    if test_val > max_val:
        test_val = max_val
    elif test_val < min_val:
        test_val = min_val
    else:
        test_val = test_val

    if TextEntryObject != "":
        if isinstance(TextEntryObject, list) == 1:  # Check if the input 'TextEntryObject' is a list or not
            TextEntryObject[0].set(str(test_val))  # Reset the text, overwriting the bad value that was entered.
        else:
            TextEntryObject.set(str(test_val))  # Reset the text, overwriting the bad value that was entered.

    return test_val
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

#######################################################################################################################
#######################################################################################################################
def LoadAndParseJSONfile_UseClassesFlags():
    global ParametersToBeLoaded_UseClassesFlags_Dict
    global USE_GUI_FLAG
    global USE_GUI_FLAG_ARGV_OVERRIDE

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
def LoadAndParseJSONfile_UDPdataExchanger():
    global ParametersToBeLoaded_UDPdataExchanger_Dict

    print("Calling LoadAndParseJSONfile_UDPdataExchanger().")

    #################################
    JSONfilepathFull_UDPdataExchanger = ParametersToBeLoaded_Directory_TO_BE_USED + "//ParametersToBeLoaded_UDPdataExchanger.json"
    ParametersToBeLoaded_UDPdataExchanger_Dict = LoadAndParseJSONfile_AddDictKeysToGlobalsDict(globals(), JSONfilepathFull_UDPdataExchanger, USE_PassThrough0and1values_ExitProgramOtherwise_FOR_FLAGS = 0, PrintResultsFlag = 1, PauseForInputOnException = 1)
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

    global UDPdataExchanger_Object
    global UDPdataExchanger_OPEN_FLAG
    global SHOW_IN_GUI_UDPdataExchanger_FLAG
    global UDPdataExchanger_MostRecentDict
    global UDPdataExchanger_MostRecentDict_Label

    global DebuggingInfo_Label
    global ArucoTag_TranslationVectorOfMarkerCenter_PythonList_PrimaryMarker

    if USE_GUI_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
        #########################################################
        #########################################################

                try:

                    #########################################################
                    DebuggingInfo_Label["text"]  = "ArucoTag_TranslationVectorOfMarkerCenter_PythonList_PrimaryMarker: " + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(ArucoTag_TranslationVectorOfMarkerCenter_PythonList_PrimaryMarker, 0, 3)
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

                    #########################################################
                    root.after(GUI_RootAfterCallbackInterval_Milliseconds, GUI_update_clock)
                    #########################################################

                except:
                    exceptions = sys.exc_info()[0]
                    print("test_program_for_ArucoTagDetectionFromCameraFeed_ReubenPython3Class.py, GUI_update_clock, Exceptions: %s" % exceptions)
                    traceback.print_exc()
        #########################################################
        #########################################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
def ExitProgram_Callback(OptionalArugment = 0):
    global EXIT_PROGRAM_FLAG
    global CSVdataLogger_ReubenPython3ClassObject
    global CSVdataLogger_OPEN_FLAG
    global ArucoTagDetectionFromCameraFeed_ReubenPython3ClassObject
    global ArucoTag_OPEN_FLAG

    try:
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        if CSVdataLogger_OPEN_FLAG == 1:

            ##########################################################################################################
            ##########################################################################################################
            if CSVdataLogger_ReubenPython3ClassObject.IsSaving() == 0:

                ##########################################################################################################
                ##########################################################################################################
                if ArucoTag_OPEN_FLAG == 1:

                    ##########################################################################################################
                    if ArucoTagDetectionFromCameraFeed_ReubenPython3ClassObject.IsSaving() == 0:
                        print("ExitProgram_Callback event fired!")
                        EXIT_PROGRAM_FLAG = 1
                    ##########################################################################################################

                    ##########################################################################################################
                    else:
                        print("ArucoTagDetectionFromCameraFeed is saving, cannot exit!")
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
            else:
                print("CSV is saving, cannot exit!")
                EXIT_PROGRAM_FLAG = 0
            ##########################################################################################################
            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        else:

            ##########################################################################################################
            ##########################################################################################################
            if ArucoTag_OPEN_FLAG == 1:

                ##########################################################################################################
                if ArucoTagDetectionFromCameraFeed_ReubenPython3ClassObject.IsSaving() == 0:
                    print("ExitProgram_Callback event fired!")
                    EXIT_PROGRAM_FLAG = 1
                ##########################################################################################################

                ##########################################################################################################
                else:
                    print("ArucoTagDetectionFromCameraFeed is saving, cannot exit!")
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
    except:
        EXIT_PROGRAM_FLAG = 1

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################

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

    ###########################################################
    ###########################################################
    global DebuggingInfo_Label
    DebuggingInfo_Label = Label(Tab_MainControls, text="DebuggingInfo_Label", width=120, font=("Helvetica", 10))  #
    DebuggingInfo_Label.grid(row=1, column=0, padx=GUIbuttonPadX, pady=GUIbuttonPadY, columnspan=10, rowspan=1)
    ###########################################################
    ###########################################################

    #################################################
    #################################################
    global UDPdataExchanger_MostRecentDict_Label
    UDPdataExchanger_MostRecentDict_Label = Label(Tab_MainControls, text="UDPdataExchanger_MostRecentDict_Label", width=120, font=("Helvetica", 10))
    UDPdataExchanger_MostRecentDict_Label.grid(row=2, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
    #################################################
    #################################################

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

    elif my_platform == "pi":
        ParametersToBeLoaded_Directory_TO_BE_USED = ParametersToBeLoaded_Directory_LinuxRaspberryPi
        LogFile_Directory_TO_BE_USED = LogFile_Directory_LinuxRaspberryPi

    elif my_platform == "mac":
        ParametersToBeLoaded_Directory_TO_BE_USED = ParametersToBeLoaded_Directory_Mac
        LogFile_Directory_TO_BE_USED = LogFile_Directory_Mac

    else:
        "test_program_for_ArucoTagDetectionFromCameraFeed_ReubenPython3Class.py: ERROR, OS must be Windows, LinuxNonRaspberryPi, or Mac!"
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

    print("test_program_for_ArucoTagDetectionFromCameraFeed_ReubenPython3Class.py, USE_GUI_FLAG_ARGV_OVERRIDE: " + str(USE_GUI_FLAG_ARGV_OVERRIDE) +
          ", SOFTWARE_LAUNCH_METHOD: " + str(SOFTWARE_LAUNCH_METHOD))


    if SOFTWARE_LAUNCH_METHOD.upper().find("RCLOCAL") != -1: #Contains something about rc.local
        USE_GUI_FLAG_ARGV_OVERRIDE = 0
        print("$$$$$$$$$$$$$$$$$$$ RCLOCAL LAUNCH DETECTED, DISABLING THE GUI $$$$$$$$$$$$$$$$$$$")
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
    global USE_UDPdataExchanger_FLAG
    global USE_GUI_FLAG
    global USE_KEYBOARD_FLAG
    global USE_PrintUDPdataForDebuggingFlag

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
    
    global GUI_ROW_UDPdataExchanger
    global GUI_COLUMN_UDPdataExchanger
    global GUI_PADX_UDPdataExchanger
    global GUI_PADY_UDPdataExchanger
    global GUI_ROWSPAN_UDPdataExchanger
    global GUI_COLUMNSPAN_UDPdataExchanger

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
    global ArucoTag_DistanceBetweenPrimaryMarkerAndSecondaryMarker
    global ArucoTag_DistanceBetweenPrimaryMarkerAndSecondaryMarker_ClosenessThreshold
    global ArucoTag_HowManyFramesAcceptedBetweenMarkers
    global ArucoTag_BadDataCounter_Threshold
    global ArucoTag_DetectInvertedMarkersAsWellAsNormalOnesFlag
    global ArucoTag_MarkerIDToDetect_PrimaryMarker
    global ArucoTag_MarkerIDToDetect_SecondaryMarker

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
    global UDPdataExchanger_Directions
    global UDPdataExchanger_NameToDisplay_UserSet
    global UDPdataExchanger_UDP_RxOrTxRole
    global UDPdataExchanger_IPV4_address
    global UDPdataExchanger_IPV4_Port
    global UDPdataExchanger_UDP_BufferSizeInBytes
    global UDPdataExchanger_MainThread_TimeToSleepEachLoop

    LoadAndParseJSONfile_UDPdataExchanger()
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
    global Tab_UDPdataExchanger

    global CurrentTime_MainLoopThread
    CurrentTime_MainLoopThread = -11111.0

    global StartingTime_MainLoopThread
    StartingTime_MainLoopThread = -11111.0

    global BadDataCounter
    BadDataCounter = 0

    global ArucoTag_TranslationVectorOfMarkerCenter_PythonList_PrimaryMarker
    ArucoTag_TranslationVectorOfMarkerCenter_PythonList_PrimaryMarker = [-11111.0]*3

    global ArucoTag_RotationVectorOfMarkerCenter_EulerAnglesXYZrollPitchYawInDegrees_PythonList_PrimaryMarker
    ArucoTag_RotationVectorOfMarkerCenter_EulerAnglesXYZrollPitchYawInDegrees_PythonList_PrimaryMarker = [-11111.0] * 3

    global ArucoTag_RotationVectorOfMarkerCenter_EulerAnglesXYZrollPitchYawInRadians_PythonList_PrimaryMarker
    ArucoTag_RotationVectorOfMarkerCenter_EulerAnglesXYZrollPitchYawInRadians_PythonList_PrimaryMarker = [-11111.0] * 3

    global ArucoTag_DetectionTimeInMilliseconds_PrimaryMarker
    ArucoTag_DetectionTimeInMilliseconds_PrimaryMarker = -11111.0

    global ArucoTag_DetectionTimeInMilliseconds_PrimaryMarker_Last
    ArucoTag_DetectionTimeInMilliseconds_PrimaryMarker = -11111.0

    global ArucoTag_TranslationVectorOfMarkerCenter_PythonList_SecondaryMarker
    ArucoTag_TranslationVectorOfMarkerCenter_PythonList_SecondaryMarker = [-11111.0] * 3

    global ArucoTag_RotationVectorOfMarkerCenter_EulerAnglesXYZrollPitchYawInDegrees_PythonList_SecondaryMarker
    ArucoTag_RotationVectorOfMarkerCenter_EulerAnglesXYZrollPitchYawInDegrees_PythonList_SecondaryMarker = [-11111.0] * 3

    global ArucoTag_RotationVectorOfMarkerCenter_EulerAnglesXYZrollPitchYawInRadians_PythonList_SecondaryMarker
    ArucoTag_RotationVectorOfMarkerCenter_EulerAnglesXYZrollPitchYawInRadians_PythonList_SecondaryMarker = [-11111.0] * 3

    global ArucoTag_DetectionTimeInMilliseconds_SecondaryMarker
    ArucoTag_DetectionTimeInMilliseconds_SecondaryMarker = -11111.0

    global ArucoTag_DetectionTimeInMilliseconds_SecondaryMarker_Last
    ArucoTag_DetectionTimeInMilliseconds_SecondaryMarker_Last = -11111.0

    global LineFromPrimaryMarkerToSecondaryMarker_NumpyArray
    LineFromPrimaryMarkerToSecondaryMarker_NumpyArray = numpy.array([-11111.0]*3)

    global LineFromPrimaryMarkerToSecondaryMarker_DistanceMM
    LineFromPrimaryMarkerToSecondaryMarker_DistanceMM = -11111.0

    global LineFromPrimaryMarkerToSecondaryMarker_AngleWRTground
    LineFromPrimaryMarkerToSecondaryMarker_AngleWRTground = -11111.0
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
    global UDPdataExchanger_Object
    UDPdataExchanger_Object = list()

    global UDPdataExchanger_OPEN_FLAG
    UDPdataExchanger_OPEN_FLAG = 0

    global UDPdataExchanger_MostRecentDict
    UDPdataExchanger_MostRecentDict = dict()
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

    #################################################
    #################################################
    print("USE_GUI_FLAG: " + str(USE_GUI_FLAG))
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
    ArucoTagDetectionFromCameraFeed_ReubenPython3Class_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG),
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

    if USE_ArucoTag_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            print("Preparing to create and start ArucoTagDetectionFromCameraFeed_ReubenPython3ClassObject.")
            ArucoTagDetectionFromCameraFeed_ReubenPython3ClassObject = ArucoTagDetectionFromCameraFeed_ReubenPython3Class(ArucoTagDetectionFromCameraFeed_ReubenPython3Class_setup_dict)
            ArucoTag_OPEN_FLAG = ArucoTagDetectionFromCameraFeed_ReubenPython3ClassObject.OBJECT_CREATED_SUCCESSFULLY_FLAG

            #################################################
            if ArucoTag_OPEN_FLAG != 1:
                print("Failed to open ArucoTagDetectionFromCameraFeed_ReubenPython3ClassObject.")
                ExitProgram_Callback()
            #################################################

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
                                                                                ("CSVfile_DirectoryPath", "C:\\CSVfiles"),
                                                                                ("FileNamePrefix", "Aruco_"),
                                                                                ("VariableNamesForHeaderList", ["Time (S)",
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

    if USE_CSVdataLogger_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            print("Preparing to create and start CSVdataLogger_ReubenPython3ClassObject.")
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
            print("Preparing to create and start MyPrint_ReubenPython2and3ClassObject.")
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
    global UDPdataExchanger_GUIparametersDict
    UDPdataExchanger_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_UDPdataExchanger_FLAG),
                                    ("root", Tab_MainControls),
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
                                        ("NameToDisplay_UserSet", UDPdataExchanger_NameToDisplay_UserSet),
                                        ("UDP_RxOrTxRole", UDPdataExchanger_UDP_RxOrTxRole),
                                        ("IPV4_address", UDPdataExchanger_IPV4_address),
                                        ("IPV4_Port", UDPdataExchanger_IPV4_Port),
                                        ("UDP_BufferSizeInBytes", UDPdataExchanger_UDP_BufferSizeInBytes),
                                        ("MainThread_TimeToSleepEachLoop", UDPdataExchanger_MainThread_TimeToSleepEachLoop)])
    #################################################

    #################################################
    if USE_UDPdataExchanger_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            print("Preparing to create and start UDPdataExchanger_Object.")
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

    if USE_GUI_FLAG == 1 and USE_MyPlotterPureTkinterStandAloneProcess_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            print("Preparing to create and start MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject.")
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

    ################################################# THIS SECTION IS FOR CREATING AND SAVING ARUCO TAGS
    #################################################
    if EXIT_PROGRAM_FLAG == 0:
        pass

        '''
        for ID_integer in range(1,13):
            print(ID_integer)
            ArucoTagDetectionFromCameraFeed_ReubenPython3ClassObject.CreateAndSaveImageOfArucoTagMarker(ID_integer=ID_integer, ArucoTag_DictType_EnglishString = "",EdgeLengthInPixels_integer = 350, WhiteBorderPixelWidth_integer = 50, BlackOutermostBorderPixelWidth_integer=1)
        
        ArucoTagDetectionFromCameraFeed_ReubenPython3ClassObject.CreateAndSaveImageOfArucoTagMarker(ID_integer=0, ArucoTag_DictType_EnglishString = "",EdgeLengthInPixels_integer = 1000, WhiteBorderPixelWidth_integer = 50)
        ArucoTagDetectionFromCameraFeed_ReubenPython3ClassObject.CreateAndSaveImageOfArucoTagMarker(ID_integer=1, ArucoTag_DictType_EnglishString = "",EdgeLengthInPixels_integer = 1000, WhiteBorderPixelWidth_integer = 50)
        EXIT_PROGRAM_FLAG = 1
        '''
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_KEYBOARD_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        print("Preparing to enable keyboard.")
        keyboard.on_press_key("esc", ExitProgram_Callback)
    #################################################
    #################################################

    #################################################
    #################################################
    if EXIT_PROGRAM_FLAG == 0:
        print("Starting main loop 'test_program_for_ArucoTagDetectionFromCameraFeed_ReubenPython3Class.py.")
        StartingTime_MainLoopThread = getPreciseSecondsTimeStampString()
    #################################################
    #################################################

    #################################################
    #################################################
    #################################################
    #################################################
    while(EXIT_PROGRAM_FLAG == 0):

        #################################################
        #################################################
        #################################################
        CurrentTime_MainLoopThread = getPreciseSecondsTimeStampString() - StartingTime_MainLoopThread

        if USE_PrintUDPdataForDebuggingFlag == 1:
            print("CurrentTime_MainLoopThread: " + str(CurrentTime_MainLoopThread))
        #################################################
        #################################################
        #################################################

        ################################################# GET's
        #################################################
        #################################################
        if JSONfiles_NeedsToBeLoadedFlag == 1:
            LoadAndParseJSONfile_GUIsettings()

            LoadAndParseJSONfile_ArucoTagParameters()

            '''
            UPDATE PARAMETERS HERE UPON RELOADING JSON FILE
            '''

            JSONfiles_NeedsToBeLoadedFlag = 0
        #################################################
        #################################################
        #################################################

        ################################################# GET's
        #################################################
        #################################################
        if ArucoTag_OPEN_FLAG == 1:

            try:
                #################################################
                #################################################
                ArucoTag_MostRecentDict = ArucoTagDetectionFromCameraFeed_ReubenPython3ClassObject.GetMostRecentDataDict()
                #print("ArucoTag_MostRecentDict: " + str(ArucoTag_MostRecentDict))
                ####################################################
                ####################################################

                ####################################################
                ####################################################
                if "Time" in ArucoTag_MostRecentDict:

                    #################################################
                    ArucoTag_MostRecentDict_DataStreamingFrequency_CalculatedFromMainThread = ArucoTag_MostRecentDict["Frequency"]
                    ArucoTag_MostRecentDict_Time = ArucoTag_MostRecentDict["Time"]
                    ArucoTag_MostRecentDict_DetectedArucoTag_InfoDict = ArucoTag_MostRecentDict["DetectedArucoTag_InfoDict"]
                    #################################################

                    #################################################
                    if ArucoTag_MarkerIDToDetect_PrimaryMarker in ArucoTag_MostRecentDict_DetectedArucoTag_InfoDict:
                        ArucoTag_DetectionTimeInMilliseconds_PrimaryMarker = ArucoTag_MostRecentDict_DetectedArucoTag_InfoDict[ArucoTag_MarkerIDToDetect_PrimaryMarker]["ArucoTag_DetectionTimeInMilliseconds"]

                        if ArucoTag_DetectionTimeInMilliseconds_PrimaryMarker > ArucoTag_DetectionTimeInMilliseconds_PrimaryMarker_Last:
                            ArucoTag_TranslationVectorOfMarkerCenter_PythonList_PrimaryMarker = ArucoTag_MostRecentDict_DetectedArucoTag_InfoDict[ArucoTag_MarkerIDToDetect_PrimaryMarker]["ArucoTag_TranslationVectorOfMarkerCenter_PythonList"]
                            ArucoTag_RotationVectorOfMarkerCenter_EulerAnglesXYZrollPitchYawInDegrees_PythonList_PrimaryMarker = ArucoTag_MostRecentDict_DetectedArucoTag_InfoDict[ArucoTag_MarkerIDToDetect_PrimaryMarker]["ArucoTag_RotationVectorOfMarkerCenter_EulerAnglesXYZrollPitchYawInDegrees_PythonList"]
                            ArucoTag_RotationVectorOfMarkerCenter_EulerAnglesXYZrollPitchYawInRadians_PythonList_PrimaryMarker = ArucoTag_MostRecentDict_DetectedArucoTag_InfoDict[ArucoTag_MarkerIDToDetect_PrimaryMarker]["ArucoTag_RotationVectorOfMarkerCenter_EulerAnglesXYZrollPitchYawInRadians_PythonList"]

                            BadDataCounter = 0
                        else:
                            BadDataCounter = BadDataCounter + 1

                    else:
                        ArucoTag_DetectionTimeInMilliseconds_PrimaryMarker = -11111.0
                        BadDataCounter = BadDataCounter + 1

                    if BadDataCounter >= ArucoTag_BadDataCounter_Threshold:
                        ArucoTag_TranslationVectorOfMarkerCenter_PythonList_PrimaryMarker = [-11111.0]*3
                        ArucoTag_RotationVectorOfMarkerCenter_EulerAnglesXYZrollPitchYawInDegrees_PythonList_PrimaryMarker = [-11111.0]*3
                        ArucoTag_RotationVectorOfMarkerCenter_EulerAnglesXYZrollPitchYawInRadians_PythonList_PrimaryMarker = [-11111.0]*3

                    '''
                    if ArucoTag_MarkerIDToDetect_SecondaryMarker in ArucoTag_MostRecentDict_DetectedArucoTag_InfoDict:
                        ArucoTag_TranslationVectorOfMarkerCenter_PythonList_SecondaryMarker = ArucoTag_MostRecentDict_DetectedArucoTag_InfoDict[ArucoTag_MarkerIDToDetect_SecondaryMarker]["ArucoTag_TranslationVectorOfMarkerCenter_PythonList"]
                        ArucoTag_RotationVectorOfMarkerCenter_EulerAnglesXYZrollPitchYawInDegrees_PythonList_SecondaryMarker = ArucoTag_MostRecentDict_DetectedArucoTag_InfoDict[ArucoTag_MarkerIDToDetect_SecondaryMarker]["ArucoTag_RotationVectorOfMarkerCenter_EulerAnglesXYZrollPitchYawInDegrees_PythonList"]
                        ArucoTag_RotationVectorOfMarkerCenter_EulerAnglesXYZrollPitchYawInRadians_PythonList_SecondaryMarker = ArucoTag_MostRecentDict_DetectedArucoTag_InfoDict[ArucoTag_MarkerIDToDetect_SecondaryMarker]["ArucoTag_RotationVectorOfMarkerCenter_EulerAnglesXYZrollPitchYawInRadians_PythonList"]
                        ArucoTag_DetectionTimeInMilliseconds_SecondaryMarker = ArucoTag_MostRecentDict_DetectedArucoTag_InfoDict[ArucoTag_MarkerIDToDetect_SecondaryMarker]["ArucoTag_DetectionTimeInMilliseconds"]
                    '''
                    #################################################

                    '''
                    #################################################
                    if ArucoTag_MarkerIDToDetect_PrimaryMarker in ArucoTag_MostRecentDict_DetectedArucoTag_InfoDict and ArucoTag_MarkerIDToDetect_SecondaryMarker in ArucoTag_MostRecentDict_DetectedArucoTag_InfoDict:
                        if abs(ArucoTag_DetectionTimeInMilliseconds_PrimaryMarker - ArucoTag_DetectionTimeInMilliseconds_SecondaryMarker) < 30*ArucoTag_HowManyFramesAcceptedBetweenMarkers: #Both markers detected within N frames
                            LineFromPrimaryMarkerToSecondaryMarker_NumpyArray = numpy.array(ArucoTag_TranslationVectorOfMarkerCenter_PythonList_SecondaryMarker) - numpy.array(ArucoTag_TranslationVectorOfMarkerCenter_PythonList_PrimaryMarker)
                            LineFromPrimaryMarkerToSecondaryMarker_DistanceMM = numpy.linalg.norm(LineFromPrimaryMarkerToSecondaryMarker_NumpyArray)
                            LineFromPrimaryMarkerToSecondaryMarker_AngleWRTground = -1.0*numpy.rad2deg(numpy.arctan2(LineFromPrimaryMarkerToSecondaryMarker_NumpyArray[1], LineFromPrimaryMarkerToSecondaryMarker_NumpyArray[0]))

                        else:
                            pass
                            #print("ERROR: ArucoTag_DetectionTimeInMilliseconds_PrimaryMarker != ArucoTag_DetectionTimeInMilliseconds_SecondaryMarker, ArucoTag_DetectionTimeInMilliseconds_PrimaryMarker = " + str(ArucoTag_DetectionTimeInMilliseconds_PrimaryMarker) + ", ArucoTag_DetectionTimeInMilliseconds_SecondaryMarker = " + str(ArucoTag_DetectionTimeInMilliseconds_SecondaryMarker))
                    #################################################
                    '''

                ####################################################
                ####################################################

            except:
                exceptions = sys.exc_info()[0]
                print("while 1, ArucoTagDetectionFromCameraFeed_ReubenPython3ClassObject GET's, exceptions: %s" % exceptions)
                # traceback.print_exc()

        ####################################################
        ####################################################
        ####################################################

        #################################################### SET's
        ####################################################
        ####################################################
        if CSVdataLogger_OPEN_FLAG == 1:

            try:

                ####################################################
                ####################################################
                if 1:#ArucoTag_MarkerIDToDetect_PrimaryMarker in ArucoTag_MostRecentDict_DetectedArucoTag_InfoDict and ArucoTag_MarkerIDToDetect_SecondaryMarker in ArucoTag_MostRecentDict_DetectedArucoTag_InfoDict:
                    if 1: #(LineFromPrimaryMarkerToSecondaryMarker_DistanceMM < ArucoTag_DistanceBetweenPrimaryMarkerAndSecondaryMarker + ArucoTag_DistanceBetweenPrimaryMarkerAndSecondaryMarker_ClosenessThreshold) and (LineFromPrimaryMarkerToSecondaryMarker_DistanceMM > ArucoTag_DistanceBetweenPrimaryMarkerAndSecondaryMarker - ArucoTag_DistanceBetweenPrimaryMarkerAndSecondaryMarker_ClosenessThreshold):

                        CSVdataLogger_ReubenPython3ClassObject.AddDataToCSVfile_ExternalFunctionCall([ArucoTag_MostRecentDict_Time,
                                        ArucoTag_TranslationVectorOfMarkerCenter_PythonList_PrimaryMarker[0],
                                        ArucoTag_TranslationVectorOfMarkerCenter_PythonList_PrimaryMarker[1],
                                        ArucoTag_TranslationVectorOfMarkerCenter_PythonList_PrimaryMarker[2],
                                        ArucoTag_TranslationVectorOfMarkerCenter_PythonList_SecondaryMarker[0],
                                        ArucoTag_TranslationVectorOfMarkerCenter_PythonList_SecondaryMarker[1],
                                        ArucoTag_TranslationVectorOfMarkerCenter_PythonList_SecondaryMarker[2],
                                        LineFromPrimaryMarkerToSecondaryMarker_DistanceMM,
                                        LineFromPrimaryMarkerToSecondaryMarker_AngleWRTground])

                ####################################################
                ####################################################

            except:

                ####################################################
                ####################################################
                exceptions = sys.exc_info()[0]
                print("while 1, CSVdataLogger_ReubenPython3ClassObject SET's, exceptions: %s" % exceptions)
                # traceback.print_exc()
                ####################################################
                ####################################################

        ####################################################
        ####################################################
        ####################################################

        #################################################### SET's
        ####################################################
        ####################################################
        if UDPdataExchanger_OPEN_FLAG == 1:

            try:

                ####################################################
                ####################################################
                if UDPdataExchanger_UDP_RxOrTxRole == "tx":
                    DictToTx = dict([("PrimaryMarker", ArucoTag_TranslationVectorOfMarkerCenter_PythonList_PrimaryMarker),
                                                                              ("TestTime", CurrentTime_MainLoopThread)])

                    UDPdataExchanger_Object.SendDictFromExternalProgram(DictToTx)

                    if USE_PrintUDPdataForDebuggingFlag == 1:
                        print(str(DictToTx))

                ####################################################
                ####################################################

            except:

                ####################################################
                ####################################################
                exceptions = sys.exc_info()[0]
                print("while 1, UDPdataExchanger_Object SET's, exceptions: %s" % exceptions)
                # traceback.print_exc()
                ####################################################
                ####################################################

        ####################################################
        ####################################################
        ####################################################

        ####################################################
        ####################################################
        ####################################################
        if MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG == 1:

            try:

                ####################################################
                ####################################################
                MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject.GetMostRecentDataDict()

                if "StandAlonePlottingProcess_ReadyForWritingFlag" in MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict:
                    MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict["StandAlonePlottingProcess_ReadyForWritingFlag"]

                    if MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag == 1:
                        if CurrentTime_MainLoopThread - LastTime_MainLoopThread_MyPlotterPureTkinterStandAloneProcess >= MyPlotterPureTkinterStandAloneProcess_RefreshDurationInSeconds:

                            if ArucoTag_MarkerIDToDetect_PrimaryMarker in ArucoTag_MostRecentDict_DetectedArucoTag_InfoDict: #and ArucoTag_MarkerIDToDetect_SecondaryMarker in ArucoTag_MostRecentDict_DetectedArucoTag_InfoDict:
                                if 1:#(LineFromPrimaryMarkerToSecondaryMarker_DistanceMM < ArucoTag_DistanceBetweenPrimaryMarkerAndSecondaryMarker + ArucoTag_DistanceBetweenPrimaryMarkerAndSecondaryMarker_ClosenessThreshold) and (LineFromPrimaryMarkerToSecondaryMarker_DistanceMM > ArucoTag_DistanceBetweenPrimaryMarkerAndSecondaryMarker - ArucoTag_DistanceBetweenPrimaryMarkerAndSecondaryMarker_ClosenessThreshold):

                                    #'''
                                    MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject.ExternalAddPointOrListOfPointsToPlot(["Channel0", "Channel1", "Channel2"],
                                                                                                                                            [CurrentTime_MainLoopThread]*3,
                                                                                                                                            [ArucoTag_TranslationVectorOfMarkerCenter_PythonList_PrimaryMarker[0],
                                                                                                                                             ArucoTag_TranslationVectorOfMarkerCenter_PythonList_PrimaryMarker[1],
                                                                                                                                             ArucoTag_TranslationVectorOfMarkerCenter_PythonList_PrimaryMarker[2]])
                                    #'''

                                    '''
                                    MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject.ExternalAddPointOrListOfPointsToPlot(["Channel0", "Channel1", "Channel2"],
                                                                                                                                            [CurrentTime_MainLoopThread]*3,
                                                                                                                                            [ArucoTag_RotationVectorOfMarkerCenter_EulerAnglesXYZrollPitchYawInDegrees_PythonList_PrimaryMarker[0],
                                                                                                                                             ArucoTag_RotationVectorOfMarkerCenter_EulerAnglesXYZrollPitchYawInDegrees_PythonList_PrimaryMarker[1],
                                                                                                                                             ArucoTag_RotationVectorOfMarkerCenter_EulerAnglesXYZrollPitchYawInDegrees_PythonList_PrimaryMarker[2]])
                                    '''

                                    #MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject.ExternalAddPointOrListOfPointsToPlot(["Channel0", "Channel1"], [CurrentTime_MainLoopThread]*2, [LineFromPrimaryMarkerToSecondaryMarker_DistanceMM, LineFromPrimaryMarkerToSecondaryMarker_AngleWRTground])


                                    LastTime_MainLoopThread_MyPlotterPureTkinterStandAloneProcess = CurrentTime_MainLoopThread
                ####################################################
                ####################################################

            except:

                ####################################################
                ####################################################
                exceptions = sys.exc_info()[0]
                print("while 1, MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject SET's, exceptions: %s" % exceptions)
                # traceback.print_exc()
                ####################################################
                ####################################################

        ####################################################
        ####################################################
        ####################################################

        ArucoTag_DetectionTimeInMilliseconds_PrimaryMarker_Last = ArucoTag_DetectionTimeInMilliseconds_PrimaryMarker
        ArucoTag_DetectionTimeInMilliseconds_SecondaryMarker_Last = ArucoTag_DetectionTimeInMilliseconds_SecondaryMarker

        time.sleep(0.030)
    ####################################################
    ####################################################
    ####################################################
    ####################################################

    #################################################### THIS IS THE EXIT ROUTINE!
    ####################################################
    ####################################################
    ####################################################
    print("Exiting main program 'test_program_for_ArucoTagDetectionFromCameraFeed_ReubenPython3Class.py.")

    ####################################################
    if ArucoTag_OPEN_FLAG == 1:
        ArucoTagDetectionFromCameraFeed_ReubenPython3ClassObject.ExitProgram_Callback()
    ####################################################

    ####################################################
    if CSVdataLogger_OPEN_FLAG == 1:
        CSVdataLogger_ReubenPython3ClassObject.ExitProgram_Callback()
    ####################################################

    ####################################################
    if MyPrint_OPEN_FLAG == 1:
        MyPrint_ReubenPython2and3ClassObject.ExitProgram_Callback()
    ####################################################

    ####################################################
    if UDPdataExchanger_OPEN_FLAG == 1:
        UDPdataExchanger_Object.ExitProgram_Callback()
    ####################################################

    ####################################################
    if MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG == 1:
        MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject.ExitProgram_Callback()
    ####################################################

    ####################################################
    ####################################################
    ####################################################
    ####################################################

##########################################################################################################
##########################################################################################################