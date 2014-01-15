

# alias		-------------------

alias ls="ls -la"
alias mv="mv -i"
alias cp="cp -i"
alias rm="rm -i"
alias ps="ps --sort=start_time"
alias rmr="rm -rf"
alias cl="clear"
alias tl="tail -f"


# history	-------------------

# 履歴ファイルの保存先
export HISTFILE=${HOME}/.zsh_history

# メモリに保存される履歴の件数
export HISTSIZE=100

# 履歴ファイルに保存される履歴の件数
export SAVEHIST=1000

# 重複を記録しない
setopt hist_ignore_dups

# 開始と終了を記録
setopt EXTENDED_HISTORY

