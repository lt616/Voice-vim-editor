import sys
import json
import ast
from pprint import pprint

def node_construct():
	with open("test3.json") as data_file:
		data = json.load(data_file)

	pprint(data)

node_construct()
