
set nocompatible              " be iMproved
filetype off                  " required!

set rtp+=~/.vim/vundle/
call vundle#rc()

" let Vundle manage Vundle
" required! 
Bundle 'gmarik/vundle'

" My bundles here:
"
" original repos on GitHub
Bundle 'vim-ruby/vim-ruby'
"Bundle 'css.vim'
Bundle 'php.vim'

" vim-scripts repos

" non-GitHub repos
Bundle 'https://github.com/altercation/vim-colors-solarized.git'
Bundle 'https://github.com/kana/vim-fakeclip.git'

" Git repos on your local machine (i.e. when working on your own plugin)


filetype plugin indent on     " required!


" Settings

" Color
syntax enable
set background=dark
colorscheme solarized

" Custom
if filereadable(expand('~/.vimrc.custom'))
	source ~/.vimrc.custom
endif


