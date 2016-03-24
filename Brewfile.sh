#!/bin/bash

/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

# up-to-date
brew update
brew upgrade

# install packages
brew install zsh vim git tig cmake curl wget fontforge go nmap openssl rbenv rbenv-gem-rehash rbenv-gemset ruby-build rbenv-gemset
brew install caskroom/cask/brew-cask

# install Ricty font
brew tap sanemat/font
brew install --powerline --vim-powerline ricty
cp -f /usr/local/Cellar/ricty/3.2.2/share/fonts/Ricty*.ttf ~/Library/Fonts/
fc-cache -vf
