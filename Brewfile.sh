#!/bin/bash

ruby -e "$(curl -fsSL https://raw.github.com/Homebrew/homebrew/go/install)"

# Homebrewを最新版にアップデート
brew update

# Formulaを更新
brew upgrade

# パッケージのインストール
brew install zsh vim git tig cmake curl wget fontforge go nmap openssl rbenv rbenv-gem-rehash rbenv-gemset ruby-build rbenv-gemset brew-cask
brew install caskroom/cask/brew-cask

brew cask install google-chrome
brew cask install iterm2
brew cask install dropbox
brew cask install coteditor
brew cask install daisydisk
brew cask install evernote
brew cask install firefox
brew cask install nike-plus-connect
brew cask install sequel-pro
brew cask install sublime-text
brew cask install transmission
brew cask install virtualbox
brew cask install vagrant
brew cask install vlc
brew cask install monolingual
brew cask install the-unarchiver

# fontインストール
brew tap sanemat/font
brew install ricty
cp -f /usr/local/Cellar/ricty/3.2.2/share/fonts/Ricty*.ttf ~/Library/Fonts/
fc-cache -vf


