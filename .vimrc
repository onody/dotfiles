"NeoBundle Scripts-----------------------------
if &compatible
  set nocompatible               " Be iMproved
endif

" Required:
set runtimepath^=/Users/kohei.onodera/.vim/bundle/neobundle.vim/

" Required:
call neobundle#begin(expand('/Users/kohei.onodera/.vim/bundle'))

" Let NeoBundle manage NeoBundle
" Required:
NeoBundleFetch 'Shougo/neobundle.vim'

" Add or remove your Bundles here:
NeoBundle 'Shougo/neocomplcache'
NeoBundle 'Shougo/neosnippet.vim'
NeoBundle 'Shougo/neosnippet-snippets'
NeoBundle 'tpope/vim-fugitive'
NeoBundle 'ctrlpvim/ctrlp.vim'
NeoBundle 'flazz/vim-colorschemes'
NeoBundle 'itchyny/lightline.vim'
NeoBundle 'scrooloose/nerdtree'


" Rubyの設定
NeoBundle 'tpope/vim-rails'
NeoBundle 'vim-scripts/ruby-matchit'

" You can specify revision/branch/tag.
NeoBundle 'Shougo/vimshell', { 'rev' : '3787e5' }

" Required:
call neobundle#end()

" Required:
filetype plugin indent on

" If there are uninstalled bundles found on startup,
" this will conveniently prompt you to install them.
NeoBundleCheck
"End NeoBundle Scripts-------------------------

" 色味
" syntax enable
set background=dark
let g:hybrid_use_iTerm_colors = 1
colorscheme hybrid
syntax on

" Clipbord系
set clipboard=unnamed

set encoding=utf-8
set fileencodings=utf-8,iso-2022-jp,euc-jp,sjis
set fileformats=unix,dos,mac

" 変なファイルはくのを辞める
set noundofile
set nobackup

" インデントはスペース4つ
set tabstop=2
set autoindent
set expandtab
set shiftwidth=2

" keymap
nnoremap <silent><C-e> :NERDTreeToggle<CR>
