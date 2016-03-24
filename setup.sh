#!/bin/bash

DOT_FILES=(.zshrc .gitconfig .gitignore_global .vimrc .gemrc .atom)

for file in ${DOT_FILES[@]}
do
    ln -s $HOME/src/dotfiles/$file $HOME/$file
done
