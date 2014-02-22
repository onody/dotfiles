
" Include
if filereadable(expand('~/src/dotfiles/.vimrc.custom'))
	source ~/src/dotfiles/.vimrc.custom
endif

" NeoBundle
if has('vim_starting')
	set nocompatible
	set runtimepath+=~/.vim/bundle/neobundle.vim/
endif

call neobundle#rc(expand('~/.vim/bundle/'))

NeoBundleFetch 'Shougo/neobundle.vim'

NeoBundle 'itchyny/lightline.vim'
NeoBundle 'altercation/vim-colors-solarized'

filetype plugin indent on
NeoBundleCheck


" Solarized
syntax enable
set background=dark
colorscheme solarized

" lightline
set laststatus=2
let g:lightline = {
      \ 'colorscheme': 'solarized'
      \ }




