-- This file can be loaded by calling `lua require('plugins')` from your init.vim

-- Only required if you have packer configured as `opt`
vim.cmd.packadd("packer.nvim")

return require("packer").startup(function(use)
  -- Packer can manage itself
  use({ "wbthomason/packer.nvim" })

  -- Telescope
  use({
    "nvim-telescope/telescope.nvim",
    tag = "0.1.0",
    -- or                            , branch = '0.1.x',
    requires = { { "nvim-lua/plenary.nvim" } },
  })

  -- Gruvbox Colortheme
  use({ "ellisonleao/gruvbox.nvim" })

  -- Treesitter
  use("nvim-treesitter/nvim-treesitter", { run = ":TSUpdate" })
  use({ "nvim-treesitter/playground" })

  -- Harpoon
  use({ "ThePrimeagen/harpoon" })

  -- Undo-tree
  use({ "mbbill/undotree" })

  -- Formatter
  use({ "mhartington/formatter.nvim" })

  -- LSP-Zero
  use({
    "VonHeikemen/lsp-zero.nvim",
    requires = {
      -- LSP Support
      { "neovim/nvim-lspconfig" },
      { "williamboman/mason.nvim" },
      { "williamboman/mason-lspconfig.nvim" },

      -- Autocompletion
      { "hrsh7th/nvim-cmp" },
      { "hrsh7th/cmp-buffer" },
      { "hrsh7th/cmp-path" },
      { "saadparwaiz1/cmp_luasnip" },
      { "hrsh7th/cmp-nvim-lsp" },
      { "hrsh7th/cmp-nvim-lua" },

      -- Snippets
      { "L3MON4D3/LuaSnip" },
      { "rafamadriz/friendly-snippets" },
    },
  })

  -- GitHub Copilot
  use({ "github/copilot.vim" })

  -- TPope Good Stuff
  use({ "tpope/vim-surround" })
  use({ "tpope/vim-commentary" })
  use({ "tpope/vim-repeat" })

  -- File Tree Explorer
  -- use {
  --     'nvim-tree/nvim-tree.lua',
  --     requires = {
  --         'nvim-tree/nvim-web-devicons', -- optional, for file icons
  --     },
  --     -- tag = 'nightly' -- optional, updated every week. (see issue #1193)
  -- }

  -- Statusline
  use({
    "nvim-lualine/lualine.nvim",
    requires = { "kyazdani42/nvim-web-devicons", opt = true },
  })

  -- Wakatime
  use({ "wakatime/vim-wakatime" })
end)
