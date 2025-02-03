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
import os
import sys
import traceback
import cv2
print("OpenCV version: " + str(cv2.__version__))
#########################################################

##########################################################################################################
##########################################################################################################
def OpenCVgetSupportedBackends():

    try:
        OpenCVsupportedBackendsDictWithEnglishNamesAsKeys = dict()
        OpenCVsupportedBackendsListOfIntegerCodes = cv2.videoio_registry.getBackends()

        for BackendIntegerCode in OpenCVsupportedBackendsListOfIntegerCodes:
            EnglishNameString = cv2.videoio_registry.getBackendName(BackendIntegerCode)
            OpenCVsupportedBackendsDictWithEnglishNamesAsKeys["CAP_" + EnglishNameString] = BackendIntegerCode

        OpenCVsupportedBackendsDictWithEnglishNamesAsKeys["CAP_ANY"] = cv2.CAP_ANY
        return OpenCVsupportedBackendsDictWithEnglishNamesAsKeys

    except:
        exceptions = sys.exc_info()[0]
        print("OpenCVgetSupportedBackends, Exceptions: %s" % exceptions)
        return dict()
        #traceback.print_exc()

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def GetCameraSettings(CVcapture, PrintForDebuggingFlag=0):
    CameraSettingDict = dict()

    try:
        CameraSettingDict["Autofocus"] = CVcapture.get(cv2.CAP_PROP_AUTOFOCUS)
        CameraSettingDict["Autoexposure"] = CVcapture.get(cv2.CAP_PROP_AUTO_EXPOSURE)
        CameraSettingDict["Exposure"] = CVcapture.get(cv2.CAP_PROP_EXPOSURE)
        CameraSettingDict["Gain"] = CVcapture.get(cv2.CAP_PROP_GAIN)
        CameraSettingDict["Brightness"] = CVcapture.get(cv2.CAP_PROP_BRIGHTNESS)
        CameraSettingDict["Contrast"] = CVcapture.get(cv2.CAP_PROP_CONTRAST)
        CameraSettingDict["Saturation"] = CVcapture.get(cv2.CAP_PROP_SATURATION)
        CameraSettingDict["Hue"] = CVcapture.get(cv2.CAP_PROP_HUE)

        if PrintForDebuggingFlag == 1:
            print("GetCameraSettings, CameraSettingDict: " + str(CameraSettingDict))

        return CameraSettingDict

    except:
        exceptions = sys.exc_info()[0]
        print("GetCameraSettings: Exceptions, %s" % exceptions)
        return CameraSettingDict
        # traceback.print_exc()
##########################################################################################################
##########################################################################################################


##########################################################################################################
##########################################################################################################
try:

    ##########################################################################################################
    OpenCVsupportedBackendsDictWithEnglishNamesAsKeys = OpenCVgetSupportedBackends()
    print("OpenCVsupportedBackendsDictWithEnglishNamesAsKeys: " + str(OpenCVsupportedBackendsDictWithEnglishNamesAsKeys))
    ##########################################################################################################

    ##########################################################################################################
    CameraNumberInteger = 0
    OpenCVbackendToUseEnglishName = "CAP_ANY"

    cv2.namedWindow("CameraPreviewWindow")
    CVcapture = cv2.VideoCapture(CameraNumberInteger, OpenCVsupportedBackendsDictWithEnglishNamesAsKeys[OpenCVbackendToUseEnglishName])
    ##########################################################################################################

    ##########################################################################################################
    GetCameraSettings(CVcapture, PrintForDebuggingFlag = 1)
    ##########################################################################################################

    ##########################################################################################################
    if CVcapture.isOpened(): # try to get the first frame
        image_capture_success_flag, original_captured_image_TEMP = CVcapture.read()
    else:
        image_capture_success_flag = False
    ##########################################################################################################

    ##########################################################################################################
    while image_capture_success_flag:
        cv2.imshow("CameraPreviewWindow", original_captured_image_TEMP)
        image_capture_success_flag, original_captured_image_TEMP = CVcapture.read()

        KeyboardPress = cv2.waitKey(20)

        ###################################################
        if KeyboardPress == 27: #ESC
            break
        ###################################################

    ##########################################################################################################

    ##########################################################################################################
    cv2.destroyWindow("CameraPreviewWindow")
    CVcapture.release()
    ##########################################################################################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
except:
    exceptions = sys.exc_info()[0]
    print("Exceptions: %s" % exceptions)
    traceback.print_exc()
##########################################################################################################
##########################################################################################################