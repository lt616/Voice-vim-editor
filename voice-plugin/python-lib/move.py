import sys
import exception

def dispatch(command, mode):
	commands = command.split(" ")


	if len(commands) < 2:
		return mode, exception.move_format_error()

	if commands[0].lower() == "line":
		# move line <count>
		try:
			count = int(commands[1])
		except:
			return mode, exception.move_format_error()

		return mode, "normal! " + str(count) + "gg"
	else:
		# move <count> <char / word / line> <up / down / forward / backward / right / left>
		try:
			count = int(commands[0])
		except:
			return mode, exception.move_format_error()

		direct = True
		if len(commands) > 2:
			if "backward" in commands[2].lower() or "up" in commands[2].lower() or "right" in commands[2].lower():
				direct = False

		if "char" in commands[1].lower():
			direct_sym = "l" if direct else "h"
			del_cmd = str(count) + direct_sym
		elif "word" in commands[1].lower():
			direct_sym = "w" if direct else "b"
			del_cmd = str(count) + direct_sym
		elif "line" in commands[1].lower():
			direct_sym = "j" if direct else "k"
			del_cmd = str(count) + direct_sym
		else:
			return mode, exception.move_format_error()

		return mode, "normal! " + del_cmd






	return mode, exception.print_error("Not implemented yet.")
