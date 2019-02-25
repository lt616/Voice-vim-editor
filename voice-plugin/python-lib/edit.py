import sys
import exception

def add_dispatch(command, mode):
	# If currently in insert mode, add whatever occurs after ADD command
	if mode == "i":
		return mode, "normal! a" + command
	# If in normal mode, may add text or add node?
	elif mode == "n":
		commands = command.split(" ", 1)
		if commands[0].lower() == "text":
			return mode, "normal! a" + commands[1]
		else:
			return mode, "echo: Not implemented yet"

	return mode, exception.print_error("Unable to process [add " + command + "]")


def delete_dispatch(command, mode):
	# delete # type for/backward
	commands = command.split(" ")

	if len(commands) < 2:
		return mode, exception.delete_format_error()

	try:
		count = int(commands[0])
	except:
		return mode, exception.delete_format_error()

	direct = True
	if len(commands) > 2 and "backward" in commands[2].lower():
		direct = False

	if "char" in commands[1]:
		direct_sym = "l" if direct else "h"
		del_cmd = "d" + str(count) + direct_sym
	elif "word" in commands[1]:
		direct_sym = "w" if direct else "b" 
		del_cmd = "d" + str(count) + direct_sym
	elif "line" in commands[1]:
		direct_sym = "d" if direct else "k"
		del_cmd = str(count) + "d" + direct_sym
	else:
		return mode, exception.delete_format_error()

	return mode, "normal! " + del_cmd



