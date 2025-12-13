
#!/bin/bash

# Usage: volume-change-notify.sh <up|down|mute|micmute>
# Default sink (audio output) and source (microphone input)
SINK="@DEFAULT_SINK@"
SOURCE="@DEFAULT_SOURCE@"

# Volume adjustment amount (change as needed)
VOLUME_STEP=5%

# Persistent notification ID
NOTIFICATION_ID="volume_notification"

# Determine action
if [[ "$1" == "up" ]]; then
    # Increase volume
    pactl set-sink-volume $SINK +$VOLUME_STEP
    change="increased"
    icon="🔊" # Volume up icon
elif [[ "$1" == "down" ]]; then
    # Decrease volume
    pactl set-sink-volume $SINK -$VOLUME_STEP
    change="decreased"
    icon="🔉" # Volume down icon
elif [[ "$1" == "mute" ]]; then
    # Toggle speaker mute
    pactl set-sink-mute $SINK toggle
    is_muted=$(pactl get-sink-mute $SINK | grep -o "yes")

    if [[ "$is_muted" == "yes" ]]; then
        	notify-send -h string:x-canonical-private-synchronous:sys-notify "Volume Muted" "🔇 The volume is now muted"
        exit 0
    else
        	notify-send -h string:x-canonical-private-synchronous:sys-notify "Volume Unmuted" "🔊 The volume is now unmuted"
        exit 0
    fi
elif [[ "$1" == "micmute" ]]; then
    # Toggle microphone mute
    pactl set-source-mute $SOURCE toggle
    is_muted=$(pactl get-source-mute $SOURCE | grep -o "yes")

    if [[ "$is_muted" == "yes" ]]; then
        	notify-send -h string:x-canonical-private-synchronous:sys-notify "Microphone Muted" "🎙️ The microphone is now muted"
        exit 0
    else
        	notify-send -h string:x-canonical-private-synchronous:sys-notify "Microphone Unmuted" "🎙️ The microphone is now unmuted"
        exit 0
    fi
else
   notify-send -h string:x-canonical-private-synchronous:sys-notify "Volume Control Error" "Invalid argument: $1"
    exit 1
fi

# Get the updated volume level for speaker
current_volume=$(pactl get-sink-volume $SINK | grep -oP '\d{1,3}%' | head -1)

# Send a persistent notification using notify-send for volume changes
	notify-send -h string:x-canonical-private-synchronous:sys-notify "Volume $change" "$icon Current Volume: $current_volume"
