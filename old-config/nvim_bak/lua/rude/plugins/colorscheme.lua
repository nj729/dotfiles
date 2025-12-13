return {
	"rose-pine/neovim",
	name = "rose-pine",
	config = function()
		local rose_pine = require("rose-pine")
		rose_pine.setup({
			variant = "main",
			dark_variant = "main",
			bold_vert_split = false,
			dim_nc_background = false,
			disable_background = true,
			disable_float_background = true,
			disable_italics = true,

			groups = {
				background = "base",
				background_nc = "_experimental_nc",
				panel = "surface",
				panel_nc = "base",
				border = "highlight_med",
				comment = "muted",
				link = "iris",
				punctuation = "subtle",

				error = "love",
				hint = "iris",
				info = "foam",
				warn = "gold",

				headings = {
					h1 = "iris",
					h2 = "foam",
					h3 = "rose",
					h4 = "gold",
					h5 = "pine",
					h6 = "foam",
				},
			},

			highlight_groups = {
				ColorColumn = { bg = "rose" },
				CursorLine = { bg = "foam", blend = 10 },
				StatusLine = { fg = "love", bg = "love", blend = 10 },
				Search = { bg = "gold", inherit = false },
				GitSignsAdd = { bg = "NONE" },
				GitSignsChange = { bg = "NONE" },
				GitSignsDelete = { bg = "NONE" },
			},
		})
		vim.cmd.colorscheme("rose-pine")
		vim.cmd("highlight Search guibg=#E58AC8 guifg=#1D1E2C")

		vim.api.nvim_set_hl(0, "Normal", { bg = "none" })
		vim.api.nvim_set_hl(0, "NormalFloat", { bg = "none" })
	end,
}

--
-- return {
--   "catppuccin/nvim",
--   name = "catppuccin",
--   priority = 1000,
--
--   config = function()
--     require("catppuccin").setup({
--    flavour = "mocha", -- latte, frappe, macchiato, mocha
--     background = { -- :h background
--         light = "latte",
--         dark = "mocha",
--     },
--     transparent_background = true, -- disables setting the background color.
--     show_end_of_buffer = false, -- shows the '~' characters after the end of buffers
--     term_colors = true, -- sets terminal colors (e.g. `g:terminal_color_0`)
--     dim_inactive = {
--         enabled = true, -- dims the background color of inactive window
--         shade = "dark",
--         percentage = 0.15, -- percentage of the shade to apply to the inactive window
--     },
--     no_italic = false, -- Force no italic
--     no_bold = false, -- Force no bold
--     no_underline = false, -- Force no underline
--     -- Integrations
--     default_integrations = true,
--     integrations = {
--
--     }
--     })
--
--     -- setup must be called before loading
--     vim.cmd.colorscheme "catppuccin"
--   end,
-- }
--
--
