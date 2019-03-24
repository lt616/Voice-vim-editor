let g:mode = "n"

" Vim Function for selecting a node in virtual mode
" Argument 00: node_pos fake json
function! VirtualSelect(node_pos)
python3 << EOF
import sys
from importlib import reload
sys.path.append('./python-lib')
import dispatcher
import vim

res = dispatcher.node_dispatcher(vim.eval("a:node_pos"))

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

	let result = VirtualSelect(node_pos)
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

#print(res)
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

res = dispatcher.test()
vim.command("echom " + res);
#vim.command("echom libclang#version()")
EOF
endfunction

function! Test(command)
let ast = libclang#AST#non_system_headers#all('hello_libclang.cpp')
echom ast
endfunction
