#!/bin/sh

# Script to set the wallpaper using hyprpaper

# Location of the current wallpaper
WALLPAPER_LOCATION=~/.config/wallpapers/wallpaper.png

# Directory containing wallpapers (you can specify your directory here)
WALLPAPER_DIR=~/.config/wallpapers/

# Function to check if the file is an image
is_image() {
    local file="$1"
    if file --mime-type -b "$file" | grep -q '^image/'; then
        return 0  # true: it's an image
    else
        return 1  # false: not an image
    fi
}

# Function to set the wallpaper
set_wallpaper() {
    local image_file="$1"
    echo "Setting wallpaper to: $image_file"

    # Resize and set the wallpaper to 1920x1080 (Full HD)
    convert "$image_file" -resize 1920x1080 -gravity center -extent 1920x1080 "$WALLPAPER_LOCATION"

    # Restart hyprpaper to apply the wallpaper
    killall hyprpaper
    nohup hyprpaper >/dev/null 2>&1 &
}

# Function to set a random wallpaper from the directory
set_random_wallpaper() {
    # Find all image files in the wallpaper directory
    local random_image
    random_image=$(find "$WALLPAPER_DIR" -type f -iname "*.jpg" -o -iname "*.png" | shuf -n 1)

    if [ -z "$random_image" ]; then
        echo "No valid images found in the wallpaper directory."
        exit 1
    fi

    # Set the random wallpaper
    set_wallpaper "$random_image"
}

# Main script logic
if [ $# -gt 0 ]; then
    IMAGE_FILE="$1"

    if ! is_image "$IMAGE_FILE"; then
        echo "Error: Not a valid image file."
        exit 1
    fi

    # Set wallpaper from the provided file
    set_wallpaper "$IMAGE_FILE"
else
    # If no file is provided, set a random wallpaper from the directory
    set_random_wallpaper
fi
