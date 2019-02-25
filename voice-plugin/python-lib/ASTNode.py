import sys

class ASTNode:

	# self.parent
	# self.children

	def __init__(self, dict):
		self.type_kind = dict["type_kind"]
		self.start_line = dict["line"]
		self.start_column = dict["column"]
		self.offset = dict["offset"]
		self.kind = dict["kind"]
		self.kind_type = dict["kind_type"]
		self.spell = dict["spell"] if "spell" in dict else ""

		self.end_line = None
		self.end_column = None
		self.parent = None
		self.children = []

	def set_parent(self, parent):
		self.parent = parent

	def set_child(self, child):
		self.children.append(child)

	def set_end_pos(self, next):
		self.endline = next["line"]
		self.column = next["column"]
	
	def get_full_pos(self):
		pass

	def get_parent(self):
		return self.parent

	def get_children(self):
		return self.children



