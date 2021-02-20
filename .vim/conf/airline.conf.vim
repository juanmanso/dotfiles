" Airline's plugin configuration file
set laststatus=2        " always show airline
set noshowmode          " don't show the current mode
                        " in the command bar [Already showed by Airline]

let g:airline#extensions#tabline#enabled = 0
let g:airline#extensions#tabline#left_alt_sep = '┃'
let g:airline#extensions#tabline#left_sep = '▌'
let g:airline#extensions#tabline#formatter = 'unique_tail_improved'
let g:airline#extensions#tabline#overflow_marker = '…'
let g:airline#extensions#ale#enabled = 1
let g:airline#extensions#tabline#show_tab_type = 0
let g:airline_section_z = '%p%% %v:%l/%L'
let g:airline_left_sep = ''
let g:airline_right_sep = ''
let g:airline_right_alt_sep = ''
let g:airline_powerline_fonts = 1
let g:airline_section_y = ''
let g:airline_skip_empty_sections = 1
let g:airline_detect_spelllang=1

" Set airline color to Luna-term if available
if filereadable(glob("~/.vim/plugged/vim-luna/colors/luna-term.vim"))
    let g:airline_theme = 'luna'
endif


