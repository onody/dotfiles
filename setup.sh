#!/bin/bash

DOT_FILES=(.tmux.conf .zshrc .zshrc.alias .zshrc.custom .oh-my-zsh .gitconfig .gitignore .vimrc .vim .gemrc .inputrc)

for file in ${DOT_FILES[@]}
do
    ln -s $HOME/src/dotfiles/$file $HOME/$file
done


