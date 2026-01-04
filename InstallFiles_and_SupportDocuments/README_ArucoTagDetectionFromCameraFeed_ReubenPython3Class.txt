########################

ArucoTagDetectionFromCameraFeed_ReubenPython3Class

Code (including ability to hook to Tkinter GUI) that uses OpenCV to identify and localize an Aruco code (similar to a QR code) from a USB camera-stream (like a webcam).

Reuben Brewer, Ph.D.

reuben.brewer@gmail.com

www.reubotics.com

Apache 2 License

Software Revision H, 01/02/2026

Verified working on: Python 3.12/13 for Windows 10/11 64-bit (Backend = "CAP_DSHOW") and Raspberry Pi Bullseye (Backend = "CAP_ANY").

########################  

########################### Python module installation instructions, all OS's

ArucoTagDetectionFromCameraFeed_ReubenPython3Class, ListOfModuleDependencies: ['CameraStreamerClass_ReubenPython2and3Class', 'cv2', 'LowPassFilter_ReubenPython2and3Class', 'LowPassFilterForDictsOfLists_ReubenPython2and3Class', 'numpy', 'ReubenGithubCodeModulePaths', 'scipy.spatial.transform']

ArucoTagDetectionFromCameraFeed_ReubenPython3Class, ListOfModuleDependencies_TestProgram: ['CSVdataLogger_ReubenPython3Class', 'keyboard', 'MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class', 'numpy', 'ReubenGithubCodeModulePaths', 'UDPdataExchanger_ReubenPython3Class']

ArucoTagDetectionFromCameraFeed_ReubenPython3Class, ListOfModuleDependencies_NestedLayers: ['cv2', 'EntryListWithBlinking_ReubenPython2and3Class', 'GetCPUandMemoryUsageOfProcessByPID_ReubenPython3Class', 'LowPassFilterForDictsOfLists_ReubenPython2and3Class', 'numpy', 'pexpect', 'psutil', 'pyautogui', 'ReubenGithubCodeModulePaths']

ArucoTagDetectionFromCameraFeed_ReubenPython3Class, ListOfModuleDependencies_All:['CameraStreamerClass_ReubenPython2and3Class', 'CSVdataLogger_ReubenPython3Class', 'cv2', 'EntryListWithBlinking_ReubenPython2and3Class', 'GetCPUandMemoryUsageOfProcessByPID_ReubenPython3Class', 'keyboard', 'LowPassFilter_ReubenPython2and3Class', 'LowPassFilterForDictsOfLists_ReubenPython2and3Class', 'MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class', 'numpy', 'pexpect', 'psutil', 'pyautogui', 'ReubenGithubCodeModulePaths', 'scipy.spatial.transform', 'UDPdataExchanger_ReubenPython3Class']

pip install opencv-contrib-python==4.12.0.88

pip install numpy==2.2.6

pip install future

pip install scipy==1.16.3

pip install psutil

pip install pexpect

pip install keyboard

###########################

###########################

Example command line usage of 'ExcelPlot_CSVdataLogger_test_program_for_ArucoTagDetectionFromCameraFeed_ReubenPython3Class.py':

python "G:\My Drive\CodeReuben\ArucoTagDetectionFromCameraFeed_ReubenPython3Class\ExcelPlot_CSVdataLogger_test_program_for_ArucoTagDetectionFromCameraFeed_ReubenPython3Class.py" "G:\My Drive\CodeReuben\ArucoTagDetectionFromCameraFeed_ReubenPython3Class\SavedCSVfiles"

###########################