import sys
import json
import exception
from ASTNode import ASTNode
from pprint import pprint

class SearchSpace():

	def __init__(self, cursor_start, cursor_end, err_msg):
		self.res_line_start = -1
		self.res_col_start = -1
		self.res_line_end = -1
		self.res_col_end = -1
		self.offset_start = -1
		self.offset_end = -1

		self.cursor_start = cursor_start
		self.cursor_end = cursor_end

		self.err_msg = err_msg

	def visual_select(self, err_str):
		if self.res_line_start == -1 and self.res_col_end == -1:
			# exception.print_error(err_str)
			return "echo \"" + "Error: " + self.err_msg + "\""

		if self.res_line_end == -1 or self.res_col_end == -1:
			return "normal! " + str(self.res_line_start) + "G " + str(self.res_col_start) + "| 2h v " + "G$"
		else:
			return "normal! " + str(self.res_line_start) + "G " + str(self.res_col_start) + "| 2h v " + str(self.res_line_end) + "G " + str(self.res_col_end) + "|" 

	def set_result(self, node_pos):
		if node_pos is None:
			self.res_line_start = -1
			self.res_col_start = -1
			self.offset_start = self.cursor_start

			self.res_line_end = -1
			self.res_col_end = -1
			self.offset_end = self.cursor_end
			return

		self.res_line_start = node_pos["start"]["line"]
		self.res_col_start = node_pos["start"]["column"]
		self.offset_start = node_pos["start"]["offset"]

		self.res_line_end = node_pos["end"]["line"]
		self.res_col_end = node_pos["end"]["column"]
		self.offset_end = node_pos["end"]["offset"]

	def set_next_sibling_result(self, nodes, index, next_node_pos):
		if index >= len(nodes):
			self.res_line_start = -1
			self.res_col_start = -1
			self.offset_start = -1

			self.res_line_end = -1
			self.res_col_end = -1
			self.offset_end = -1
		else:
			self.res_line_start = int(nodes[index]["line"])
			self.res_col_start = int(nodes[index]["column"])
			self.offset_start = int(nodes[index]["offset"])

			if index + 1 >= len(nodes):
				if next_node_pos is None:
					self.res_line_end = -1
					self.res_col_end = -1
					self.offset_end = -1
				else:
					self.res_line_end = int(next_node_pos["line"])
					self.res_col_end = int(next_node_pos["column"])
					self.offset_end = int(next_node_pos["offset"]) - 1
			else:
				self.res_line_end = int(nodes[index + 1]["line"])
				self.res_col_end = int(nodes[index + 1]["column"])
				self.offset_end = int(nodes[index + 1]["offset"]) - 1


	def set_prev_sibling_result(self, nodes, index):
		if index - 1 < 0:
			self.res_line_start = -1
			self.res_col_start = -1
			self.offset_start = -1

			self.res_line_end = -1
			self.res_col_end = -1
			self.offset_end = -1
		else:
			self.res_line_start = int(nodes[index - 1]["line"])
			self.res_col_start = int(nodes[index - 1]["column"])
			self.offset_start = int(nodes[index - 1]["offset"])

			self.res_line_end = int(nodes[index]["line"])
			self.res_col_end = int(nodes[index]["column"])
			self.offset_end = int(nodes[index]["offset"]) - 1

	def parent_search(self, node_pos):
		for child in node_pos["children"]: 
			if int(child["start"]["offset"]) == self.cursor_start and int(child["end"]["offset"]) == self.cursor_end:
				self.set_result(node_pos)
				return
			
			if int(child["start"]["offset"]) > self.cursor_end:
				self.set_result(None)
				return

			if int(child["end"]["offset"]) < self.cursor_start:
				continue;

			self.parent_search(child)
			return


	def child_search(self, node_pos):
		for child in node_pos["children"]: 
			if int(child["start"]["offset"]) == self.cursor_start and int(child["end"]["offset"]) == self.cursor_end:
				if child["children"] is []:
					self.set_result(None)
				else:
					self.set_result(child["children"][0])
				return
			
			if int(child["start"]["offset"]) > self.cursor_end:
				self.set_result(None)
				return

			if int(child["end"]["offset"]) < self.cursor_start:
				continue;

			self.child_search(child)
			return

	def next_sibling_search(self, node_pos):
		children = node_pos["children"]
		for i in range(len(children)): 
			if int(children[i]["start"]["offset"]) == self.cursor_start and int(children[i]["end"]["offset"]) == self.cursor_end:
				if i == len(children) - 1:
					self.set_result(None)
				else:
					self.set_result(children[i + 1])
				return
			
			if int(children[i]["start"]["offset"]) > self.cursor_end:
				self.set_result(None)
				return

			if int(children[i]["end"]["offset"]) < self.cursor_start:
				continue;

			self.next_sibling_search(children[i])
			return


	def prev_sibling_search(self, node_pos):
		children = node_pos["children"]
		for i in range(len(children)): 
			if int(children[i]["start"]["offset"]) == self.cursor_start and int(children[i]["end"]["offset"]) == self.cursor_end:
				if i == 0:
					self.set_result(None)
				else:
					self.set_result(children[i - 1])
				return
			
			if int(children[i]["start"]["offset"]) > self.cursor_end:
				self.set_result(None)
				return

			if int(children[i]["end"]["offset"]) < self.cursor_start:
				continue;

			self.prev_sibling_search(children[i])
			return



