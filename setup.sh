#!/bin/bash

DOT_FILES=(.zshrc .gitconfig .vimrc .vim .gemrc)

for file in ${DOT_FILES[@]}
do
    ln -s $HOME/src/dotfiles/$file $HOME/$file
done

mkdir -p ~/.vim/;
mkdir -p ~/.vim/bundle;
git clone https://github.com/Shougo/neobundle.vim ~/.vim/bundle/neobundle.vim

