vim.keymap.set("n", "<leader>pv", vim.cmd.Ex) -- Jump to file tree

vim.keymap.set("v", "J", ":m '>+1<CR>gv=gv") -- Move selected lines down
vim.keymap.set("v", "K", ":m '<-2<CR>gv=gv") -- Move selected lines up

vim.keymap.set("n", "J", "mzJ`z") -- Appends the next line to the current line with a space keeping the cursor static
vim.keymap.set("n", "<C-d>", "<C-d>zz") -- Scroll down half a page with cursor in the middle
vim.keymap.set("n", "<C-u>", "<C-u>zz") -- Scroll up half a page with cursor in the middle
vim.keymap.set("n", "n", "nzzzv") -- Move down a search term while cursor in the middle
vim.keymap.set("n", "N", "Nzzzv") -- Move up a search term while cursor in the middle

vim.keymap.set("x", "<leader>p", [["_dP]]) -- Replace selected text without loosing previous buffer

-- Select the '+' buffer to copy and paste into system's clipboard
vim.keymap.set({ "n", "v" }, "<leader>y", [["+y]])
vim.keymap.set("n", "<leader>Y", [["+Y]])

vim.keymap.set({ "n", "v" }, "<leader>d", [["_d]]) -- Delete selected text without loosing previous buffer

vim.keymap.set("n", "Q", "<nop>") -- Disable Ex mode's hotkey
vim.keymap.set("n", "<C-f>", "<cmd>silent !tmux neww tmux-sessionizer<CR>") -- Let's us go back to previous projects on tmux
-- vim.keymap.set("n", "<leader>f", function()
--   vim.lsp.buf.format()
-- end) -- Format code
vim.keymap.set("n", "<leader>f", "<cmd>silent :Format<CR>")
vim.keymap.set("n", "<leader>F", "<cmd>silent :FormatWrite<CR>")

-- Quick Fix navigation
vim.keymap.set("n", "<C-k>", "<cmd>cnext<CR>zz")
vim.keymap.set("n", "<C-j>", "<cmd>cprev<CR>zz")
vim.keymap.set("n", "<leader>k", "<cmd>lnext<CR>zz")
vim.keymap.set("n", "<leader>j", "<cmd>lprev<CR>zz")

vim.keymap.set("n", "<leader>s", [[:s%s/\<<C-r><C-w>\>/<C-w>/gI<Left><Left><Left>]]) -- Replace the word the cursor was on (across the whole file)
vim.keymap.set("n", "<leader>x", "<cmd>!chmod +x %<CR>", { silent = true }) -- Make file executable
