import sys
import exception


def dispatch(command, mode):
	def switch2insert():
		return "i", ":startinsert"

	def switch2normal():
		return "n", "stopinsert"

	if "insert" in command:
		return switch2insert()
	elif "normal" in command:
		return switch2normal()
	else:
		return mode, exception.unknown_mode(command)



