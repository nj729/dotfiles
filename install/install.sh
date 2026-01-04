#!/bin/sh


## Install Paru

# if pacman -Qi paru &> /dev/null; then
#   	tput setaf 1;echo "###### Paru is already installed"
# else
#     tput setaf 2;echo "###### Installing paru "
#     cd
#     sudo pacman -S --needed base-devel
#     git clone https://aur.archlinux.org/paru.git
#     cd paru
#     makepkg -si
#     tput setaf 4;echo "###### Paru Installed "
# fi


### Installing packages

func_install() {
	if paru -Qi $1 &> /dev/null; then
  		tput setaf 1;echo "################## The package "$1" is already installed"
	else
    	tput setaf 2;echo "##################  Installing package "  $1
	 paru -S --noconfirm --needed $1 
    fi
}

mapfile -t pkglist < pkgs

count=0

for name in "${pkglist[@]}" ; do
	count=$[count+1]
	tput setaf 3;echo "Installing package nr.  "$count " " $name;tput sgr0;
	func_install $name
done

