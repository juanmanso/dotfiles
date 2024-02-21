vim.g.mapleader = " " -- Set leader key to space

vim.opt.guicursor = "" -- To keep normal cursor in insert mode

vim.opt.number = true -- Show line numbers
vim.opt.relativenumber = true -- Show relative line numbers

vim.opt.tabstop = 4 -- Number of spaces tabs count for
vim.opt.softtabstop = 4 -- Number of spaces tabs count for while editing
vim.opt.shiftwidth = 4 -- Number of spaces to use for autoindent
vim.opt.expandtab = true -- Use spaces instead of tabs

vim.opt.smartindent = true -- Insert indents automatically

vim.opt.wrap = false -- Disable line wrap

vim.opt.swapfile = false -- Disable swap files
vim.opt.backup = false -- Disable backup files
vim.opt.undodir = os.getenv("HOME") .. "/.vim/undodir" -- Set undo directory
vim.opt.undofile = true -- Enable undo files

vim.opt.hlsearch = false -- Avoid highlight search results after search is done
vim.opt.incsearch = true -- Show search results as you type

vim.opt.termguicolors = true -- Enable 24-bit RGB colors

vim.opt.scrolloff = 8 -- Lines of context (above and below cursor) to keep visible
vim.opt.sidescrolloff = 8 -- Columns of context (left and right of cursor) to keep visible
-- vim.opt.signcolumn = "yes" -- Show sign column to keep consistency with diagnostics
vim.opt.isfname:append("@-@") -- Allow @ in filenames
vim.opt.colorcolumn = "80" -- Show vertical line at 80 characters

vim.opt.updatetime = 750 -- Faster completion (default is 4000 ms)

vim.opt.autoread = true -- Automatically reload files when they change outside vim

-- Set folding method to indent (use zc to close, zo to open, zr open a lvl,
--    zm close a lvl, zR open all, zM close all)
vim.opt.foldmethod = "indent" -- Enable folding based on indent
vim.opt.foldenable = false -- Disable folding by default on file open

vim.opt.list = true -- Show invisible characters
vim.opt.listchars = { tab = "▸ ", trail = "·", extends = "»", precedes = "«" } -- Set list characters

