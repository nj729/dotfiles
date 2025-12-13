Clone this repository locally and enter the cloned folder:
```
git clone https://github.com/catppuccin/grub.git && cd grub
```
Copy all or selected theme from src folder to /usr/share/grub/themes/. E.g. to copy all themes use:
```
sudo cp -r src/* /usr/share/grub/themes/
```
Uncomment and edit following line in /etc/default/grub to your selected theme:
```
GRUB_THEME="/usr/share/grub/themes/catppuccin-macchiato-grub-theme/theme.txt"
```
Update grub:
```
sudo grub-mkconfig -o /boot/grub/grub.cfg
```
For Fedora:
```
sudo grub2-mkconfig -o /boot/grub2/grub.cfg
```

