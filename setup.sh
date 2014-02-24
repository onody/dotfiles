#!/bin/bash

DOT_FILES=(.tmux.conf .zshrc .oh-my-zsh .gitconfig .gitignore .vimrc .vim)

for file in ${DOT_FILES[@]}
do
    ln -s $HOME/src/dotfiles/$file $HOME/$file
done


