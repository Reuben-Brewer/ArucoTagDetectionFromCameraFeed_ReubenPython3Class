#!/bin/sh
#IF THIS SCRIPT CAN'T BE FOUND OR RUN IN THE COMMAND TERMINAL, TYPE "dos2unix filename.sh" to remove ^M characters that are preenting it from running.

CurrentTimeVariable=`date +%s`
echo "CurrentTimeVariable in seconds = $CurrentTimeVariable"

LogFileFullPath="/home/pinis/Desktop/ArucoTagDetectionFromCameraFeed_PythonDeploymentFiles/LogFiles/ArucoTagDetectionFromCameraFeed_ExecutionLog_$CurrentTimeVariable.txt"
echo "LogFileFullPath = $LogFileFullPath"

PythonVirtualEnvironmentFullPath="/home/pinis/VirtualEnvironment_SelfBalancingRobot1/bin/python3"
echo "PythonVirtualEnvironmentFullPath = $PythonVirtualEnvironmentFullPath"

echo "Running Launch_ArucoTagDetectionFromCameraFeed_RCLOCAL.sh" | tee -a $LogFileFullPath

echo "Launch_ArucoTagDetectionFromCameraFeed_RCLOCAL.sh running GetPIDsByProcessEnglishNameAndOptionallyKill.py" | tee -a $LogFileFullPath
sudo $PythonVirtualEnvironmentFullPath -u /home/pinis/Desktop/ArucoTagDetectionFromCameraFeed_PythonDeploymentFiles/GetPIDsByProcessEnglishNameAndOptionallyKill_ReubenPython2and3.py "python" "sigkill" | tee -a $LogFileFullPath
sudo $PythonVirtualEnvironmentFullPath -u /home/pinis/Desktop/ArucoTagDetectionFromCameraFeed_PythonDeploymentFiles/GetPIDsByProcessEnglishNameAndOptionallyKill_ReubenPython2and3.py "python3" "sigkill" | tee -a $LogFileFullPath

echo "Launch_ArucoTagDetectionFromCameraFeed_RCLOCAL.sh running ArucoTagDetectionFromCameraFeed.py" | tee -a $LogFileFullPath
echo "########## NOTE THAT YOU CANNOT LAUNCH A TKINTER GUI FROM /ETC/RC.LOCAL ##########" | tee -a $LogFileFullPath
sudo $PythonVirtualEnvironmentFullPath -u /home/pinis/Desktop/ArucoTagDetectionFromCameraFeed_PythonDeploymentFiles/test_program_for_ArucoTagDetectionFromCameraFeed_ReubenPython3Class.py "SOFTWARE_LAUNCH_METHOD:RCLOCAL" | tee -a $LogFileFullPath

exit
