[[ -z $WAYLAND_DISPLAY && $(tty) = /dev/tty1 ]] && exec uwsm start start-hyprland
