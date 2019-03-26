import sys
import json
from ASTNode import ASTNode
from pprint import pprint

class SearchSpace():

	def __init__(self):
		self.res_line_start = -1
		self.res_col_start = -1
		self.res_line_end = -1
		self.res_col_end = -1
		self.offset_start = -1
		self.offset_end = -1

	def visual_select(self):
		if self.res_line_end == -1 or self.res_col_end == -1:
			return "normal! " + str(self.res_line_start) + "G " + str(self.res_col_start) + "| 2h v " + "G$"
		else:
			return "normal! " + str(self.res_line_start) + "G " + str(self.res_col_start) + "| 2h v " + str(self.res_line_end) + "G " + str(self.res_col_end) + "|" 


	def node_search(self, node_pos, next_node_pos, cursor_start, cursor_end):

		for i in range(len(node_pos["children"])):
			if int(node_pos["children"][i]["offset"]) > cursor_start:
				self.node_search(node_pos["children"][i - 1], node_pos["children"][i], cursor_start, cursor_end)
				break;
			elif int(node_pos["children"][i]["offset"]) == cursor_start:
				if i == len(node_pos["children"]) - 1:
					# set search result
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

					self.node_search(node_pos["children"][i], None, cursor_start, cursor_end)
				elif cursor_end <= int(node_pos["children"][i + 1]["offset"]):

					# set search result
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

					self.node_search(node_pos["children"][i], node_pos["children"][i + 1], cursor_start, cursor_end)
				
				break;
			elif i == len(node_pos["children"]) - 1:
				self.node_search(node_pos["children"][i], None, cursor_start, cursor_end)

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


# def node_search(node_pos, next_node_pos, cursor_start, cursor_end):

# 	for i in range(len(node_pos["children"])):
# 		if node_pos["children"][i]["offset"] > cursor_start:
# 			print(str(node_pos["children"][i]["offset"]) + ">=" + str(cursor_start))
# 			node_search(node_pos["children"][i - 1], node_pos["children"][i], cursor_start, cursor_end)
# 			break;
# 		elif node_pos["children"][i]["offset"] == cursor_start:
# 			print("==")
# 			if cursor_end > node_pos["children"][i + 1]["offset"]:
# 				return

# 			# set search result
# 			res_line_start = node_pos["line"]
# 			res_col_start = node_pos["column"]

# 			if next_node_pos is None:
# 				res_line_end = -1
# 				res_col_end = -1
# 			else:
# 				res_line_end = next_node_pos["line"]
# 				res_col_end = next_node_pos["column"]

# 			if i == len(node_pos["children"]) - 1:
# 				node_search(node_pos["children"][i], None, cursor_start, cursor_end)
# 			else:
# 				node_search(node_pos["children"][i], node_pos["children"][i + 1], cursor_start, cursor_end)
# 			break;
# 		elif i == len(node_pos["children"]) - 1:
# 			print("lastLAST" + str(node_pos["children"][i]["offset"]))

# 			node_search(node_pos["children"][i], None, cursor_start, cursor_end)

# 		else:
# 			pass


def parent_select(node_pos, cursor_start, cursor_end):

	root = {}
	root["children"] = node_pos

	search_space = SearchSpace()

	search_space.node_search(root, None, int(cursor_start), int(cursor_end))
	# print(search_space.visual_select())
	# print(search_space.offset_start)
	# print(search_space.offset_end)
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

	parent_select(data["root"], 138, 143)





# init_tree()
