"" All system-wide defaults are set in $VIMRUNTIME/debian.vim and sourced by
"" the call to :runtime you can find below.  If you wish to change any of those
"" settings, you should do it in this file (/etc/vim/vimrc), since debian.vim
"" will be overwritten everytime an upgrade of the vim packages is performed.
"" It is recommended to make changes after sourcing debian.vim since it alters
"" the value of the 'compatible' option.

"" This line should not be removed as it ensures that various options are
"" properly set to work with the Vim-related packages available in Debian.
""runtime! debian.vim

"" Uncomment the next line to make Vim more Vi-compatible
"" NOTE: debian.vim sets 'nocompatible'.  Setting 'compatible' changes numerous
"" options, so any other options should be set AFTER setting 'compatible'.
"set compatible

"" Vim5 and later versions support syntax highlighting. Uncommenting the next
"" line enables syntax highlighting by default.
if has("syntax")
  syntax on
endif

"" If using a dark background within the editing area and syntax highlighting
"" turn on this option as well
set background=dark

"" Uncomment the following to have Vim jump to the last position when
"" reopening a file
"if has("autocmd")
"  au BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g'\"" | endif
"endif

"" Uncomment the following to have Vim load indentation rules and plugins
"" according to the detected filetype.
if has("autocmd")
  filetype plugin indent on
endif

"" The following are commented out as they cause vim to behave a lot
"" differently from regular Vi. They are highly recommended though.
set showcmd		" Show (partial) command in status line.
set showmatch		" Show matching brackets.
"set ignorecase		" Do case insensitive matching
"set smartcase		" Do smart case matching
"set incsearch		" Incremental search
"set autowrite		" Automatically save before commands like :next and :make
"set hidden		" Hide buffers when they are abandoned
set mouse=a		" Enable mouse usage (all modes)

"" Source a global configuration file if available
if filereadable("/etc/vim/vimrc.local")
  source /etc/vim/vimrc.local
endif

"" Uncomment the following command for 256 colors
set t_Co=256

"" Set the colorscheme (may try it while on vim with 
"" :colo <name_of_color_scheme>
 colorscheme torte

"" Put line numbers in the margin. If want
"" referenced numbers uncomment the second one
set number
set numberwidth=5

"" Set UTF-8
set enc=utf-8
set fileencoding=utf-8

"" Toggle relative numbering, and set to absolute on loss of focus or insert
"" mode
"set rnu
"function! ToggleNumbersOn()
"	set nu!
"	set rnu
"endfunction
"function! ToggleRelativeOn()
"	set rnu!
"	set nu
"endfunction
" autocmd FocusLost * call ToggleRelativeOn()
" autocmd FocusGained * call ToggleRelativeOn()
" autocmd InsertEnter * call ToggleRelativeOn()
" autocmd InsertLeave * call ToggleRelativeOn()


"""" NOTES ON DEMO
""" SYSTEM CLIPBOARD COPY & PASTE SUPPORT
"set pastetoggle=<F2> "F2 before pasting to preserve indentation
""Copy paste to/from clipboard
"vnoremap <C-c> "*y
"map <silent><Leader>p :set paste<CR>o<esc>"*]p:set nopaste<cr>"
"map <silent><Leader><S-p> :set paste<CR>O<esc>"*]p:set nopaste<cr>"

"" Set syntax highlighting for specific file types
" autocmd BufRead,BufNewFile *.md set filetype=markdown

""Set default font in mac vim and gvim
""set cursorline    " highlight the current line
"set visualbell    " stop that ANNOYING beeping
"set wildmenu	" Display all matching files when we tab complete
"set wildmode=list:longest,full

"" Search down into subfolders
"" Provides tab-completion for all file-related tasks
"set path+=**

"" NOW WE CAN:
"" - Hit tab to :find by partial match
"" - Use * to make it fuzzy

"" THINGS TO CONSIDER:
"" - :b lets you autocomplete any open buffer





""" TAG JUMPING:

"" Create the `tags` file (may need to install ctags first)
command! MakeTags !ctags -R .

"" NOW WE CAN:
"" - Use ^] to jump to tag under cursor
"" - Use g^] for ambiguous tags
"" - Use ^t to jump back up the tag stack

"" THINGS TO CONSIDER:
"" - This doesn't help if you want a visual list of tags



""" AUTOCOMPLETE:

"" The good stuff is documented in |ins-completion|

"" HIGHLIGHTS:
"" - ^x^n for JUST this file
"" - ^x^f for filenames (works with our path trick!)
"" - ^x^] for tags only
"" - ^n for anything specified by the 'complete' option

"" NOW WE CAN:
"" - Use ^n and ^p to go back and forth in the suggestion list




""" FILE BROWSING:

"" Tweaks for browsing
"let g:netrw_banner=0        " disable annoying banner
"let g:netrw_browse_split=4  " open in prior window
let g:netrw_altv=1          " open splits to the right
let g:netrw_liststyle=3     " tree view
let g:netrw_list_hide=netrw_gitignore#Hide()
let g:netrw_list_hide.=',\(^\|\s\s\)\zs\.\S\+'

"" NOW WE CAN:
"" - :edit a folder to open a file browser
"" - <CR>/v/t to open in an h-split/v-split/tab
"" - check |netrw-browse-maps| for more mappings


""" SNIPPETS:

"" Read an empty HTML template and move cursor to title
"nnoremap ,html :-1read $HOME/.vim/.skeleton.html<CR>3jwf>a

"" NOW WE CAN:
"" - Take over the world!
""   (with much fewer keystrokes)

