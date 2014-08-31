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
NeoBundle 'Shougo/neocomplcache'
NeoBundle 'Shougo/neosnippet'
NeoBundle 'Shougo/neosnippet-snippets'
NeoBundle 'jpalardy/vim-slime'
NeoBundle 'scrooloose/syntastic'
NeoBundle 'tomtom/tcomment_vim'

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
NeoBundle 'bronson/vim-trailing-whitespace'
NeoBundle 'nathanaelkane/vim-indent-guides'

" My Bundles here:
" Refer to |:NeoBundle-examples|.
" Note: You don't set neobundle setting in .gvimrc!

call neobundle#end()

" Required:
filetype plugin indent on

" If there are uninstalled bundles found on startup,
" this will conveniently prompt you to install them.
NeoBundleCheck
