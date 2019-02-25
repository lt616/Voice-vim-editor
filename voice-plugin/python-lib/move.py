import sys
import exception

def dispatch(command, mode):
	commands = command.split(" ")

	if len(commands) < 2:
		return mode, exception.move_format_error()

	try:
		count = int(commands[0])
	except:
		return mode, exception.move_format_error()

	return mode, exception.print_error("Not implemented yet.")
