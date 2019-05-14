import mysql.connector


class RecipeBook:
	# How could I make the columns more generic?
	def __init__(self, username, password, host, database, main_table, referencing_table, key):
		self.mydb = mysql.connector.connect(
			user=username,
			password=password,
			host=host,
			database=database,
		)
		self.db = database
		self.cursor = self.mydb.cursor()
		self.main_table = main_table
		self.ref_table = referencing_table
		# Key for this table is the recipe name, all recipe names must be unique
		self.key = key

	def get_table(self):
		self.cursor.execute("SELECT * FROM %s" % (self.main_table))
		return self.cursor.fetchall()

	def add_recipe(self, recipe_name, ingredients, instructions, category,
						meal, prep_time, difficulty, price, ethnicity):
		sql = "INSERT INTO %s VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s');"
		vals = (self.main_table, recipe_name, ingredients, instructions, category,
					meal, prep_time, difficulty, price, ethnicity)
		self.cursor.execute(sql % vals)

		self.mydb.commit()

		self.cursor.execute("SELECT recipe_name FROM %s WHERE recipe_name = '%s';"
		                    % (self.main_table, recipe_name))
		if (len(self.cursor.fetchall()) == 0):
			print("The recipe could not be added")
			return -1

		return 0


	# def add_to_ingredients(self, recipe_name, ingredients_str, split_pattern):
	# 	self.cursor.execute("SELECT column_name FROM information_schema.columns WHERE "
	# 	                     " table_name = '%s' AND table_schema = '%s'" % (self.ref_table, self.db))
	# 	full_col_list = self.cursor.fetchall()
	# 	for line in ingredients_str.split(split_pattern):
	# 		column_matches = []
	# 		for word in line.split():
	# 			for col_tuple in full_col_list:
	# 				for column in col_tuple:
	# 					if '_' in column:
	# 						word_list = column.split('_')
	#
	#
	# 					else:
	#
	# 					for item in word_list:
	# 						if item == word.lower():
	# 							column_matches.append(column)




	def delete_recipe(self, recipe_name):
		self.cursor.execute("SELECT %s FROM %s WHERE %s = '%s';"
		                    % (self.key, self.main_table, self.key, recipe_name))
		if(len(self.cursor.fetchall()) == 0):
			print("That recipe is not in the database")
			return -1
		self.cursor.execute("DELETE FROM %s WHERE %s = '%s' LIMIT 1" % (self.ref_table, self.key, recipe_name))
		self.cursor.execute("DELETE FROM %s WHERE %s = '%s' LIMIT 1" % (self.main_table, self.key, recipe_name))
		self.mydb.commit()
		return 0

	def edit_recipe(self, current_name, new_name, new_ingr, new_instr, new_cat,
						new_meal, new_time, new_dif, new_price, new_ethn):
		if(new_name != current_name):
			self.cursor.execute("SELECT %s FROM %s WHERE %s = '%s';"
			                    % (self.key, self.main_table, self.key, new_name))
			if len(self.cursor.fetchall()) != 0:
				print("Your new recipe name must not match any existing recipes")
				return -1

		sql = "UPDATE %s SET recipe_name = '%s', ingredients = '%s', instructions = '%s', category = '%s', " \
		      "meal = '%s', prep_time = '%s', difficulty = '%s', price = '%s', ethnicity = '%s' WHERE %s = '%s'"
		vals = (self.main_table, new_name, new_ingr, new_instr, new_cat,
		        new_meal, new_time, new_dif, new_price, new_ethn, self.key, current_name)
		self.cursor.execute(sql % vals)

		self.mydb.commit()
		return 0

	def split_ing(self, recipe_name):
		ing_list = []
		self.cursor.execute("SELECT ingredients FROM %s WHERE %s = '%s';"
		                    % (self.main_table, self.key, recipe_name))
		fetch_list = self.cursor.fetchall()
		if len(fetch_list) == 0:
			print("That recipe is not in the database")
			return ing_list
		ing_str = fetch_list[0][0]
		split_list = ing_str.split('\n')
		for item in split_list:
			ing_list.append(item.strip())
		return ing_list


	#def filter_by_ing(self, ing_list):


	#Purpose: return a list of all recipes matching given parameters (e.g. all recipes tagged as indian, cheap
	def filter_recipes(self, column_list, value_list):
		val_iter = iter(value_list)
		final_recipe_list = []
		list_instantiated = False

		for column in column_list:
			temp_recipe_list = []
			self.cursor.execute("SELECT %s FROM %s WHERE %s = '%s';" % (self.key, self.main_table, column, next(val_iter)))

			for tuple in self.cursor.fetchall():
				for recipe in tuple:
					temp_recipe_list.append(recipe)
			if not list_instantiated:
				final_recipe_list = temp_recipe_list
				list_instantiated = True

			else:
				removal_list = []
				for recipe in final_recipe_list:
					if not temp_recipe_list.__contains__(recipe):
						removal_list.append(recipe)
				for recipe in removal_list:
					final_recipe_list.remove(recipe)

		final_recipe_list.sort()
		return final_recipe_list



model = RecipeBook("andrew", "password", "localhost", "recipes", "recipes", "ingredients", "recipe_name")
#model.add_recipe("Tiramisu1", "cream \n milk", "test3", "cat", "meal", "time", "dif", "price", "ethn")
#model.delete_recipe("Tiramisu1")
#model.edit_recipe("filterTest2", "newName", "2", "3", "4", "5", "6", "7", "8", "9")
list = model.split_ing("Tiramisu")
print(list)
col = ["ingredients", "category"]
ing = [""]
val = ['ing', 'cat']
print(model.filter_recipes(col, val))
for row in model.get_table():
	print(row)


	## FIX ME: add error checking for add/delete, have an if that can return false


