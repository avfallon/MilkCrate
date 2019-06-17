import mysql.connector

MAX_CATEGORY_OPTIONS = 15
NUM_TABLE_CATEGORIES = 9

class Recipe:
	def __init__(self, table_row):
		if(len(table_row) != NUM_TABLE_CATEGORIES):
			print("Invalid Row")
		self.recipe_name = table_row(0)
		self.ingredients = table_row(1)
		self.


		print(table_row)
		print("\n ^ thats a row")
		#self.recipe_name = recipe_id

	def contains_ing(self, ingredient):
		pass

	def check_category(self, column, needle):
		pass




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

		#list of all recipe objects in the DB
		self.recipe_list = []

		self.build_recipe_list()

	def build_recipe_list(self):
		self.recipe_list = []

		table = self.get_table()
		for row in table:
			new_recipe = Recipe(row)
			self.recipe_list.append(new_recipe)


	def get_table(self):
		self.cursor.execute("SELECT * FROM %s ORDER BY recipe_name" % (self.main_table))
		return self.cursor.fetchall()


	# Purpose: Add a row to the recipe database
	# Input: the info for every column in that row, i.e the recipe name, ingredients, instructions, and various tags
	# Output: 0 for success, -1 if not added to the database
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




	# Purpose: remove a certain recipe from the database
	# Input: the name of the recipe
	# Output: 0 if deleted or -1 if the recipe was already not in the database
	def delete_recipe(self, recipe_name):
		self.cursor.execute("SELECT %s FROM %s WHERE %s = '%s';"
							% (self.key, self.main_table, self.key, recipe_name))
		if len(self.cursor.fetchall()) == 0:
			print("That recipe is not in the database")
			return -1
		self.cursor.execute("DELETE FROM %s WHERE %s = '%s' LIMIT 1" % (self.ref_table, self.key, recipe_name))
		self.cursor.execute("DELETE FROM %s WHERE %s = '%s' LIMIT 1" % (self.main_table, self.key, recipe_name))
		self.mydb.commit()
		return 0


	# Purpose: change values in a certain recipe in the database
	# Input: the existing name of the recipe, what you would like the new name to be, and then
	#        all of the "new" recipe information. If you want certain information to stay the same, just input the
	#        same value for that tag
	# Output: 0 on success, -1 if your new name matches another recipe, or if the existing recipe could not be found
	def edit_recipe(self, current_name, new_name, new_ingr, new_instr, new_cat,
						new_meal, new_time, new_dif, new_price, new_ethn):

		# Check if old recipe exists
		self.cursor.execute("SELECT %s FROM %s WHERE %s = '%s';"
		                    % (self.key, self.main_table, self.key, recipe_name))
		if len(self.cursor.fetchall()) == 0:
			print("That recipe is not in the database")
			return -1

		# Check if new name is already taken
		if new_name != current_name:
			self.cursor.execute("SELECT %s FROM %s WHERE %s = '%s';"
								% (self.key, self.main_table, self.key, new_name))
			if len(self.cursor.fetchall()) != 0:
				print("Your new recipe name must not match any existing recipes")
				return -1

		# Set new values
		sql = "UPDATE %s SET recipe_name = '%s', ingredients = '%s', instructions = '%s', category = '%s', " \
			"meal = '%s', prep_time = '%s', difficulty = '%s', price = '%s', ethnicity = '%s' WHERE %s = '%s'"
		vals = (self.main_table, new_name, new_ingr, new_instr, new_cat,
				new_meal, new_time, new_dif, new_price, new_ethn, self.key, current_name)
		self.cursor.execute(sql % vals)

		self.mydb.commit()
		return 0

	# Purpose: return a list of every ingredient in a recipe
	# Input: the name of the recipe
	# Output: a list of the ingredients in a recipe (An empty list if the recipe was not found)
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

	# Purpose: Determine which recipes contain ALL ingredients in a given list
	# Input: List of ingredients that must be contained in the recipes
	# Output: a list of all recipes that use all the given ingredients
	def filter_by_ing(self, search_list):
		final_recipe_list = []
		list_instantiated = False
		table = self.get_table()

		for item in search_list:
			temp_recipe_list = []
			print("first   %s" % item)
			for row in table:
				recipe_name = row[0]
				ing_list = self.split_ing(recipe_name)

				if item in ing_list:
					temp_recipe_list.append(recipe_name)

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

		return final_recipe_list

	# Purpose: return a list of all recipes matching ALL given parameters
	#          (e.g. every recipe that is $$ AND Indian AND uses potatoes AND carrots)
	# Input: List of columns that must be checked, and a list of the accompanying values to check for in those columns
	# Output: A list of recipe names that match the parameters (Strings)
	def filter_recipes(self, column_list, value_list):
		val_iter = iter(value_list)
		final_recipe_list = []
		list_instantiated = False

# TODO add ingredient filtering
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
#model.add_recipe("Tiramisu3", "milk \n butter", "test3", "cat", "meal", "time", "dif", "price", "ethn")
#model.delete_recipe("Tiramisu1")
#model.edit_recipe("filterTest2", "newName", "2", "3", "4", "5", "6", "7", "8", "9")
list = model.split_ing("Tiramisu")
print(list)
col = ["ingredients", "category"]
ing = [""]
val = ['ing', 'cat']
print(model.filter_recipes(col, val))
print("\nFULL TABLE")
for row_ in model.get_table():
	print(row_)

print("printing %s" % model.filter_by_ing(['butter', 'cream']))


	## FIX ME: add error checking for add/delete, have an if that can return false


