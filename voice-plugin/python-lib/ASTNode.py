import sys

class ASTNode:

	# self.parent
	# self.children

	def __init__(self, dict):
		self.type_kind = dict["type_kind"]
		self.line = dict["line"]
		self.column = dict["column"]
		self.offset = dict["offset"]
		self.kind = dict["kind"]
		self.kind_type = dict["kind_type"]
		self.spell = dict["spell"] if "spell" in dict else ""

		self.parent = None
		self.children = []

	def set_parent(parent):
		self.parent = parent

	def set_child(child):
		self.children.append(child)


