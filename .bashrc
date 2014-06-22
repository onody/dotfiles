
#
# alias
#

alias ll='ls -AlFh --show-control-chars --color=auto'
alias ls='ls -CFal'
alias mv='mv -i'
alias rm='rm -i'
alias cp='cp -i'
alias sc='screen'
alias ps='ps --sort=start_time'


#
# history
#

# 重複履歴を無視
export HISTCONTROL=ignoredups

# 無視するコマンド
export HISTIGNORE="fg*:bg*:history*:ls*:pwd*"

# 時刻を追加
HISTTIMEFORMAT='%Y.%m.%d ';
export HISTTIMEFORMAT

