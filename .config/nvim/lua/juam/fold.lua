vim.cmd([[
  function! BlockFolds()
     let thisline = getline(v:lnum)
     if match(thisline, '^\"\"\ =') >= 0
        return ">1"
     else
        return "="
     endif
  endfunction
  ]])

-- vim.api.nvim_create_autocmd("BufRead", "~/.vim/vimrc", "setlocal foldmethod=expr", {once = true})
-- vim.api.nvim_create_autocmd("BufNewFile", "~/.vim/vimrc", "setlocal foldmethod=expr", {once = true})

-- vim.api.nvim_create_autocmd("BufRead", "~/.vim/vimrc", "setlocal foldexpr=BlockFolds()", {once = true})
-- vim.api.nvim_create_autocmd("BufNewFile", "~/.vim/vimrc", "setlocal foldexpr=BlockFolds()", {once = true})

-- vim.api.nvim_create_autocmd("BufRead", "~/.vim/vimrc", "setlocal foldtext=getline(v:foldstart+1)", {once = true})
-- vim.api.nvim_create_autocmd("BufNewFile", "~/.vim/vimrc", "setlocal foldtext=getline(v:foldstart+1)", {once = true})
