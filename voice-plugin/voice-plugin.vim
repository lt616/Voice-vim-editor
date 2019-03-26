let g:mode = "n"
let g:cursor_start = -1
let g:cursor_end = -1

" Vim Function for selecting a node in virtual mode
" Argument 00: node_pos fake json

function! VisualSelect(opt, node_pos)
python3 << EOF
import sys
from importlib import reload
sys.path.append('./python-lib')
import dispatcher
import vim

print(vim.eval("g:cursor_start"))
print(vim.eval("g:cursor_end"))

start_pos, end_pos, res = dispatcher.node_dispatcher(vim.eval("a:opt"), vim.eval("a:node_pos"), vim.eval("g:cursor_start"), vim.eval("g:cursor_end"))

print("str " + str(start_pos) + " " + str(end_pos))

print(res)

vim.command("let g:cursor_start = %s"% start_pos)
vim.command("let g:cursor_end = %s"% end_pos)
vim.command(res)
EOF
endfunction

function! VoiceCommand(command)

if a:command =~ "select current node"
	" get current cursor position
	let file_name = expand('%:t:r')
	let ext_name = expand('%:e')
	let line_pos = line(".")
	let col_pos = virtcol('.')
	let file = file_name . "." . ext_name
	
	" get the most inner node at current cursor position using libclang
	let node_pos = libclang#location#extent(file, line_pos, col_pos)
	
	" if current cursor position is not a valid node
	if empty(node_pos) == 1
		echom "Error: Current position doesn't have a node."
		return
	endif

	let temp_pos = VisualSelect("current", node_pos)
	echom g:cursor_start
	echom g:cursor_end
	return
endif


if a:command =~ "select parent node"
	" if no node selected
	if g:cursor_start == -1 && g:cursor_end == -1
		echom "Error: No node selected. Cannot find parent node"
		return
	endif

	" get  file name
	let file_name = expand('%:t:r')
	let ext_name = expand('%:e')
	let file = file_name . "." . ext_name

	" get entire AST
	let ast = libclang#AST#non_system_headers#all(file)
	
	let temp_pos = VisualSelect("parent", ast)
	return
endif


if a:command =~ "select child node"
	" if no node selected
	if g:cursor_start == -1 && g:cursor_end == -1
		echom "Error: No node selected. Cannot find child node"
		return
	endif

	" get file name
	let file_name = expand('%:t:r')
	let ext_name = expand('%:e')
	let file = file_name . "." . ext_name

	" get entire AST
	let ast = libclang#AST#non_system_headers#all(file)

	let temp_pos = VisualSelect("child", ast)
	return
endif

if a:command =~ "select next sibling node"
	" if no node selected
	if g:cursor_start == -1 && g:cursor_end == -1
		echom "Error: No node selected. Cannot find next sibling node"
		return
	endif

	" get file name
	let file_name = expand('%:t:r')
	let ext_name = expand('%:e')
	let file = file_name . "." . ext_name

	" get entire AST
	let ast = libclang#AST#non_system_headers#all(file)

	let temp_pos = VisualSelect("next sibling", ast)
	return
endif


python3 << EOF
import sys
from importlib import reload
sys.path.append('./python-lib')
#sys.path.append('./python-lib/switch')
import vim
import dispatcher


#print(vim.eval("g:mode"))
#vim.command("let g:mode = \"i\"")

# edit-level commands
mode, res = dispatcher.voice_command(vim.eval("a:command"), vim.eval("g:mode"))

#print(mode)
if mode == "n":
	vim.command("let g:mode = \"n\"")
else:
	vim.command("let g:mode = \"i\"")

# clear cursor positions
vim.command("let g:cursor_start = -1")
vim.command("let g:cursor_end = -1")
vim.command(res)

EOF
endfunction






function! Reload()
python3 << EOF
import sys
from importlib import reload
sys.path.append('./python-lib')
import vim
import dispatcher
reload(dispatcher)
EOF
endfunction

function! Execute()
python3 << EOF
import sys
from importlib import reload
sys.path.append('./python-lib')
import vim
import dispatcher

#end_pos = vim.command("execute 'w !wc -m'")
#print(end_pos)
#vim.command("echom libclang#version()")
EOF

let value = system("wc -m")
echom value

endfunction

function! Test(command)
vim.command("w !wc -m")
"let ast = libclang#AST#non_system_headers#all('hello_libclang.cpp')
"echom ast
endfunction
