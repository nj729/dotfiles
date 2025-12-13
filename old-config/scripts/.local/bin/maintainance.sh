#!/bin/bash
# ---------------------------------------
# Define Functions:
# ---------------------------------------
#
#
handlerror () {
  clear
  set -uo pipefail
  trap 's=$?; echo "$0: Error on line "$LINENO": $BASH_COMMAND"; exit $s' ERR
}
#
#
#
failedsrvs () {
  clear
  systemctl --failed > /tmp/failedsrvs
  less /tmp/failedsrvs
  clear
  echo -e "\n"
  rm /tmp/failedsrvs
  clear
}
#
journalchk () {
  clear
  journalctl -p 3 -xb > /tmp/journalchk
  less /tmp/journalchk
  clear
  echo -e "\n"
  rm /tmp/journalchk
  clear
}
#
journalcln () {
  clear
  journalctl --vacuum-time=2weeks
  clear
  printf "\nJournal directory cleaned"
  sleep 2
  clear
}
#
sysupdate () {
  clear
  pacman -Syu
  clear
  paru -Syu
  clear
  printf "\nFull system upgrade finished"
  sleep 2
  clear
}
#
pkgsccache () {
  clear
  pacman -Scc
  clear
  printf "\nPackage cache cleaned"
  sleep 2
  clear
}
#
orphanchk () {
  clear
  pacman -Qtdq > /tmp/orphanchk
  less /tmp/orphanchk
  clear
  printf "\n"
  rm /tmp/orphanchk
  clear
}
#
orphancln () {
  clear
  pacman -Rns "$(pacman -Qtdq)"
  clear
  printf "\nOrphan packages cleaned"
  sleep 2
  clear
}
#
usercachecln () {
  clear
  read -p "Type your user name, be exact, and press Enter: " USERCACHE
  rm -rf "/home/$USERCACHE/.cache/*"
  clear
  printf "\nUser's cache directory cleaned"
  sleep 2
  clear
}
#
runreflector () {
  clear
  reflector --age 6 --latest 20 --protocol https --sort rate --save /etc/pacman.d/mirrorlist
  clear
  printf "\nMirrorlist regenerated"
  sleep 2
  clear
}
#
mainmenu () { while true
do
  clear
  echo "-------------------------------------"
  echo " Maintenance Script"
  echo "-------------------------------------"
  echo ""
  echo "  1) Failed systemd services"
  echo "  2) Check journal logs"
  echo "  3) Cleanup journal space"
  echo "  4) Run system update"
  echo "  5) Clean package cache"
  echo "  6) Check for orphan packages"
  echo "  7) Remove orphan packages"
  echo "  8) Cleanup user cache folder"
  echo "  9) Regenerate mirrorlist"
  echo ""
  echo "  X) Exit"
  echo -e "\n"
  read -p "Enter your choice: " option
  case $option in
    1 ) failedsrvs ;;
    2 ) journalchk ;;
    3 ) journalcln ;;
    4 ) sysupdate ;;
    5 ) pkgsccache ;;
    6 ) orphanchk ;;
    7 ) orphancln ;;
    8 ) usercachecln ;;
    9 ) runreflector ;;
    x|X ) exit;;
    * ) invalid ;;
  esac
done
}
#
#
ROOTUSER () {
  if [[ "$EUID" = 0 ]]; then
    return
  else
    echo "Please Run As Root"
    sleep 2
    exit
  fi
}
#
#
ROOTUSER
handlerror
mainmenu
