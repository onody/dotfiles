#!/bin/bash

DOT_FILES=(.zshrc .gitconfig .vimrc .vim .gemrc)

for file in ${DOT_FILES[@]}
do
    ln -s $HOME/src/dotfiles/$file $HOME/$file
done


