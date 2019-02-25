let g:mode = "n"

function! VoiceCommand(command)
python3 << EOF
import sys
from importlib import reload
sys.path.append('./python-lib')
#sys.path.append('./python-lib/switch')
import vim
import dispatcher
#reload(dispatcher)

print(vim.eval("g:mode"))
#vim.command("let g:mode = \"i\"")
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
vim.command("normal! asdasdas<CR>")
EOF
endfunction

function! Test(command)
execute "normal! " . a:command
endfunction
