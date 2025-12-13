local M = {}

-- Helper: get kitty color by name
local function kitty_color(name)
	local handle = io.popen("kitty @ get-colors --color " .. name)
	if not handle then
		return "#ffffff"
	end
	local result = handle:read("*a")
	handle:close()
	return result:gsub("%s+$", "")
end

function M:setup()
	local theme = {
		ui = {
			background = kitty_color("background"),
			foreground = kitty_color("foreground"),
			accent = kitty_color("color4"), -- blue
			highlight = kitty_color("color6"), -- cyan
			info = kitty_color("color2"), -- green
			warn = kitty_color("color3"), -- yellow
			error = kitty_color("color1"), -- red
		},

		manager = {
			folder = kitty_color("color4"),
			folder_hover = kitty_color("color6"),
			file_hover = kitty_color("color5"),
			preview_border = kitty_color("color8"),
		},
	}

	return theme
end

return M
