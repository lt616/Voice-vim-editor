let g:mode = "n"
let g:cursor_start = -1
let g:cursor_end = -1
let g:search_results = []
let g:search_index = -1
let g:compile_args = ""

" Vim Function for selecting a node in virtual mode
" Argument 00: node_pos fake json

function! ReadFlags()
python3 << EOF
import sys
from importlib import reload
import vim

with open('config', 'r') as file:
    data = file.read().replace('\n', '')
    flags = data.split(" ")

    flag_str = ""
    for flag in flags:
        flag_str += ", \""
        flag_str += flag
        flag_str += "\""

    vim.command("let g:compile_args = '%s'"% flag_str)

EOF
endfunction

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

    if type(res[index]) is str:
        vim.command("normal! %sG ^"% res[index])
        vim.command("normal! v $")
    else:
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
#print(res)

if start_pos == -2:
    if res == []:
        vim.command("echo 'No result.'")
        vim.command("let g:search_results = %s"% res)
        vim.command("let g:search_index = %d"% -1)
    else:
        vim.command("normal! %sG %s| 2h v %sG %s|"% (res[0]["start_line"], res[0]["start_column"], res[0]["end_line"], res[0]["end_column"]))
        vim.command("let g:search_results = %s"% res)
        vim.command("let g:search_index = %d"% 0)
elif start_pos == -3:
    if res == []:
        vim.command("echo 'No result.'")
        vim.command("let g:search_results = %s"% res)
        vim.command("let g:search_index = %d"% -1)
    else:
        vim.command("normal! %sG ^"% res[0])
        vim.command("normal! v $")
        vim.command("let g:search_results = %s"% res)
        vim.command("let g:search_index = %d"% 0)
else:
    vim.command(res)
EOF
endfunction


function! VoiceCommand(command)

"let visual_pos = GetVisualSelection()

if a:command =~ "select current node"
	"let node_pos = libclang#location#extent(file, line_pos, col_pos)
        " get  file name
        let file_name = expand('%:t:r')
        let ext_name = expand('%:e')
        let file = file_name . "." . ext_name

        " get entire AST
        "let ast = libclang#AST#current_file#all(file)
	let a = ReadFlags()
        execute("let ast = libclang#AST#current_file#all(\"" . file . "\"" . g:compile_args . ")")

	"let line = getpos(".")
	let [line_start, column_start] = getpos("'<")[1:2]
        let [line_end, column_end] = getpos("'>")[1:2]
	
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
	"let ast = libclang#AST#current_file#all(file)
	let a = ReadFlags()
        execute("let ast = libclang#AST#current_file#all(\"" . file . "\"" . g:compile_args . ")")

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
	"let ast = libclang#AST#current_file#all(file)
	let a = ReadFlags()
        execute("let ast = libclang#AST#current_file#all(\"" . file . "\"" . g:compile_args . ")")

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
	"let ast = libclang#AST#current_file#all(file)
	let a = ReadFlags()
        execute("let ast = libclang#AST#current_file#all(\"" . file . "\"" . g:compile_args . ")")

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
	"let ast = libclang#AST#current_file#all(file)
	let a = ReadFlags()
        execute("let ast = libclang#AST#current_file#all(\"" . file . "\"" . g:compile_args . ")")

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
        " let ast = libclang#AST#current_file#all(file)
	let a = ReadFlags()
	execute("let ast = libclang#AST#current_file#all(\"" . file . "\"" . g:compile_args . ")")

        "echo ast
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

nnoremap sn :<C-u>call VoiceCommand("select current node")<cr>
nnoremap sp :<C-u>call VoiceCommand("select parent node")<cr>
nnoremap sc :<C-u>call VoiceCommand("select child node")<cr>
nnoremap sps :<C-u>call VoiceCommand("select previous sibling node")<cr>
nnoremap sns :<C-u>call VoiceCommand("select next sibling node")<cr>
