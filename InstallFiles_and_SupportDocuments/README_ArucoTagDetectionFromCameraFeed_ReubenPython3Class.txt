########################

ArucoTagDetectionFromCameraFeed_ReubenPython3Class

Code (including ability to hook to Tkinter GUI) that uses OpenCV to identify and localize an Aruco code (similar to a QR code) from a USB camera-stream (like a webcam).

Reuben Brewer, Ph.D.

reuben.brewer@gmail.com

www.reubotics.com

Apache 2 License

Software Revision F, 09/24/2023

Verified working on: 
Python 3.8, Windows 10 64-bit (no testing on Raspberry Pi or Mac testing yet)
########################  

########################### Python module installation instructions, all OS's

ArucoTagDetectionFromCameraFeed_ReubenPython3Class, ListOfModuleDependencies: ['CameraStreamerClass_ReubenPython2and3Class', 'cv2', 'future.builtins', 'LowPassFilter_ReubenPython2and3Class', 'LowPassFilterForDictsOfLists_ReubenPython2and3Class', 'numpy', 'scipy.spatial.transform']
ArucoTagDetectionFromCameraFeed_ReubenPython3Class, ListOfModuleDependencies_TestProgram: ['CSVdataLogger_ReubenPython3Class', 'MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class', 'MyPrint_ReubenPython2and3Class']
ArucoTagDetectionFromCameraFeed_ReubenPython3Class, ListOfModuleDependencies_NestedLayers: ['cv2', 'future.builtins', 'LowPassFilter_ReubenPython2and3Class', 'numpy', 'pexpect', 'psutil']
ArucoTagDetectionFromCameraFeed_ReubenPython3Class, ListOfModuleDependencies_All:['CameraStreamerClass_ReubenPython2and3Class', 'CSVdataLogger_ReubenPython3Class', 'cv2', 'future.builtins', 'LowPassFilter_ReubenPython2and3Class', 'LowPassFilterForDictsOfLists_ReubenPython2and3Class', 'MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class', 'MyPrint_ReubenPython2and3Class', 'numpy', 'pexpect', 'psutil', 'scipy.spatial.transform']

To install the cv2 Python module using pip:
pip install opencv-contrib-python==4.5.5.64

###########################

###########################
Example command line usage of 'ExcelPlot_CSVdataLogger_test_program_for_ArucoTagDetectionFromCameraFeed_ReubenPython3Class.py':

python "G:\My Drive\CodeReuben\ArucoTagDetectionFromCameraFeed_ReubenPython3Class\ExcelPlot_CSVdataLogger_test_program_for_ArucoTagDetectionFromCameraFeed_ReubenPython3Class.py" "G:\My Drive\CodeReuben\ArucoTagDetectionFromCameraFeed_ReubenPython3Class\SavedCSVfiles"
###########################