
" Include
if filereadable(expand('~/src/dotfiles/.vimrc.custom'))
	source ~/src/dotfiles/.vimrc.custom
endif

:filetype plugin indent off

" Solarized Colorscheme
syntax enable
set background=dark
colorscheme solarized

" visulaモードで選択してからのインデント調整で調整後に選択範囲を開放しない
vnoremap > >gv
vnoremap < <gv

