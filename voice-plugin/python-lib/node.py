import sys
import json
from ASTNode import ASTNode
from pprint import pprint

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




# init_tree()
