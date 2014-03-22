
" Include
if filereadable(expand('~/src/dotfiles/.vimrc.custom'))
	source ~/src/dotfiles/.vimrc.custom
endif

:filetype plugin indent off

" Solarized Colorscheme
syntax enable
set background=dark
colorscheme solarized

