#!/bin/sh
#IF THIS SCRIPT CAN'T BE FOUND OR RUN IN THE COMMAND TERMINAL, TYPE "dos2unix filename.sh" to remove ^M characters that are preenting it from running.

echo "StopAllPythonProcesses.sh running"

PythonVirtualEnvironmentFullPath="/home/pinis/VirtualEnvironment_SelfBalancingRobot1/bin/python3"
echo "PythonVirtualEnvironmentFullPath = $PythonVirtualEnvironmentFullPath"

sudo $PythonVirtualEnvironmentFullPath -u /home/pinis/Desktop/ArucoTagDetectionFromCameraFeed_PythonDeploymentFiles/GetPIDsByProcessEnglishNameAndOptionallyKill_ReubenPython2and3.py "python" "sigkill"
sudo $PythonVirtualEnvironmentFullPath -u /home/pinis/Desktop/ArucoTagDetectionFromCameraFeed_PythonDeploymentFiles/GetPIDsByProcessEnglishNameAndOptionallyKill_ReubenPython2and3.py "python3" "sigkill"

exit
