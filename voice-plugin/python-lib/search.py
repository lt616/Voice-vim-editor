import sys
import exception

def dispatch(command, mode):
	commands = command.split(" ")

# clear search result

	# search current word
	if command == "current word":
		return mode, "normal! *"
	# search gsfdsfsfd
	else:
		return mode, "normal! /" + command

def next(mode):
	return mode, "normal! n";
