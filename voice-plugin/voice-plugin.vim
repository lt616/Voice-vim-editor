let g:mode = "n"
let g:cursor_start = -1
let g:cursor_end = -1
let g:search_results = []
let g:search_index = -1

" Vim Function for selecting a node in virtual mode
" Argument 00: node_pos fake json

function! VisualSelect(opt, node_pos)
python3 << EOF
import sys
from importlib import reload
sys.path.append('./python-lib')
import dispatcher
import vim

#print(vim.eval("g:cursor_start"))
#print(vim.eval("g:cursor_end"))

start_pos, end_pos, res = dispatcher.node_dispatcher(vim.eval("a:opt"), vim.eval("a:node_pos"), vim.eval("g:cursor_start"), vim.eval("g:cursor_end"))

#print("str " + str(start_pos) + " " + str(end_pos))

#print(res)

vim.command("let g:cursor_start = %s"% start_pos)
vim.command("let g:cursor_end = %s"% end_pos)
vim.command(res)
EOF
endfunction


function! VisualNextSearchResult()
python3 << EOF
import sys
from importlib import reload
sys.path.append('./python-lib')
import dispatcher
import vim

res = vim.eval("g:search_results")
index = int(vim.eval("g:search_index"))

if res == []:
    vim.command("echom 'No result.'")
else:
    index += 1
    if index >= len(res):
        index = 0

    vim.command("let g:search_index = %d"% index)
    vim.command("normal! %sG %s| 2h v %sG %s|"% (res[index]["start_line"], res[index]["start_column"], res[index]["end_line"], res[index]["end_column"]))
EOF
endfunction


function! VisualSelectCurrent(node_pos, line_start, col_start, line_end, col_end)
python3 << EOF
import sys
from importlib import reload
sys.path.append('./python-lib')
import dispatcher
import vim

start_pos, end_pos, res = dispatcher.node_dispatcher_current(vim.eval("a:node_pos"), vim.eval("a:line_start"), vim.eval("a:col_start"), vim.eval("a:line_end"), vim.eval("a:col_end"))
print(res)


vim.command("let g:cursor_start = %s"% start_pos)
vim.command("let g:cursor_end = %s"% end_pos)
vim.command(res)

EOF
endfunction


function! VisualSearch(search_cmd, node_pos, line, column)
python3 << EOF
import sys
from importlib import reload
sys.path.append('./python-lib')
import dispatcher
import vim

start_pos, end_pos, res = dispatcher.node_search(vim.eval("a:search_cmd"), vim.eval("a:node_pos"), vim.eval("a:line"), vim.eval("a:column"))
print(res)

if start_pos == -2:
    if res == []:
        vim.command("echo 'No result.'")
        vim.command("let g:search_results = %s"% res)
        vim.command("let g:search_index = %d"% -1)
    else:
        vim.command("normal! %sG %s| 2h v %sG %s|"% (res[0]["start_line"], res[0]["start_column"], res[0]["end_line"], res[0]["end_column"]))
        vim.command("let g:search_results = %s"% res)
        vim.command("let g:search_index = %d"% 0)
else:
    vim.command(res)
EOF
endfunction


function! VoiceCommand(command)

"let visual_pos = GetVisualSelection()

if a:command =~ "select current node"
	" get current cursor position
	"let file_name = expand('%:t:r')
	"let ext_name = expand('%:e')
	"let line_pos = line(".")
	"let col_pos = virtcol('.')
	"let file = file_name . "." . ext_name
	
	" get the most inner node at current cursor position using libclang
	"let node_pos = libclang#location#extent(file, line_pos, col_pos)
	
	" if current cursor position is not a valid node
	"if empty(node_pos) == 1
	"	echom Error: Current position doesn't have a node."
	"	return
	"endif

	"let temp_pos = VisualSelect("current", node_pos)
	" echom g:cursor_start
	" echom g:cursor_end

        " get  file name
        let file_name = expand('%:t:r')
        let ext_name = expand('%:e')
        let file = file_name . "." . ext_name

        " get entire AST
        let ast = libclang#AST#non_system_headers#all(file)

	"let line = getpos(".")
	let [line_start, column_start] = getpos("'<")[1:2]
        let [line_end, column_end] = getpos("'>")[1:2]
	echom line_start
	echom line_end
	echom column_start
	echom column_end

	"echom line
	let temp_pos = VisualSelectCurrent(ast, line_start, column_start, line_end, column_end)
	
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

	let temp_pos = VisualSearch("child", ast)
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

if a:command =~ "select previous sibling node"
	" if no node selected
	if g:cursor_start == -1 && g:cursor_end == -1
		echom "Error: No node selected. Cannot find previous sibling node"
		return
	endif

	" get file name
	let file_name = expand('%:t:r')
	let ext_name = expand('%:e')
	let file = file_name . "." . ext_name

	" get entire AST
	let ast = libclang#AST#non_system_headers#all(file)

	let temp_pos = VisualSelect("previous sibling", ast)
	return
endif

if a:command =~ "next result"
	let temp_pos = VisualNextSearchResult()
	return
endif

if a:command =~ "search node"
	" get file name
        let file_name = expand('%:t:r')
        let ext_name = expand('%:e')
        let file = file_name . "." . ext_name

        " get entire AST
        let ast = libclang#AST#non_system_headers#all(file)

	let [line, column] = getpos(".")[1:2]

        let temp_pos = VisualSearch(a:command, ast, line, column) 
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
let ast = libclang#AST#non_system_headers#all('deduction.cpp')
echom ast
endfunction
