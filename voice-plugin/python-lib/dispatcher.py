import sys
import json
import switch
import edit
import move
import search
import clear
import node

from pprint import pprint
# from importlib import reload
# reload(switch)
# reload(switch)

RESERVED_WORDS_COND = ["if", "switch", "for", "while", "dowhile"]
RESERVED_WORDS_UNCOND = ["auto", "return", "char", "string", "bool", "int", "float", "double"]

def print_error(err):
	return ":echo \"" + err + "\""

def select_nodes(nodes):
	return [node for node in nodes if "file" in node and "parent" in node and node["file"] == node["parent"]]

def voice_command(command, mode):
	# check if imported correct
	# if "switch" not in dir():
  		# print("switch not imported!")

	res_str = print_error("Command " + command + " not recognized.")

	commands = command.split(" ", 1)


	
	# return msg need to be changed

	# switch mode
	if commands[0].lower() == "switch" and len(commands) > 1:
		mode, res_str = switch.dispatch(commands[1], mode)

	# add text
	elif commands[0].lower() == "add" and len(commands) > 1:
		mode, res_str = edit.add_dispatch(commands[1], mode)

	# delete text
	elif commands[0].lower() == "delete" and len(commands) > 1:
		mode, res_str = edit.delete_dispatch(commands[1], mode)

	# move cursor
	elif commands[0].lower() == "move" and len(commands) > 1:
		mode, res_str = move.dispatch(commands[1], mode)

	# search text
	elif commands[0].lower() == "search" and len(commands) > 1:
		mode, res_str = search.dispatch(commands[1], mode)

	# show next search result
	elif command.lower() == "next":
		mode, res_str = search.next(mode)

	# clear search result
	# elif commands[0].lower() == "clear":
		# mode, res_str = clear.dispatch(mode)

	return mode, res_str

def node_dispatcher(command, node_pos, cursor_start, cursor_end):
	if command == "current":
		return node_pos["start"]["offset"], node_pos["end"]["offset"], node.node_select(node_pos)

	elif command == "parent":
		return node.parent_select(select_nodes(node_pos["root"]), cursor_start, cursor_end)

	elif command == "child":
		return node.child_select(select_nodes(node_pos["root"]), cursor_start, cursor_end)

	elif command == "next sibling":
		return node.next_sibling_select(select_nodes(node_pos["root"]), cursor_start, cursor_end)

	elif command == "previous sibling":
		return node.prev_sibling_select(select_nodes(node_pos["root"]), cursor_start, cursor_end)

	else:
		print_error("Invalid node command.")

def node_dispatcher_current(node_pos, line_start, col_start, line_end, col_end):
	return node.current_select(select_nodes(node_pos["root"]), line_start, col_start, line_end, col_end)

def node_search(command, node_pos, line, col):
	commands = command.split(" ")
	if len(commands) < 3:
		return -1, -1, search_format_error()

	# search AST using DFS and find out the first occurence after cursor

	# the first argument is commands[2]
	if commands[2].lower() == "function" or commands[2].lower() == "variable":
		# search 1st occurence of a var name

		if len(commands) < 4:
			return -1, -1, search_format_error()

		# concate the rest of arguments as var name
		# a string with no space
		var_name = "".join(commands[3:]).lower()
		return node.variable_search(select_nodes(node_pos["root"]), line, col, var_name)

	elif commands[2].lower() == "declaration":
		# search declaration of a func / variable

		if len(commands) < 4:
			return -1, -1, search_format_error()

		# concate the rest of arguments as var name
		# a string with no space
		var_name = "".join(commands[3:]).lower()
		return node.declaration_search(select_nodes(node_pos["root"]), line, col, var_name)				

	elif commands[2] in RESERVED_WORDS_COND:
		# search 1st occurence of a loop or decision

		keywords = {}
		for i in range(3, len(commands)):
			keywords[commands[i]] = False

		return node.condition_search(select_nodes(node_pos["root"]), line, col, keywords, commands[2])

	else:
		# search by plain text
		
		keywords = {}
		for i in range(2, len(commands)):
			keywords[commands[i]] = {}

		return node.inline_search(select_nodes(node_pos["root"]), line, col, keywords)




def handle_json(text):
	text = text.replace('"', "000\"")
	text = text.replace("'", '"')
	text = text.replace("000\"", "'")

	return json.loads(text)




# print(voice_command("switch mode"))
# print(voice_command("add text printf", "n"))
# print(voice_command("delete 5 chars", "n"))


