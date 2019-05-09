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

		self.cursor_start = cursor_start  # cursor_line when searching node
		self.cursor_end = cursor_end	# cursor_col when searching node

		self.err_msg = err_msg

		self.reach_cursor = False

		self.condition_nums = {"if": 1, "switch": 1, "for": 3, "while": 1}
		self.condition_stmts = {"if": "IfStmt", "switch": "SwitchStmt", "for": "ForStmt", "while": "WhileStmt"}

		self.before_cursor_results = []
		self.after_cursor_results = []

		self.line_results = {}

	def visual_select(self, err_str):
		if self.res_line_start == -1 and self.res_col_end == -1:
			# exception.print_error(err_str)
			return "echo \"" + "Error: " + self.err_msg + "\""

		if self.res_line_end == -1 or self.res_col_end == -1:
			# return "normal! " + str(self.res_line_start) + "G " + str(self.res_col_start) + "| v " + "G$"
			return "normal! " + str(self.offset_start) + "go v " + "G$"
		else:
			# return "normal! " + str(self.res_line_start) + "G " + str(self.res_col_start) + "| v " + str(self.res_line_end) + "G " + str(self.res_col_end) + "|" 
			return "normal! " + str(self.offset_start) + "go v " + str(self.offset_end) + "go"

	def return_all_results(self):
		return self.after_cursor_results + self.before_cursor_results

	def set_result(self, node_pos):
		if node_pos is None:
			self.res_line_start = -1
			self.res_col_start = -1
			self.offset_start = self.cursor_start

			self.res_line_end = -1
			self.res_col_end = -1
			self.offset_end = self.cursor_end
			return

		self.res_line_start = node_pos["line"]
		self.res_col_start = node_pos["column"]
		self.offset_start = node_pos["offset"]

		self.res_line_end = node_pos["end"]["line"]
		self.res_col_end = node_pos["end"]["column"]
		self.offset_end = node_pos["end"]["offset"]
 

	def set_dict_result(self, node_pos):
		temp = {}
		temp["start_line"] = node_pos["line"]
		temp["start_column"] = node_pos["column"]
		temp["start_offset"] = node_pos["offset"]

		temp["end_line"] = node_pos["end"]["line"]
		temp["end_column"] = node_pos["end"]["column"]
		temp["end_offset"] = node_pos["end"]["offset"]

		return temp

	def compare_line_col(self, x_line, x_col, y_line, y_col):
		if x_line < y_line:
			return -1
		elif x_line > y_line:
			return 1
		else:
			if x_col < y_col:
				return -1
			elif x_col > y_col:
				return 1
			return 0

	def check_condition(self, node_pos, keywords):
		for word in keywords.keys():
			if ("spell" in node_pos and node_pos["spell"] == word) or ("value" in node_pos and node_pos["value"]) == word:
				keywords[word] = True

		for child in node_pos["children"]:
			self.check_condition(child, keywords)

	def check_condition_inline(self, node_pos, keywords, line):
		if node_pos["line"] != line:
			return 

		for word in keywords.keys():
			if ("spell" in node_pos and node_pos["spell"] == word) or ("value" in node_pos and node_pos["value"]) == word:
				keywords[word] = True

		for child in node_pos["children"]:
			self.check_condition(child, keywords)


	def check_conditions(self, node_pos, keywords, num_cond):
		if num_cond > len(node_pos["children"]):
			return False

		for i in range(0, num_cond):
			self.check_condition(node_pos["children"][i], keywords)

		for key in keywords.keys():
			if not keywords[key]:
				return False

		return True


	def check_inline_conditions(self, node_pos, keywords):
		if "spell" in node_pos and node_pos["spell"].lower() in keywords:
			keywords[node_pos["spell"]][int(node_pos["line"])] = True
		elif "value" in node_pos and node_pos["value"].lower() in keywords:
			keywords[node_pos["value"]][int(node_pos["line"])] = True

		for child in node_pos["children"]:
			self.check_inline_conditions(child, keywords)


	def check_inline_node_conditions(self, node_pos, keywords, line):
		self.check_condition_inline(node_pos, keywords, line)

		res = True

		for key in keywords.keys():
			if not keywords[key]:
				res = False
			keywords[key] = False

		return res


	def current_search(self, node_pos, line_start, column_start, line_end, column_end, node_parent):

		for child in node_pos["children"]:
			start_compare = self.compare_line_col(int(child["line"]), int(child["column"]), int(line_start), int(column_start))
			end_compare = self.compare_line_col(int(child["end"]["line"]), int(child["end"]["column"]), int(line_end), int(column_end))
			if (start_compare == 0 or start_compare == -1) and (end_compare == 0 or end_compare == 1):
				self.current_search(child, line_start, column_start, line_end, column_end, child)
				return

			# if self.compare_line_col(int(child["start"]["line"]), int(child["start"]["column"]), line_end, column_end) == 1:
			# 	print(1)
			# 	self.set_result(None)
			# 	return

			if self.compare_line_col(int(child["end"]["line"]), int(child["end"]["column"]), int(line_start), int(column_start)) == -1:
				continue;

		if node_parent is None or "line" not in node_parent:
			self.set_result(None)
		else:
			self.set_result(node_parent)


	def parent_search(self, node_pos):
		for child in node_pos["children"]: 
			if int(child["offset"]) == self.cursor_start and int(child["end"]["offset"]) == self.cursor_end:
				self.set_result(node_pos)
				return
			
			if int(child["offset"]) > self.cursor_end:
				self.set_result(None)
				return

			if int(child["end"]["offset"]) < self.cursor_start:
				continue;

			self.parent_search(child)
			return


	def child_search(self, node_pos):
		for child in node_pos["children"]: 
			if int(child["offset"]) == self.cursor_start and int(child["end"]["offset"]) == self.cursor_end:
				if child["children"] is []:
					self.set_result(None)
				else:
					self.set_result(child["children"][0])
				return
			
			if int(child["offset"]) > self.cursor_end:
				self.set_result(None)
				return

			if int(child["end"]["offset"]) < self.cursor_start:
				continue;

			self.child_search(child)
			return

	def next_sibling_search(self, node_pos):
		children = node_pos["children"]
		for i in range(len(children)): 

			if int(children[i]["offset"]) == self.cursor_start and int(children[i]["end"]["offset"]) == self.cursor_end:
				if i == len(children) - 1:
					self.set_result(None)
				else:
					self.set_result(children[i + 1])
				return
			
			if int(children[i]["offset"]) > self.cursor_end:
				self.set_result(None)
				return

			if int(children[i]["end"]["offset"]) < self.cursor_start:
				continue;

			self.next_sibling_search(children[i])
			return


	def prev_sibling_search(self, node_pos):
		children = node_pos["children"]
		for i in range(len(children)): 
			if int(children[i]["offset"]) == self.cursor_start and int(children[i]["end"]["offset"]) == self.cursor_end:
				if i == 0:
					self.set_result(None)
				else:
					self.set_result(children[i - 1])
				return
			
			if int(children[i]["offset"]) > self.cursor_end:
				self.set_result(None)
				return

			if int(children[i]["end"]["offset"]) < self.cursor_start:
				continue;

			self.prev_sibling_search(children[i])
			return


	def var_search(self, node_pos, var_name):
		for child in node_pos["children"]:
			if not self.reach_cursor:
				if self.compare_line_col(int(child["line"]), int(child["column"]), self.cursor_start, self.cursor_end) >= 0:
					self.reach_cursor = True

			if "kind" in child and child["kind"] == "DeclRefExpr" and "spell" in child and child["spell"].lower() == var_name:
				if self.reach_cursor:
					self.after_cursor_results.append(self.set_dict_result(child))
				else:
					self.before_cursor_results.append(self.set_dict_result(child))

			self.var_search(child, var_name)


	def decl_search(self, node_pos, var_name):
		for child in node_pos["children"]:
			if not self.reach_cursor:
				if self.compare_line_col(int(child["line"]), int(child["column"]), self.cursor_start, self.cursor_end) >= 0:
					self.reach_cursor = True

			if "kind_type" in child and child["kind_type"] == "Declaration" and "spell" in child and child["spell"].lower() == var_name:
				if self.reach_cursor:
					self.after_cursor_results.append(self.set_dict_result(child))
				else:
					self.before_cursor_results.append(self.set_dict_result(child))

			self.decl_search(child, var_name)


	def cond_search(self, node_pos, keywords, cond):
		for child in node_pos["children"]:
			if not self.reach_cursor:
				if self.compare_line_col(int(child["line"]), int(child["column"]), self.cursor_start, self.cursor_end) >= 0:
					self.reach_cursor = True

			if "kind" in child and child["kind"] == self.condition_stmts[cond] and self.check_conditions(child, keywords, self.condition_nums[cond]):
				if self.reach_cursor:
					self.after_cursor_results.append(self.set_dict_result(child))
				else:
					self.before_cursor_results.append(self.set_dict_result(child))

			self.cond_search(child, keywords, cond)


	def inline_search(self, node_pos, keywords):
		for child in node_pos["children"]:
			self.check_inline_conditions(node_pos, keywords)

		_, line_list = keywords.popitem()

		for line in line_list.keys():
			line_flag = True
			for keyword in keywords.keys():
				if line not in keywords[keyword]:
			 		line_flag = False
			 		break

			if line_flag:
				if line < self.cursor_start:
					self.before_cursor_results.append(line)
				else:
					self.after_cursor_results.append(line)

		self.before_cursor_results.sort()
		self.after_cursor_results.sort()


	def inline_node_search(self, node_pos, keywords):
		new_keywords = {}
		for keyword in keywords.keys():
			new_keywords[keyword] = False

		for child in node_pos["children"]:
			self.check_inline_conditions(node_pos, keywords)

		_, line_list = keywords.popitem()

		for line in line_list.keys():
			line_flag = True
			for keyword in keywords.keys():
				if line not in keywords[keyword]:
			 		line_flag = False
			 		break

			if line_flag:
				self.line_results[line] = True

		self.extract_node_line(node_pos, new_keywords)

	def extract_node_line(self, node_pos, keywords):
		res = False
		for child in node_pos["children"]:
			if not self.reach_cursor:
				if self.compare_line_col(int(child["line"]), int(child["column"]), self.cursor_start, self.cursor_end) >= 0:
					self.reach_cursor = True

			# if child selected early exit
			if self.extract_node_line(child, keywords):
				res = True
				continue

			if int(child["line"]) in self.line_results:
				if self.check_inline_node_conditions(child, keywords, child["line"]):
					if self.reach_cursor:
						self.after_cursor_results.append(self.set_dict_result(child))
					else:
						self.before_cursor_results.append(self.set_dict_result(child))

					res = True
		return res








