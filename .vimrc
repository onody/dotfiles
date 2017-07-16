" Plug
call plug#begin('~/.vim/plugged')
Plug 'airblade/vim-gitgutter'
Plug 'Shougo/unite.vim'
call plug#end()

" filetype設定
filetype on
filetype plugin on
filetype indent on

" 色味
set t_Co=256
set background=dark
let g:hybrid_use_iTerm_colors = 1
colorscheme hybrid
syntax on

" ペースト
set pastetoggle=<F12>
set clipboard=unnamed,unnamedplus,autoselect

" 文字コード
set encoding=utf-8
set fileencodings=utf-8,iso-2022-jp,euc-jp,sjis
set fileformats=unix,dos,mac

" 変なファイルはくのを辞める
set noundofile
set nobackup

" インデントはスペース2つ
set tabstop=2
set autoindent
set expandtab
set shiftwidth=2

" カレント行ハイライト
set cursorline
" アンダーラインを引く(color terminal)
highlight CursorLine cterm=underline ctermfg=NONE ctermbg=NONE
" アンダーラインを引く(gui)
highlight CursorLine gui=underline guifg=NONE guibg=NONE

" マウス対応
set mouse=a
set ttymouse=xterm2

" 勝手なコメントアウトを防止
autocmd FileType * setlocal formatoptions-=ro

" vim-gitgutter
set updatetime=250

