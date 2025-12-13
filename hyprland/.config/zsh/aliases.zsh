# prompt and verbose
alias cp='cp -iv'
alias mv='mv -iv'
alias rm='rm -iv'
alias cat='bat --style='numbers,changes,grid,auto,header,header-filename,header-filesize,snip''
alias bat='bat --style='numbers,changes,grid,auto,header,header-filename,header-filesize,snip''

#dev
alias vs='vscodium'

#list
alias ls='eza -lh --group-directories-first --icons=auto'
alias la='ls -a'
alias lt='eza --tree --level=2 --long --icons --git'
alias lta='lt -a'

#custom configs
#alias vim='nvim'
alias cfg="nvim ~/.config/"
alias nvc="nvim ~/.config/nvim/"
alias hc="nvim ~/.config/hypr/"
alias wbc="nvim ~/.config/waybar/"
alias eb="nvim ~/.local/share/bin/"

# pacman
alias pacman="sudo pacman --color auto"
alias update="sudo pacman -Syyu"

#zsh
alias sz='source ~/.zshrc'
alias zo='nvim ~/.zshrc'
alias za='nvim ~/.config/zsh/aliases.zsh'
alias zp='nvim ~/.config/zsh/prompt.zsh'

#cd
alias hd="cd ~/dotfiles/hyprland/"
alias cd="z"

#decompress
alias decompress="tar -xzf"

# exit
alias :q="exit"
