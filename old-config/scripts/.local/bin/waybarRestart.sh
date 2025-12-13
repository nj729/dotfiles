#!/usr/bin/bash

#Restart Waybar and swaync

killall waybar
killall swaync
waybar &
swaync &
notify-send --app-name=HOME "Waybar and SwayNc Resarted"
