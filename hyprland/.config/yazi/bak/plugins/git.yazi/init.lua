local M = {}

function M:preview(state)
	return {
		title = "Git",
		body = vim.fn.system("git status --short -- " .. vim.fn.shellescape(state.file)),
	}
end

return M
