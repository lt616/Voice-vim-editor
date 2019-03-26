import sys
import json
import exception
from ASTNode import ASTNode
from pprint import pprint

class SearchSpace():

	def __init__(self, cursor_start, cursor_end):
		self.res_line_start = -1
		self.res_col_start = -1
		self.res_line_end = -1
		self.res_col_end = -1
		self.offset_start = -1
		self.offset_end = -1

		self.cursor_start = cursor_start
		self.cursor_end = cursor_end

	def visual_select(self):
		if self.res_line_start == -1 and self.res_col_end == -1:
			exception.print_error("No parent node.")
			return None

		if self.res_line_end == -1 or self.res_col_end == -1:
			return "normal! " + str(self.res_line_start) + "G " + str(self.res_col_start) + "| 2h v " + "G$"
		else:
			return "normal! " + str(self.res_line_start) + "G " + str(self.res_col_start) + "| 2h v " + str(self.res_line_end) + "G " + str(self.res_col_end) + "|" 

	def set_parent_result(self, node_pos, next_node_pos):
		self.res_line_start = int(node_pos["line"])
		self.res_col_start = int(node_pos["column"])
		self.offset_start = int(node_pos["offset"])

		if next_node_pos is None:
			self.res_line_end = -1
			self.res_col_end = -1
			self.offset_end = -1

		else:
			self.res_line_end = int(next_node_pos["line"])
			self.res_col_end = int(next_node_pos["column"])
			self.offset_end = int(next_node_pos["offset"]) - 1

	def set_child_result(self, node_pos, next_node_pos, next_parent_pos):
		if len(node_pos["children"]) == 0:
			self.res_line_start = -1
			self.res_col_start = -1
			self.offset_start = -1
		else:
			self.res_line_start = int(node_pos["children"][0]["line"])
			self.res_col_start = int(node_pos["children"][0]["column"])
			self.offset_start = int(node_pos["children"][0]["offset"])

		if len(node_pos["children"]) < 2:
			if next_node_pos is None:
				if next_parent_pos is None:
					self.res_line_end = -1
					self.res_col_end = -1
					self.offset_end = -1
				else:
					self.res_line_end = int(next_parent_pos["line"])
					self.res_col_end = int(next_parent_pos["column"])
					self.offset_end = int(next_parent_pos["offset"]) - 1
			else:
				self.res_line_end = int(next_node_pos["line"])
				self.res_col_end = int(next_node_pos["column"])
				self.offset_end = int(next_node_pos["offset"]) - 1
		else:
			self.res_line_end = int(node_pos["children"][1]["line"])
			self.res_col_end = int(node_pos["children"][1]["column"])
			self.offset_end = int(node_pos["children"][1]["offset"]) - 1

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


	def parent_search(self, node_pos, next_node_pos):
		for i in range(len(node_pos["children"])):
			if int(node_pos["children"][i]["offset"]) > self.cursor_start:
				self.parent_search(node_pos["children"][i - 1], node_pos["children"][i])
				break;
			elif int(node_pos["children"][i]["offset"]) == self.cursor_start:
				if i == len(node_pos["children"]) - 1 or self.cursor_end == -1:
					# MAYBE BUG: multiple functions
					self.set_parent_result(node_pos, next_node_pos)

					self.parent_search(node_pos["children"][i], None)
				elif self.cursor_end <= int(node_pos["children"][i + 1]["offset"]):
					# set search result
					# MAYBE BUG: when cursor_end is -1
					self.set_parent_result(node_pos, next_node_pos)

					self.parent_search(node_pos["children"][i], node_pos["children"][i + 1])
				break;
			elif i == len(node_pos["children"]) - 1:
				self.parent_search(node_pos["children"][i], None)
			else:
				pass

	def child_search(self, node_pos, next_node_pos):

		for i in range(len(node_pos["children"])):
			# if next_node_pos is None:
			# 	print(str(node_pos["children"][i]["offset"]) + "next is none")
			# else:
			# 	print(str(node_pos["children"][i]["offset"]) + "next is " + str(next_node_pos["offset"]))

			if int(node_pos["children"][i]["offset"]) > self.cursor_start:
				self.child_search(node_pos["children"][i - 1], node_pos["children"][i])
				break;
			elif int(node_pos["children"][i]["offset"]) == self.cursor_start:
				if i == len(node_pos["children"]) - 1 or self.cursor_end == -1:
					self.set_child_result(node_pos["children"][i], None, next_node_pos)
					self.child_search(node_pos["children"][i], None)
				elif self.cursor_end <= int(node_pos["children"][i + 1]["offset"]):
					self.set_child_result(node_pos["children"][i], node_pos["children"][i + 1], next_node_pos)
					self.child_search(node_pos["children"][i], node_pos["children"][i + 1])
				break;
			elif i == len(node_pos["children"]) - 1:
				self.child_search(node_pos["children"][i], None)
			else:
				pass

	def next_sibling_search(self, node_pos, next_node_pos):
		for i in range(len(node_pos["children"])):
			if int(node_pos["children"][i]["offset"]) > self.cursor_start:
				self.next_sibling_search(node_pos["children"][i - 1], node_pos["children"][i])
				break;
			elif int(node_pos["children"][i]["offset"]) == self.cursor_start:
				if i == len(node_pos["children"]) - 1 or self.cursor_end == -1:
					self.set_next_sibling_result(node_pos["children"], i + 1, next_node_pos)
					self.next_sibling_search(node_pos["children"][i], None)
				elif self.cursor_end <= int(node_pos["children"][i + 1]["offset"]):
					self.set_next_sibling_result(node_pos["children"], i + 1, next_node_pos)
					self.next_sibling_search(node_pos["children"][i], node_pos["children"][i + 1])
				break;
			elif i == len(node_pos["children"]) - 1:
				self.next_sibling_search(node_pos["children"][i], None)
			else:
				pass



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

	root = node_pos[0]

	search_space = SearchSpace(int(cursor_start), int(cursor_end))

	search_space.parent_search(root, None)
	# print(search_space.visual_select())
	# print(search_space.offset_start)
	# print(search_space.offset_end)
	return search_space.offset_start, search_space.offset_end, search_space.visual_select()


def child_select(node_pos, cursor_start, cursor_end):
	root = {}
	root["children"] = node_pos

	search_space = SearchSpace(int(cursor_start), int(cursor_end))
	search_space.child_search(root, None)
	print(search_space.visual_select())
	print(search_space.offset_start)
	print(search_space.offset_end)
	return search_space.offset_start, search_space.offset_end, search_space.visual_select()


def next_sibling_select(node_pos, cursor_start, cursor_end):
	root = {}
	root["children"] = node_pos

	search_space = SearchSpace(int(cursor_start), int(cursor_end))
	search_space.next_sibling_search(root, None)
	print(search_space.visual_select())
	print(search_space.offset_start)
	print(search_space.offset_end)
	return search_space.offset_start, search_space.offset_end, search_space.visual_select()


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


with open("hello_output.txt") as data_file:
	data = json.load(data_file)

	next_sibling_select(data["root"], 142, 144)





# init_tree()
