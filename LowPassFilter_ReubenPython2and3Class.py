# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision J, 11/10/2024

Verified working on: Python 2.7, 3.8 for Windows 8.1, 10 64-bit, Ubuntu 20.04, and Raspberry Pi Buster (no Mac testing yet).
'''

__author__ = 'reuben.brewer'

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
import statistics
###########################################################

class LowPassFilter_ReubenPython2and3Class():

    ##########################################################################################################
    ##########################################################################################################
    def __init__(self, setup_dict):

        print("#################### LowPassFilter_ReubenPython2and3Class __init__ starting. ####################")

        #########################################################
        #########################################################
        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.UpdateFilterParameters(setup_dict, StringPrefixToPrint="LowPassFilter_ReubenPython2and3Class __init__: ")
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.MostRecentDataDict = dict()
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
            print(self.TellWhichFileWereIn() + ", PassThrough0and1values_ExitProgramOtherwise Error. InputNumber '" + InputNameString + "' must be a numerical value, Exceptions: %s" % exceptions)

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

                print(self.TellWhichFileWereIn() + ", PassThrough0and1values_ExitProgramOtherwise Error. '" +
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
            print(self.TellWhichFileWereIn() + ", PassThrough0and1values_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)

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
            print(self.TellWhichFileWereIn() + ", PassThroughFloatValuesInRange_ExitProgramOtherwise Error. InputNumber '" + InputNameString + "' must be a float value, Exceptions: %s" % exceptions)
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
                print(self.TellWhichFileWereIn() + ", PassThroughFloatValuesInRange_ExitProgramOtherwise Error. '" +
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
            print(self.TellWhichFileWereIn() + ", PassThroughFloatValuesInRange_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)
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
    def AddDataPointFromExternalProgram(self, NewDataPoint):

        try:
            ##########################################################################################################
            NewDataPoint = float(NewDataPoint)

            self.SignalInRaw = list(numpy.roll(self.SignalInRaw, 1)) #MUST EXPLICITLY MAKE NEW LIST() FOR THIS TO WORK PROPERLY
            self.SignalInRaw[0] = NewDataPoint  #Add the incoming data point

            self.SignalOutSmoothed = list(numpy.roll(self.SignalOutSmoothed, 1)) #MUST EXPLICITLY MAKE NEW LIST() FOR THIS TO WORK PROPERLY
            ##########################################################################################################

            ##########################################################################################################
            #MedianValue = self.ComputeMedian5point_BoseNelson(self.SignalInRaw[4], self.SignalInRaw[3], self.SignalInRaw[2], self.SignalInRaw[1], self.SignalInRaw[0]) #Must do this evaluation BEFORE putting it in the real signal.
            MedianValue = statistics.median(self.SignalInRaw)

            if self.UseMedianFilterFlag == 1:
                self.SignalOutSmoothed[0] = MedianValue
                #print("self.SignalInRaw len: " + str(len(self.SignalInRaw)))
            else:
                self.SignalOutSmoothed[0] = NewDataPoint
            ##########################################################################################################

            ##########################################################################################################
            if self.UseExponentialSmoothingFilterFlag == 1: #FORMER ERROR: THIS USED TO WORK ON self.SignalInRaw[0] INSTEAD OF self.SignalOutSmoothed[0], SO IT ERASED MEDIAN FILTER
                self.SignalOutSmoothed[0] = self.ExponentialSmoothingFilterLambda * self.SignalOutSmoothed[0] + (1.0 - self.ExponentialSmoothingFilterLambda) * self.SignalOutSmoothed[1]
            ##########################################################################################################

            ##########################################################################################################
            self.MostRecentDataDict = dict([("SignalInRaw", self.SignalInRaw[0]),
                                           ("SignalOutSmoothed", self.SignalOutSmoothed[0]),
                                           ("UseMedianFilterFlag", self.UseMedianFilterFlag),
                                           ("MedianFilterKernelSize", self.MedianFilterKernelSize),
                                           ("UseExponentialSmoothingFilterFlag", self.UseExponentialSmoothingFilterFlag),
                                           ("ExponentialSmoothingFilterLambda", self.ExponentialSmoothingFilterLambda),
                                           ("DataStreamingFrequency", -11111.0)]) #For backwards-compatibility, remove this later after we've updated our code.

            return self.MostRecentDataDict
            ##########################################################################################################

        except:
            exceptions = sys.exc_info()[0]
            print("AddDataPointFromExternalProgram: Exceptions: %s" % exceptions)
            traceback.print_exc()
            return dict()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GetMostRecentDataDict(self):

        #deepcopy is not required as MostRecentDataDict only contains numbers (no lists, dicts, etc. that go beyond 1-level).
        return self.MostRecentDataDict.copy()
    ##########################################################################################################
    ##########################################################################################################
    
    ##########################################################################################################
    ##########################################################################################################
    def UpdateFilterParameters(self, setup_dict, StringPrefixToPrint = ""):

        ##########################################################
        #########################################################
        if "UseMedianFilterFlag" in setup_dict:
            self.UseMedianFilterFlag = self.PassThrough0and1values_ExitProgramOtherwise("UseMedianFilterFlag", setup_dict["UseMedianFilterFlag"])
        else:
            self.UseMedianFilterFlag = 1

        if StringPrefixToPrint != "":
            print(StringPrefixToPrint + "UseMedianFilterFlag: " + str(self.UseMedianFilterFlag))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "MedianFilterKernelSize" in setup_dict:
            self.MedianFilterKernelSize = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("MedianFilterKernelSize", setup_dict["MedianFilterKernelSize"], 3.0, 100.0))

        else:
            self.MedianFilterKernelSize = 5

        if StringPrefixToPrint != "":
            print(StringPrefixToPrint + "MedianFilterKernelSize: " + str(self.MedianFilterKernelSize))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "UseExponentialSmoothingFilterFlag" in setup_dict:
            self.UseExponentialSmoothingFilterFlag = self.PassThrough0and1values_ExitProgramOtherwise("UseExponentialSmoothingFilterFlag", setup_dict["UseExponentialSmoothingFilterFlag"])
        else:
            self.UseExponentialSmoothingFilterFlag = 1

        if StringPrefixToPrint != "":
            print(StringPrefixToPrint + "UseExponentialSmoothingFilterFlag: " + str(self.UseExponentialSmoothingFilterFlag))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "ExponentialSmoothingFilterLambda" in setup_dict:
            self.ExponentialSmoothingFilterLambda = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("ExponentialSmoothingFilterLambda", setup_dict["ExponentialSmoothingFilterLambda"], 0.0, 1.0)

        else:
            self.ExponentialSmoothingFilterLambda = 0.005

        if StringPrefixToPrint != "":
            print(StringPrefixToPrint + "ExponentialSmoothingFilterLambda: " + str(self.ExponentialSmoothingFilterLambda))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.SignalInRaw = [0.0]*self.MedianFilterKernelSize
        self.SignalOutSmoothed = [0.0]*self.MedianFilterKernelSize
        #########################################################
        #########################################################

    ##########################################################################################################
    ##########################################################################################################


