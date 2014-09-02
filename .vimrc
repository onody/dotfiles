if has('vim_starting')
  set nocompatible
  set runtimepath+=~/.vim/bundle/neobundle.vim/
endif

" Required:
call neobundle#begin(expand('~/.vim/bundle/'))

" Let NeoBundle manage NeoBundle
" Required:
NeoBundleFetch 'Shougo/neobundle.vim'
NeoBundle 'Shougo/vimproc', {
	\ 'build' : {
	\ 'windows' : 'make -f make_mingw32.mak',
	\ 'cygwin' : 'make -f make_cygwin.mak',
	\ 'mac' : 'make -f make_mac.mak',
	\ 'unix' : 'make -f make_unix.mak',
	\ },
\ }

NeoBundle 'Shougo/vimshell'
NeoBundle 'Shougo/unite.vim'
NeoBundle 'jpalardy/vim-slime'
NeoBundle 'scrooloose/syntastic'
NeoBundle 'tomtom/tcomment_vim'

" スニペット
NeoBundle 'Shougo/neocomplcache'
NeoBundle 'Shougo/neosnippet'
NeoBundle 'Shougo/neosnippet-snippets'

" 色味
"set t_Co=256
syntax enable
colorscheme monokai

" Clipbord系
set clipboard=unnamed

" Rubyの設定
NeoBundle 'tpope/vim-rails'
NeoBundle 'vim-scripts/ruby-matchit'

" Twigの設定
NeoBundle 'evidens/vim-twig'

" HTMLの設定
NeoBundle 'othree/html5.vim'

" ファイル展開とかのやつ
NeoBundle 'Shougo/unite.vim'

" Markdown
NeoBundle 'plasticboy/vim-markdown'
NeoBundle 'kannokanno/previm'
NeoBundle 'tyru/open-browser.vim'


" 文字コード判定
:set encoding=utf-8
:set fileencodings=iso-2022-jp,utf-8,euc-jp,sjis
:set fileformats=unix,dos,mac

" 変なファイルはくのを辞める
:set noundofile
:set nobackup

" Vim Girl
NeoBundle 'thinca/vim-splash'

" スペースなど可視化
NeoBundle 'nathanaelkane/vim-indent-guides'
" Vim 起動時 vim-indent-guides を自動起動
let g:indent_guides_enable_on_vim_startup=1
" ガイドをスタートするインデントの量
let g:indent_guides_start_level=2
" 自動カラー無効
let g:indent_guides_auto_colors=0
" 奇数番目のインデントの色
autocmd VimEnter,Colorscheme * :hi IndentGuidesOdd  guibg=#444433 ctermbg=black
" 偶数番目のインデントの色
autocmd VimEnter,Colorscheme * :hi IndentGuidesEven guibg=#333344 ctermbg=darkgray
" ガイドの幅
let g:indent_guides_guide_size = 1
" インデントはスペース4つ
set tabstop=4
set autoindent
set expandtab
set shiftwidth=4


" My Bundles here:
" Refer to |:NeoBundle-examples|.
" Note: You don't set neobundle setting in .gvimrc!

call neobundle#end()

" Required:
filetype plugin indent on

" If there are uninstalled bundles found on startup,
" this will conveniently prompt you to install them.
NeoBundleCheck
