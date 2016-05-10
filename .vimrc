" Plug
call plug#begin('~/.vim/plugged')
Plug 'airblade/vim-gitgutter'
Plug 'Shougo/neocomplcache'
Plug 'Shougo/neosnippet.vim'
Plug 'Shougo/neosnippet-snippets'
Plug 'itchyny/lightline.vim'
Plug 'tpope/vim-rails'
Plug 'vim-scripts/ruby-matchit'
Plug 'tpope/vim-endwise'
Plug 'scrooloose/syntastic'
Plug 'junegunn/vim-easy-align'
Plug 'Yggdroot/indentLine'
Plug 'fatih/vim-go'
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

" Plugin key-mappings.
imap <C-k> <Plug>(neosnippet_expand_or_jump)
smap <C-k> <Plug>(neosnippet_expand_or_jump)
xmap <C-k> <Plug>(neosnippet_expand_target)
 
" SuperTab like snippets behavior.
imap <expr><TAB> neosnippet#expandable_or_jumpable() ?
      \ "\<Plug>(neosnippet_expand_or_jump)"
      \: pumvisible() ? "\<C-n>" : "\<TAB>"
smap <expr><TAB> neosnippet#expandable_or_jumpable() ?
      \ "\<Plug>(neosnippet_expand_or_jump)"
      \: "\<TAB>"
 
" For snippet_complete marker.
if has('conceal')
  set conceallevel=2 concealcursor=i
endif

" easy align
xmap ga <Plug>(EasyAlign)
nmap ga <Plug>(EasyAlign)

" lightline.vim
set laststatus=2

" indentLine
let g:indentLine_color_term = 239
let g:indentLine_char = '›'

"全角スペースをハイライト表示
function! ZenkakuSpace()
  highlight ZenkakuSpace cterm=reverse ctermfg=DarkMagenta gui=reverse guifg=DarkMagenta
endfunction
if has('syntax')
  augroup ZenkakuSpace
    autocmd!
    autocmd ColorScheme       * call ZenkakuSpace()
    autocmd VimEnter,WinEnter * match ZenkakuSpace /　/
  augroup END
  call ZenkakuSpace()
endif