# virtual select
def node_select(node_pos):
	# print(node_pos["start"]["line"])
	# print(node_pos["start"]["column"])
	# print(node_pos["end"]["line"])
	# print(node_pos["end"]["column"])

	start_line = node_pos["start"]["line"]
	start_col = node_pos["start"]["column"]
	end_line = node_pos["end"]["line"]
	end_col = node_pos["end"]["column"]

	return "normal! " + str(start_line) + "G " + str(start_col) + "| 2h v " + str(end_line) + "G " + str(end_col) + "|" 


def parent_select(node_pos, cursor_start, cursor_end):
	root = {}
	root["children"] = node_pos

	search_space = SearchSpace(int(cursor_start), int(cursor_end), "No parent.")

	search_space.parent_search(root)
	# print(search_space.visual_select())
	# print(search_space.offset_start)
	# print(search_space.offset_end)
	return search_space.offset_start, search_space.offset_end, search_space.visual_select("Error: No parent node.")


def child_select(node_pos, cursor_start, cursor_end):
	root = {}
	root["children"] = node_pos

	search_space = SearchSpace(int(cursor_start), int(cursor_end), "No child.")
	search_space.child_search(root)
	# print(search_space.visual_select())
	# print(search_space.offset_start)
	# print(search_space.offset_end)
	return search_space.offset_start, search_space.offset_end, search_space.visual_select("Error: No child node.")


def next_sibling_select(node_pos, cursor_start, cursor_end):
	root = {}
	root["children"] = node_pos

	search_space = SearchSpace(int(cursor_start), int(cursor_end), "No next sibling.")
	search_space.next_sibling_search(root)
	# print(search_space.visual_select())
	# print(search_space.offset_start)
	# print(search_space.offset_end)
	return search_space.offset_start, search_space.offset_end, search_space.visual_select("Error: No next sibling node.")


def prev_sibling_select(node_pos, cursor_start, cursor_end):
	root = {}
	root["children"] = node_pos

	search_space = SearchSpace(int(cursor_start), int(cursor_end), "No previous sibling")
	search_space.prev_sibling_search(root)
	# print(search_space.visual_select())
	# print(search_space.offset_start)
	# print(search_space.offset_end)
	return search_space.offset_start, search_space.offset_end, search_space.visual_select("Error: No previous sibling node.")


def tree_construct(data, parent, next_node, next_uncle):
	cur_node = ASTNode(data)
	cur_node.set_parent(parent)
	# cur_node.set_end_pos(next_node)
	if not next_node is None:
		cur_node.set_end_pos(next_node)
	else:
		cur_node.set_end_pos(next_uncle)

	children = data["children"]
	for i in range(0, len(children)):
		next_child = None if i == len(children) - 1 else children[i + 1]
		tree_construct(children[i], cur_node, next_child, next_node)


def init_tree():
	with open("test3.json") as data_file:
		data = json.load(data_file)

	pprint(data)

	tree_construct(data["root"][0], None, None, None)


# with open("hello.txt") as data_file:
# 	data = json.load(data_file)

# 	print(prev_sibling_select(data["root"], 138, 143))





# init_tree()