# virtual select
def node_select(node_pos): 

	start_line = node_pos["start"]["line"]
	start_col = node_pos["start"]["column"]
	end_line = node_pos["end"]["line"]
	end_col = node_pos["end"]["column"]

	return "normal! " + str(start_line) + "G " + str(start_col) + "| 2h v " + str(end_line) + "G " + str(end_col) + "|" 

def current_select(node_pos, line_start, column_start, line_end, column_end):
	root = {}
	root["children"] = node_pos

	search_space = SearchSpace(0, 0, "Current position is not a valid node.")
	search_space.current_search(root, line_start, column_start, line_end, column_end, None)

	return search_space.offset_start, search_space.offset_end, search_space.visual_select("Error: Current position is not a valid node.")


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


def variable_search(node_pos, cursor_line, cursor_col, var_name):
	root = {}
	root["children"] = node_pos

	search_space = SearchSpace(int(cursor_line), int(cursor_col), "No result.")
	search_space.var_search(root, var_name)

	return -2, -2, search_space.return_all_results()


def declaration_search(node_pos, cursor_line, cursor_col, var_name):
	root = {}
	root["children"] = node_pos

	search_space = SearchSpace(int(cursor_line), int(cursor_col), "No result.")
	search_space.decl_search(root, var_name)

	return -2, -2, search_space.return_all_results()


