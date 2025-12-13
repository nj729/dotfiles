
# # ex = EXtractor for all kinds of archives
# # usage: ex <file>
ex ()
{
  if [ -f $1 ] ; then
    case $1 in
      *.tar.bz2)   tar xjf $1   ;;
      *.tar.gz)    tar xzf $1   ;;
      *.bz2)       bunzip2 $1   ;;
      *.rar)       unrar x $1   ;;
      *.gz)        gunzip $1    ;;
      *.tar)       tar xf $1    ;;
      *.tbz2)      tar xjf $1   ;;
      *.tgz)       tar xzf $1   ;;
      *.zip)       unzip $1     ;;
      *.Z)         uncompress $1;;
      *.7z)        7z x $1      ;;
      *.deb)       ar x $1      ;;
      *.tar.xz)    tar xf $1    ;;
      *.tar.zst)   tar xf $1    ;;
      *)           echo "'$1' cannot be extracted via ex()" ;;
    esac
  else
    echo "'$1' is not a valid file"
  fi
}

# Zoxide cd wrapper
if command -v zoxide &> /dev/null; then
  zd() {
    if [ $# -eq 0 ]; then
      builtin cd ~ && return
    elif [ -d "$1" ]; then
      builtin cd "$1"
    else
      z "$@" && printf "\U000F17A9 " && pwd || echo "Error: Directory not found"
    fi
  }
  alias cd="zd"
fi

# Open files with xdg-open
open() {
  xdg-open "$@" >/dev/null 2>&1 &
}

# Neovim wrapper
n() {
  if [ "$#" -eq 0 ]; then
    nvim .
  else
    nvim "$@"
  fi
}

alias decompress="tar -xzf"


# yazi-cwd
function y() {
	local tmp="$(mktemp -t "yazi-cwd.XXXXXX")" cwd
	yazi "$@" --cwd-file="$tmp"
	IFS= read -r -d '' cwd < "$tmp"
	[ -n "$cwd" ] && [ "$cwd" != "$PWD" ] && builtin cd -- "$cwd"
	rm -f -- "$tmp"
}

# Transcode a video to a good-balance 1080p
transcode-video-1080p() {
  ffmpeg -i $1 -vf scale=1920:1080 -c:v libx264 -preset fast -crf 23 -c:a copy ${1%.*}-1080p.mp4
}

# Transcode a video to a good-balance 4K
transcode-video-4K() {
  ffmpeg -i $1 -c:v libx265 -preset slow -crf 24 -c:a aac -b:a 192k ${1%.*}-optimized.mp4
}

# Transcode any image to JPG
img2jpg() {
  magick $1 -quality 95 -strip ${1%.*}.jpg
}

# Transcode any image to small JPG
img2jpg-small() {
  magick $1 -resize 1080x\> -quality 95 -strip ${1%.*}.jpg
}

# Transcode any image to compressed PNG
img2png() {
  magick "$1" -strip -define png:compression-filter=5 \
    -define png:compression-level=9 \
    -define png:compression-strategy=1 \
    -define png:exclude-chunk=all \
    "${1%.*}.png"
}

# fzf integration
if command -v fzf &> /dev/null; then
  # Load fzf keybindings and completion
  if [[ -f /usr/share/fzf/key-bindings.zsh ]]; then
    source /usr/share/fzf/key-bindings.zsh
  fi
  if [[ -f /usr/share/fzf/completion.zsh ]]; then
    source /usr/share/fzf/completion.zsh
  fi

  # fzf file/directory search widget (Ctrl+F)
  fzf-file-widget() {
    local fd_cmd=$(command -v fdfind || command -v fd || echo "fd")
    local current_token="${LBUFFER##* }"
    # Remove leading/trailing quotes and expand variables, but don't add -- if empty
    local expanded_token=""
    if [[ -n "$current_token" ]]; then
      expanded_token=$(eval echo "$current_token" 2>/dev/null || echo "$current_token")
    fi
    
    local selected
    if [[ "$expanded_token" == */ ]] && [[ -d "$expanded_token" ]]; then
      # Search within specific directory
      selected=$($fd_cmd --color=always --base-directory="$expanded_token" 2>/dev/null | \
        fzf --multi --ansi --prompt="Directory $expanded_token> " \
          --preview="[[ -d $expanded_token{} ]] && ls -lah $expanded_token{} || bat --color=always --style=numbers $expanded_token{} 2>/dev/null || cat $expanded_token{}")
      [[ -n "$selected" ]] && selected="${expanded_token}${selected}"
    else
      # Search from current directory
      selected=$($fd_cmd --color=always 2>/dev/null | \
        fzf --multi --ansi --prompt="Directory> " --query="$expanded_token" \
          --preview="[[ -d {} ]] && ls -lah {} || bat --color=always --style=numbers {} 2>/dev/null || cat {}")
    fi

    if [[ -n "$selected" ]]; then
      # Escape spaces and special characters
      selected=$(printf '%q' "$selected")
      LBUFFER="${LBUFFER%$current_token}${selected} "
    fi
    zle reset-prompt
  }
  zle -N fzf-file-widget
  bindkey '^F' fzf-file-widget  # Ctrl+F

  # fzf git log search widget (Ctrl+L)
  fzf-git-log-widget() {
    if ! git rev-parse --git-dir >/dev/null 2>&1; then
      echo "Not in a git repository." >&2
      return 1
    fi

    local selected
    selected=$(git log --no-show-signature --color=always \
      --format='%C(bold blue)%h%C(reset) - %C(cyan)%ad%C(reset) %C(yellow)%d%C(reset) %C(normal)%s%C(reset)  %C(dim normal)[%an]%C(reset)' \
      --date=short | \
      fzf --ansi --multi --scheme=history --prompt="Git Log> " \
        --preview='git show --color=always --stat --patch {1}' \
        --preview-window=right:50%:wrap | \
      awk '{print $1}' | \
      xargs -I {} git rev-parse {} 2>/dev/null | \
      tr '\n' ' ')

    if [[ -n "$selected" ]]; then
      LBUFFER="${LBUFFER}${selected}"
    fi
    zle reset-prompt
  }
  zle -N fzf-git-log-widget
  bindkey '^L' fzf-git-log-widget  # Ctrl+L

  # fzf variables search widget (Ctrl+V)
  fzf-variables-widget() {
    local current_token="${LBUFFER##* }"
    local cleaned_token="${current_token#\$}"
    
    local selected
    selected=$(typeset -p | awk '{print $1, $2}' | sort -u | awk '{print $2}' | \
      fzf --multi --prompt="Variables> " --preview-window=wrap \
        --preview='echo {} && typeset -p {} 2>/dev/null || echo "No details available"' \
        --query="$cleaned_token")

    if [[ -n "$selected" ]]; then
      # If current token starts with $, keep the $
      if [[ "$current_token" == \$* ]]; then
        selected="\$${selected}"
      fi
      # Replace the current token
      LBUFFER="${LBUFFER%$current_token}${selected} "
    fi
    zle reset-prompt
  }
  zle -N fzf-variables-widget
  bindkey '^V' fzf-variables-widget  # Ctrl+V
fi

#One-Time Run (Fastfetch)
# Only run this if we are in an interactive shell (not a script)
if [[ -o interactive ]]; then
    if command -v fastfetch &> /dev/null; then
        fastfetch
    fi
fi
