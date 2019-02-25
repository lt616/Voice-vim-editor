import sys
import json
from ASTNode import ASTNode
from pprint import pprint

def tree_construct(data, parent, next_node):
	cur_node = ASTNode(data)
	cur_node.set_parent(parent)
	# cur_node.set_end_pos(next_node)

	children = data["children"]
	for i in range(0, len(children)):
		next_child = None if i == len(children) - 1 else children[i + 1]
		tree_construct(children[i], cur_node, next_child)


def init_tree():
	with open("test3.json") as data_file:
		data = json.load(data_file)

	pprint(data)

	tree_construct(data["root"][0], None, None)




init_tree()