def condition_search(node_pos, cursor_line, cursor_col, keywords, cond):
	root = {}
	root["children"] = node_pos

	search_space = SearchSpace(int(cursor_line), int(cursor_col), "No result.")
	search_space.cond_search(root, keywords, cond)

	return -2, -2, search_space.return_all_results()


def inline_search(node_pos, cursor_line, cursor_col, keywords):
	root = {}
	root["children"] = node_pos

	search_space = SearchSpace(int(cursor_line), int(cursor_col), "No result.")
	search_space.inline_search(root, keywords)

	return -3, -3, search_space.return_all_results()


def inline_node_search(node_pos, cursor_line, cursor_col, keywords):
	root = {}
	root["children"] = node_pos

	search_space = SearchSpace(int(cursor_line), int(cursor_col), "No result.")
	search_space.inline_node_search(root, keywords)

	return -2, -2, search_space.return_all_results()









# def tree_construct(data, parent, next_node, next_uncle):
# 	cur_node = ASTNode(data)
# 	cur_node.set_parent(parent)
# 	# cur_node.set_end_pos(next_node)
# 	if not next_node is None:
# 		cur_node.set_end_pos(next_node)
# 	else:
# 		cur_node.set_end_pos(next_uncle)

# 	children = data["children"]
# 	for i in range(0, len(children)):
# 		next_child = None if i == len(children) - 1 else children[i + 1]
# 		tree_construct(children[i], cur_node, next_child, next_node)


# def init_tree():
# 	with open("test3.json") as data_file:
# 		data = json.load(data_file)

# 	pprint(data)

# 	tree_construct(data["root"][0], None, None, None)


with open("hello.txt") as data_file:
	data = json.load(data_file)

	print(inline_node_search(data["root"], 1, 1, {'i': {}}))





# init_tree()