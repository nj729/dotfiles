#!/bin/bash

# Get the status of Caps Lock and Num Lock using xset
caps_state=$(xset q | grep "Caps Lock" | awk '{print $4}')
num_state=$(xset q | grep "Num Lock" | awk '{print $8}')

# Check for Caps Lock status
if [[ "$caps_state" == "on" ]]; then
    notify-send "Caps Lock Status" "🟢 Caps Lock is ON"
else
    notify-send "Caps Lock Status" "⚪ Caps Lock is OFF"
fi

# Check for Num Lock status
if [[ "$num_state" == "on" ]]; then
    notify-send "Num Lock Status" "🔢 Num Lock is ON"
else
    notify-send "Num Lock Status" "⚪ Num Lock is OFF"
fi
