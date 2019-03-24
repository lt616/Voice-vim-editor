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

def print_error(err):
	return ":echo \"" + err + "\""

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

def node_dispatcher(node_pos_raw):
	return node.node_select(node_pos_raw)

def handle_json(text):
	text = text.replace('"', "000\"")
	text = text.replace("'", '"')
	text = text.replace("000\"", "'")

	return json.loads(text)


# print(voice_command("switch mode"))
# print(voice_command("add text printf", "n"))
# print(voice_command("delete 5 chars", "n"))


