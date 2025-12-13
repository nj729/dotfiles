#!/bin/sh


## Install Paru

if pacman -Qi paru &> /dev/null; then
  	tput setaf 1;echo "###### Paru is already installed"
else
    tput setaf 2;echo "###### Installing paru "
    cd
    sudo pacman -S --needed base-devel
    git clone https://aur.archlinux.org/paru.git
    cd paru
    makepkg -si
    tput setaf 4;echo "###### Paru Installed "
fi


### Installing packages

func_install() {
	if paru -Qi $1 &> /dev/null; then
  		tput setaf 1;echo "################## The package "$1" is already installed"
	else
    	tput setaf 2;echo "##################  Installing package "  $1
	 paru -S --noconfirm --needed $1 
    fi
}


list=(
#amd-ucode
alsa-utils
alsa-plugins
alsa-lib
alsa-firmware
bat
bluetuibluez
bluez-libs
bluez-utils
brightnessctl
btop
#cliphist
elephant
evince
eza
fastfetch
fzf
git
grim
gstreamer
gst-plugins-good
gst-plugins-bad
gst-plugins-base
gst-plugins-ugly
gtk3
gtk4
gum
gvfs
gvfs-mtp
helium-browser-bin
hypridle
hyprland
hyprland-guiutils
hyprlock
hyprpicker
hyprsunset
intel-ucode
imagemagick
impala
imv
kitty
#lf
libnotify
librewolf-bin
#man-db
mako
mise
mpv
neovim
nvidia
nvidia-utils
#nwg-look
pamixer
pipewire
pipewire-alsa
pipewire-pulse
pipewire-jack
pipewire-zeroconf
playerctl
polkit-gnome
ripgrep
#rofi-wayland
satty
slurp
starship
stow
swaybg
swayosd-git
thunar
thunar-volman
tmux
ttf-nerd-fonts-symbols
ufw
unzip
uwsm
walker
waybar
wiremix
wl-clipboard
xdg-desktop-portal-gtk
xdg-desktop-portal-hyprland
xdg-terminal-exec
yaru-icon-theme
yazi
#zellij
zoxide
zsh
zsh-autosuggestions
zsh-syntax-highlighting
)

count=0

for name in "${list[@]}" ; do
	count=$[count+1]
	tput setaf 3;echo "Installing package nr.  "$count " " $name;tput sgr0;
	func_install $name
done

