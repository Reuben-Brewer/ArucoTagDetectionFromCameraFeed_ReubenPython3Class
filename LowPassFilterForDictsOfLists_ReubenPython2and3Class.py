# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision I, 12/22/2025

Verified working on: 3.11/12/13 for Windows 10/11 64-bit, Ubuntu 20.04, and Raspberry Pi Bookworm (no Mac testing yet).
'''

__author__ = 'reuben.brewer'

#######################################################################################################################
#######################################################################################################################

###########################################################
import ReubenGithubCodeModulePaths #Replaces the need to have "ReubenGithubCodeModulePaths.pth" within "C:\Anaconda3\Lib\site-packages".
ReubenGithubCodeModulePaths.Enable()
###########################################################

###########################################################
import os
import sys
import time
import datetime
import math
import cmath
import ctypes
import collections
import numpy
import random
from random import randint
import inspect #To enable 'TellWhichFileWereIn'
import traceback
from copy import * #for deepcopy(dict)

###########################################################

#######################################################################################################################
#######################################################################################################################

class LowPassFilterForDictsOfLists_ReubenPython2and3Class():

    ##########################################################################################################
    ##########################################################################################################
    def __init__(self, SetupDict):

        print("#################### LowPassFilterForDictsOfLists_ReubenPython2and3Class __init__ starting. ####################")

        self.SetupDict = SetupDict

        #########################################################
        #########################################################
        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "DictOfVariableFilterSettings" in self.SetupDict:
            self.DictOfVariableFilterSettings = self.SetupDict["DictOfVariableFilterSettings"]

            '''
            #STILL NEED TO IMPLEMENT A CHECK OF ALL VALUES
            self.UseMedianFilterFlag = self.PassThrough0and1values_ExitProgramOtherwise("UseMedianFilterFlag", self.SetupDict["UseMedianFilterFlag"])
            self.UseExponentialSmoothingFilterFlag = self.PassThrough0and1values_ExitProgramOtherwise("UseExponentialSmoothingFilterFlag", self.SetupDict["UseExponentialSmoothingFilterFlag"])
            self.ExponentialSmoothingFilterLambda = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("ExponentialSmoothingFilterLambda", self.SetupDict["ExponentialSmoothingFilterLambda"], 0.0, 1.0)
            '''

        else:
            self.DictOfVariableFilterSettings = dict()

        print("LowPassFilterForDictsOfLists_ReubenPython2and3Class __init__: DictOfVariableFilterSettings: " + str(self.DictOfVariableFilterSettings))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.VariablesDict = dict()

        '''
        #DO NOT INITIALIZE self.VariablesDict HERE BECAUSE WE DON'T KNOW LengthOfList (THE VARIABLES BEING WRITTEN), UNLESS WE WANT TO PASS THAT INTO THE SETUP DICT.
        LengthOfList = len(self.DictOfVariableFilterSettings)
        StartingValueOfSignalList = [0.0] * 5
        for VariableNameString in self.DictOfVariableFilterSettings:
            self.VariablesDict[VariableNameString] = dict([("__SignalInRawHistoryList", list([StartingValueOfSignalList] * LengthOfList)),
                                                           ("__SignalOutFilteredHistoryList", list([StartingValueOfSignalList] * LengthOfList)),
                                                           ("Raw_MostRecentValuesList", [0.0] * LengthOfList),
                                                           ("Filtered_MostRecentValuesList", [0.0] * LengthOfList),
                                                           ("UseMedianFilterFlag", self.DictOfVariableFilterSettings[VariableNameString]["UseMedianFilterFlag"]),
                                                           ("UseExponentialSmoothingFilterFlag", self.DictOfVariableFilterSettings[VariableNameString]["UseExponentialSmoothingFilterFlag"]),
                                                           ("ExponentialSmoothingFilterLambda", self.DictOfVariableFilterSettings[VariableNameString]["ExponentialSmoothingFilterLambda"])])

        print("LowPassFilterForDictsOfLists_ReubenPython2and3Class __init__: VariablesDict: " + str(self.VariablesDict))
        '''
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
    def AddOrUpdateDictOfVariableFilterSettingsFromExternalProgram(self, NewDictOfVariableFilterSettings):

        for VariableNameString in NewDictOfVariableFilterSettings:
            if VariableNameString not in self.DictOfVariableFilterSettings:
                self.DictOfVariableFilterSettings[VariableNameString] = deepcopy(NewDictOfVariableFilterSettings[VariableNameString])
                #print("AddOrUpdateDictOfVariableFilterSettingsFromExternalProgram: VariableNameString " + VariableNameString + " was NOT found in self.DictOfVariableFilterSettings.")
            else:
                self.UpdateVariableFilterSettingsFromExternalProgram(VariableNameString,
                                                                     NewDictOfVariableFilterSettings[VariableNameString]["UseMedianFilterFlag"],
                                                                     NewDictOfVariableFilterSettings[VariableNameString]["UseExponentialSmoothingFilterFlag"],
                                                                     NewDictOfVariableFilterSettings[VariableNameString]["ExponentialSmoothingFilterLambda"])
                #print("AddOrUpdateDictOfVariableFilterSettingsFromExternalProgram: VariableNameString " + VariableNameString + " was found in self.DictOfVariableFilterSettings.")

        print("AddOrUpdateDictOfVariableFilterSettingsFromExternalProgram: NewDictOfVariableFilterSettings = " + str(NewDictOfVariableFilterSettings))
        print("AddOrUpdateDictOfVariableFilterSettingsFromExternalProgram: self.DictOfVariableFilterSettings =" + str(self.DictOfVariableFilterSettings))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateVariableFilterSettingsFromExternalProgram(self, VariableNameString, UseMedianFilterFlag, UseExponentialSmoothingFilterFlag, ExponentialSmoothingFilterLambda):

        try:
            if VariableNameString in self.DictOfVariableFilterSettings:

                if UseMedianFilterFlag not in [0, 1]:
                    print("UpdateVariableFilterSettingsFromExternalProgram: Error, UseMedianFilterFlag must be in [0, 1].")
                    return -1

                if UseExponentialSmoothingFilterFlag not in [0, 1]:
                    print("UpdateVariableFilterSettingsFromExternalProgram: Error, UseExponentialSmoothingFilterFlag must be in [0, 1].")
                    return -1

                ExponentialSmoothingFilterLambda_Limited = self.LimitNumber_FloatOutputOnly(0.0, 1.0, ExponentialSmoothingFilterLambda)

                self.DictOfVariableFilterSettings[VariableNameString]["UseMedianFilterFlag"] = UseMedianFilterFlag
                self.DictOfVariableFilterSettings[VariableNameString]["UseExponentialSmoothingFilterFlag"] = UseExponentialSmoothingFilterFlag
                self.DictOfVariableFilterSettings[VariableNameString]["ExponentialSmoothingFilterLambda"] = ExponentialSmoothingFilterLambda_Limited

                self.VariablesDict[VariableNameString]["UseMedianFilterFlag"] = UseMedianFilterFlag
                self.VariablesDict[VariableNameString]["UseExponentialSmoothingFilterFlag"] = UseExponentialSmoothingFilterFlag
                self.VariablesDict[VariableNameString]["ExponentialSmoothingFilterLambda"] = ExponentialSmoothingFilterLambda_Limited

                '''
                print("UpdateVariableFilterSettingsFromExternalProgram: Update successful for " + str(VariableNameString) + \
                      " with UseMedianFilterFlag = " + str(UseMedianFilterFlag) + \
                      ", UseExponentialSmoothingFilterFlag = " + str(UseExponentialSmoothingFilterFlag) + \
                      ", and ExponentialSmoothingFilterLambda = " + str(ExponentialSmoothingFilterLambda))
                '''

            else:
                print("UpdateVariableFilterSettingsFromExternalProgram: Error, " + str(VariableNameString) + " not a recognized variable.")
                return -1

            return 1

        except:
            exceptions = sys.exc_info()[0]
            print("UpdateVariableFilterSettingsFromExternalProgram for VariableNameString " + VariableNameString + ", exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SwapTwoNumbersBasedOnSize(self, j, k):  # swaps values of j and k if j > k

        x = j
        y = k
        if j > k:
            # print "SWAPPED " + str(j) + " and " + str(k)
            x = k
            y = j

        # print [x, y]
        return [x, y]
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ComputeMedian5point_BoseNelson(self, a0, a1, a2, a3, a4):  # calculate the median from 5 adjacent points
        '''Network for N=5, using Bose-Nelson Algorithm.
          SWAP(0, 1); SWAP(3, 4); SWAP(2, 4);
          SWAP(2, 3); SWAP(0, 3); SWAP(0, 2);
          SWAP(1, 4); SWAP(1, 3); SWAP(1, 2);
        '''

        x0 = a0
        x1 = a1
        x2 = a2
        x3 = a3
        x4 = a4

        [x0, x1] = self.SwapTwoNumbersBasedOnSize(x0, x1)  # 0,1
        [x3, x4] = self.SwapTwoNumbersBasedOnSize(x3, x4)
        [x2, x4] = self.SwapTwoNumbersBasedOnSize(x2, x4)
        [x2, x3] = self.SwapTwoNumbersBasedOnSize(x2, x3)  # 2,3
        [x0, x3] = self.SwapTwoNumbersBasedOnSize(x0, x3)
        [x0, x2] = self.SwapTwoNumbersBasedOnSize(x0, x2)
        [x1, x4] = self.SwapTwoNumbersBasedOnSize(x1, x4)  # 1,4
        [x1, x3] = self.SwapTwoNumbersBasedOnSize(x1, x3)
        [x1, x2] = self.SwapTwoNumbersBasedOnSize(x1, x2)

        MedianValue = x2

        return MedianValue
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def AddDataDictFromExternalProgram(self, DataDictOfNewPointsForMultipleVariables, PrintInfoForDebuggingFlag = 0):

        try:
            #print("AddDataDictFromExternalProgram: self.DataDictOfNewPointsForMultipleVariables = " + str(DataDictOfNewPointsForMultipleVariables))

            ##########################################################################################################
            ##########################################################################################################
            for VariableNameString in DataDictOfNewPointsForMultipleVariables:

                ##########################################################################################################
                if VariableNameString in self.DictOfVariableFilterSettings:

                    ###############################################
                    ###############################################
                    UpdatedValuesList = DataDictOfNewPointsForMultipleVariables[VariableNameString]
                    if isinstance(UpdatedValuesList, list) == 0:
                        UpdatedValuesList = [UpdatedValuesList]
                    ###############################################
                    ###############################################

                    ###############################################
                    ###############################################
                    if VariableNameString not in self.VariablesDict: #unicorn

                        ###############################################
                        LengthOfList = len(UpdatedValuesList)
                        StartingValueOfSignalList = [0.0]*5
                        self.VariablesDict[VariableNameString] = dict([("__SignalInRawHistoryList", list([StartingValueOfSignalList]*LengthOfList)),
                                                                       ("__SignalOutFilteredHistoryList", list([StartingValueOfSignalList]*LengthOfList)),
                                                                       ("Raw_MostRecentValuesList", [0.0]*LengthOfList),
                                                                       ("Filtered_MostRecentValuesList", [0.0]*LengthOfList),
                                                                       ("UseMedianFilterFlag", self.DictOfVariableFilterSettings[VariableNameString]["UseMedianFilterFlag"]),
                                                                       ("UseExponentialSmoothingFilterFlag", self.DictOfVariableFilterSettings[VariableNameString]["UseExponentialSmoothingFilterFlag"]),
                                                                       ("ExponentialSmoothingFilterLambda", self.DictOfVariableFilterSettings[VariableNameString]["ExponentialSmoothingFilterLambda"])])
                        ###############################################

                    ###############################################
                    ###############################################

                    ###############################################
                    ###############################################
                    else:
                        ###############################################
                        for Index, Value in enumerate(UpdatedValuesList):
                            self.UpdateOneVariableWithNewValue(VariableNameString, Index, Value, PrintInfoForDebuggingFlag)
                        ###############################################

                    ###############################################
                    ###############################################

                ##########################################################################################################

                ##########################################################################################################
                else:
                    print("AddDataDictFromExternalProgram, error: " + VariableNameString + " not in self.DictOfVariableFilterSettings")
                    return dict()
                ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            return deepcopy(self.VariablesDict)
            ##########################################################################################################
            ##########################################################################################################

        except:
            exceptions = sys.exc_info()[0]
            print("AddDataDictFromExternalProgram, exceptions: %s" % exceptions)
            traceback.print_exc()
            return dict()

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def UpdateOneVariableWithNewValue(self, VariableNameStr, ListIndex, NewValue, PrintInfoForDebuggingFlag = 0):

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            ##########################################################################################################
            NewValue = float(NewValue)
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            if PrintInfoForDebuggingFlag == 1:
                print("UpdateOneVariableWithNewValue: " + str(VariableNameStr) + ", ListIndex = " + ", NewValue = " + str(NewValue))
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            self.VariablesDict[VariableNameStr]["__SignalInRawHistoryList"][ListIndex] = list(numpy.roll(self.VariablesDict[VariableNameStr]["__SignalInRawHistoryList"][ListIndex], 1).tolist()) #MUST EXPLICITLY MAKE NEW LIST() FOR THIS TO WORK PROPERLY
            self.VariablesDict[VariableNameStr]["__SignalInRawHistoryList"][ListIndex][0] = NewValue  #Add the incoming data point
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            self.VariablesDict[VariableNameStr]["__SignalOutFilteredHistoryList"][ListIndex] = list(numpy.roll(self.VariablesDict[VariableNameStr]["__SignalOutFilteredHistoryList"][ListIndex], 1).tolist()) #MUST EXPLICITLY MAKE NEW LIST() FOR THIS TO WORK PROPERLY
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            # fmedian = median5(fval_prev4, fval_prev3, fval_prev2, fval_prev1, fval_new);
            MedianValue_BoseNelson = self.ComputeMedian5point_BoseNelson(self.VariablesDict[VariableNameStr]["__SignalInRawHistoryList"][ListIndex][4],
                                                                         self.VariablesDict[VariableNameStr]["__SignalInRawHistoryList"][ListIndex][3],
                                                                         self.VariablesDict[VariableNameStr]["__SignalInRawHistoryList"][ListIndex][2],
                                                                         self.VariablesDict[VariableNameStr]["__SignalInRawHistoryList"][ListIndex][1],
                                                                         self.VariablesDict[VariableNameStr]["__SignalInRawHistoryList"][ListIndex][0])

            #MedianValue_Numpy = numpy.median(self.__SignalInRawHistoryList) #MedianValue_Numpy is much slower than MedianValue_BoseNelson, so don't use this.
            #print str(MedianValue_BoseNelson - MedianValue_Numpy)

            if self.VariablesDict[VariableNameStr]["UseMedianFilterFlag"] == 1:
                self.VariablesDict[VariableNameStr]["__SignalOutFilteredHistoryList"][ListIndex][0] = MedianValue_BoseNelson
            else:
                self.VariablesDict[VariableNameStr]["__SignalOutFilteredHistoryList"][ListIndex][0] = NewValue
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            if self.VariablesDict[VariableNameStr]["UseExponentialSmoothingFilterFlag"] == 1:  #new_filtered_value = k * raw_sensor_value + (1 - k) * old_filtered_value
                self.VariablesDict[VariableNameStr]["__SignalOutFilteredHistoryList"][ListIndex][0] = self.VariablesDict[VariableNameStr]["ExponentialSmoothingFilterLambda"] * self.VariablesDict[VariableNameStr]["__SignalOutFilteredHistoryList"][ListIndex][0] + (1.0 - self.VariablesDict[VariableNameStr]["ExponentialSmoothingFilterLambda"]) * self.VariablesDict[VariableNameStr]["__SignalOutFilteredHistoryList"][ListIndex][1]
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            self.VariablesDict[VariableNameStr]["Raw_MostRecentValuesList"][ListIndex] = self.VariablesDict[VariableNameStr]["__SignalInRawHistoryList"][ListIndex][0]
            self.VariablesDict[VariableNameStr]["Filtered_MostRecentValuesList"][ListIndex] = self.VariablesDict[VariableNameStr]["__SignalOutFilteredHistoryList"][ListIndex][0]
            ##########################################################################################################
            ##########################################################################################################

            #print("VariableNameStr Lambda: " + VariableNameStr + " = " + str(self.VariablesDict[VariableNameStr]["ExponentialSmoothingFilterLambda"]))

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        except:
            exceptions = sys.exc_info()[0]
            print("UpdateOneVariableWithNewValue, exceptions: %s" % exceptions)
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
    def GetMostRecentDataDict(self):

        return deepcopy(self.VariablesDict.copy()) #deepcopy is required we're returning a dict of dicts.
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ExitProgram_Callback(self):

        print("Exiting all threads for LowPassFilterForDictsOfLists_ReubenPython2and3Class object")

        #Currently not doing anything else here.
    ##########################################################################################################
    ##########################################################################################################


