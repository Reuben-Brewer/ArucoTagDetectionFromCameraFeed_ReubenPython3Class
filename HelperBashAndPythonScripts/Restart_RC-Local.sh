#!/bin/sh
echo "Running Restart_RC-Local.sh"
echo "sudo service rc.local stop"
sudo service rc.local stop
sleep 0.5
echo "sh sudo systemctl daemon-reload"
sudo systemctl daemon-reload
sleep 0.5
echo "sh sudo service rc.local start"
sudo service rc.local start
exit
