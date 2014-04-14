
" Include
if filereadable(expand('~/src/dotfiles/.vimrc.custom'))
	source ~/src/dotfiles/.vimrc.custom
endif

:filetype plugin indent off

" Solarized Colorscheme
"syntax enable
"set background=dark
"colorscheme solarized

" Molokai Colorscheme
colorscheme molokai
syntax on
let g:molokai_original = 1
let g:rehash256 = 1
set background=dark



" visulaモードで選択してからのインデント調整で調整後に選択範囲を開放しない
vnoremap > >gv
vnoremap < <gv

" ctrlp
set runtimepath^=~/.vim/bundle/ctrlp.vim

" nerdtree
set runtimepath^=~/.vim/bundle/nerdtree

" viのみで起動した場合はNERDTreeを実行する
let file_name = expand("%")
if has('vim_starting') &&  file_name == ""
    autocmd VimEnter * NERDTree ./
endif

