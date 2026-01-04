# sources
[ -f "$HOME/.config/zsh/aliases.zsh" ] && source "$HOME/.config/zsh/aliases.zsh"
[ -f "$HOME/.config/zsh/exports.zsh" ] && source "$HOME/.config/zsh/exports.zsh"
[ -f "$HOME/.config/zsh/functions.zsh" ] && source "$HOME/.config/zsh/functions.zsh"

# plugins
source /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh
source /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.plugin.zsh

# history setup
HISTFILE=$HOME/.zhistory
SAVEHIST=1000
HISTSIZE=999
setopt APPEND_HISTORY           # Append to history file
setopt SHARE_HISTORY            # Share history across sessions
setopt HIST_IGNORE_DUPS         # Ignore duplicate commands
setopt HIST_IGNORE_SPACE        # Ignore commands starting with space
setopt HIST_REDUCE_BLANKS       # Remove unnecessary blanks

# Ensure mise works (disable command hashing)
setopt NO_HASH_CMDS
setopt NO_HASH_DIRS

# completion using arrow keys (based on history)
bindkey '^[[A' history-search-backward
bindkey '^[[B' history-search-forward

# Zellij
#echo 'eval "$(zellij setup --generate-auto-start zsh)"' >> ~/.zshrc

if command -v mise &> /dev/null; then
  eval "$(mise activate zsh)"
fi

if command -v zoxide &> /dev/null; then
  eval "$(zoxide init zsh)"
fi

# if command -v try &> /dev/null; then
#   eval "$(try init ~/Work/tries)"
# fi

if command -v starship &> /dev/null; then
  eval "$(starship init zsh)"
fi

# tmux
if [ -z "$TMUX" ]; then
    # Attach to an existing session named 'default' or create a new one
    tmux attach-session -t default || tmux new-session -s default
fi

# Load and initialise completion system
autoload -Uz compinit
setopt PROMPT_SUBST
compinit
zstyle ':completion:*' menu select

