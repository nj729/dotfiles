#!/usr/bin/env bash 

#picom
picom --config /home/rude/.config/qtile/picom.conf -b &

function run {
  if ! pgrep -x $(basename $1 | head -c 15) 1>/dev/null;
  then
    $@&
  fi
}

#Some ways to set your wallpaper besides variety or nitrogen
feh --bg-fill /home/rude/0109.jpg &

#start sxhkd to replace Qtile native key-bindings
#run sxhkd -c ~/.config/qtile/sxhkd/sxhkdrc &

#starting utility applications at boot time
nm-applet &
blueman-applet &
#starting user applications at boot time
run alacritty
