#!/bin/bash

update-desktop-database ~/.local/share/applications

# Images → imv
xdg-mime default imv.desktop image/png
xdg-mime default imv.desktop image/jpeg
xdg-mime default imv.desktop image/gif
xdg-mime default imv.desktop image/webp
xdg-mime default imv.desktop image/bmp
xdg-mime default imv.desktop image/tiff
xdg-mime default imv.desktop image/svg+xml

# PDFs → Evince
xdg-mime default org.gnome.Evince.desktop application/pdf

# Browser → Helium
xdg-mime default helium-browser.desktop x-scheme-handler/http
xdg-mime default helium-browser.desktop x-scheme-handler/https

# Videos → mpv
xdg-mime default mpv.desktop video/mp4
xdg-mime default mpv.desktop video/x-msvideo
xdg-mime default mpv.desktop video/x-matroska
xdg-mime default mpv.desktop video/x-flv
xdg-mime default mpv.desktop video/x-ms-wmv
xdg-mime default mpv.desktop video/mpeg
xdg-mime default mpv.desktop video/ogg
xdg-mime default mpv.desktop video/webm
xdg-mime default mpv.desktop video/quicktime
xdg-mime default mpv.desktop video/3gpp
xdg-mime default mpv.desktop video/3gpp2
xdg-mime default mpv.desktop video/x-ms-asf
xdg-mime default mpv.desktop video/x-ogm+ogg
xdg-mime default mpv.desktop video/x-theora+ogg
xdg-mime default mpv.desktop application/ogg

# Mail
xdg-mime default helium-google.desktop x-scheme-handler/mailto

# Text / code → Neovim
xdg-mime default nvim.desktop text/plain
xdg-mime default nvim.desktop text/x-makefile
xdg-mime default nvim.desktop text/x-csrc
xdg-mime default nvim.desktop text/x-chdr
xdg-mime default nvim.desktop text/x-c++src
xdg-mime default nvim.desktop text/x-c++hdr
xdg-mime default nvim.desktop text/x-java
xdg-mime default nvim.desktop text/x-moc
xdg-mime default nvim.desktop text/x-pascal
xdg-mime default nvim.desktop text/x-tcl
xdg-mime default nvim.desktop text/x-tex
xdg-mime default nvim.desktop application/x-shellscript
xdg-mime default nvim.desktop application/xml
xdg-mime default nvim.desktop text/xml
