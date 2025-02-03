########################

ArucoTagDetectionFromCameraFeed_ReubenPython3Class

Code (including ability to hook to Tkinter GUI) that uses OpenCV to identify and localize an Aruco code (similar to a QR code) from a USB camera-stream (like a webcam).

Reuben Brewer, Ph.D.

reuben.brewer@gmail.com

www.reubotics.com

Apache 2 License

Software Revision G, 02/02/2025

Verified working on: 
Python 3.12, Windows 11 64-bit and Raspberry Pi Bullseye, Bookworm (Backend = "CAP_ANY", Camera = ELP USB).

########################  

########################### Python module installation instructions, all OS's

ArucoTagDetectionFromCameraFeed_ReubenPython3Class, ListOfModuleDependencies: ['CameraStreamerClass_ReubenPython2and3Class', 'cv2', 'future.builtins', 'LowPassFilter_ReubenPython2and3Class', 'LowPassFilterForDictsOfLists_ReubenPython2and3Class', 'numpy', 'scipy.spatial.transform']

ArucoTagDetectionFromCameraFeed_ReubenPython3Class, ListOfModuleDependencies_TestProgram: ['CSVdataLogger_ReubenPython3Class', 'MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class', 'MyPrint_ReubenPython2and3Class']

ArucoTagDetectionFromCameraFeed_ReubenPython3Class, ListOfModuleDependencies_NestedLayers: ['cv2', 'future.builtins', 'LowPassFilter_ReubenPython2and3Class', 'numpy', 'pexpect', 'psutil']

ArucoTagDetectionFromCameraFeed_ReubenPython3Class, ListOfModuleDependencies_All:['CameraStreamerClass_ReubenPython2and3Class', 'CSVdataLogger_ReubenPython3Class', 'cv2', 'future.builtins', 'LowPassFilter_ReubenPython2and3Class', 'LowPassFilterForDictsOfLists_ReubenPython2and3Class', 'MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class', 'MyPrint_ReubenPython2and3Class', 'numpy', 'pexpect', 'psutil', 'scipy.spatial.transform']

INCLUDE ALL OF THE OTHER INSTALLATION FOR DEPENDCIES!

pip install opencv-contrib-python==4.5.5.64

pip install numpy==1.26 #Does'nt work with numpy >= 2

pip install future

pip install scipy

pip install psutil

pip install pexpect

pip install keyboard

###########################

###########################

Example command line usage of 'ExcelPlot_CSVdataLogger_test_program_for_ArucoTagDetectionFromCameraFeed_ReubenPython3Class.py':

python "G:\My Drive\CodeReuben\ArucoTagDetectionFromCameraFeed_ReubenPython3Class\ExcelPlot_CSVdataLogger_test_program_for_ArucoTagDetectionFromCameraFeed_ReubenPython3Class.py" "G:\My Drive\CodeReuben\ArucoTagDetectionFromCameraFeed_ReubenPython3Class\SavedCSVfiles"

###########################