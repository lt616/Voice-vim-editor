import sys

def print_error(err):
	return ":echo \"" + err + "\""

def delete_format_error():
	return print_error("Incorrect delete format")

def move_format_error():
	return print_error("Incorrect move format")

def search_format_error():
	return print_error("Incorrect search format")

def unknown_mode(mode):
	return print_error("Error: Unknow mode [" + mode + "]")
