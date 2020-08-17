import mysql.connector

MAX_CATEGORY_OPTIONS = 15
NUM_TABLE_CATEGORIES = 9
CATEGORY_SEPARATOR = "|"

class Recipe:
	def __init__(self, table_row):
		if(len(table_row) != NUM_TABLE_CATEGORIES):
			print("Invalid Row")

		self.recipe_name = table_row[0]

		self.recipe_info = {
			"name": table_row[0],
			"ingredients": table_row[1],
			"instructions": table_row[2],
			"category": table_row[3],
			"meal": table_row[4],
			"prep time": table_row[5],
			"difficulty": table_row[6],
			"price": table_row[7],
			"ethnicity": table_row[8]
		}

	def get_info(self, category):
		if category in self.recipe_info:
			return self.recipe_info[category]
		return ""

	def check_category(self, column, needle):
		# Allow for returning all recipes of a certain category
		if needle == "":
			return True
		# Weigh timing of splitting into lists during search or building list in recipe constructor
		if column in self.recipe_info and needle in self.recipe_info[column]:
				return True
		return False

	# Returns a dictionary with the recipe's upper level categories as keys
	# and their lower level contents as values
	def get_categories(self):
		cat_dict = dict(self.recipe_info)
		del cat_dict["name"], cat_dict["ingredients"], cat_dict["instructions"]
		return cat_dict


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

		# Dictionary of all recipe objects in the DB
		self.recipe_dict = {}

		self.build_recipe_dict()

		# Dictionary with each upper level category as a key,
		# and a list of every associated lower level category as its value
		self.category_dict = {}

		self.build_categories()

	# Make every row in the database into a recipe object, and add it to the recipe_dict
	# This is constantly updated to prevent unnecessary database reading
	def build_recipe_dict(self):
		self.recipe_dict.clear()

		table = self.get_table()
		for row in table:
			new_recipe = Recipe(row)
			self.recipe_dict[new_recipe.recipe_name] = new_recipe

	# Make a dictionary with each upper level category a key and every lower level category
	# in the database in a list as the value with its upper level category as the key.
	# Used to fill category_dict instance variable
	def build_categories(self):
		return_dict = {}
		# For each recipe in the database
		for recipe_name in self.recipe_dict:
			rec_obj = self.recipe_dict[recipe_name]
			categories = rec_obj.get_categories()
			# For each high level category in the current recipe
			for key in categories:
				value_list = categories[key].split(",")
				# Only used in first pass to initialize return_dict keys
				if key not in return_dict:
					return_dict[key] = value_list
				else:
					# For each low level value in the recipe that is
					# associated with current high level category
					for value in value_list:
						value = value.strip()
						# if the value has not yet been added, add it
						if value not in return_dict[key]:
							new_list = return_dict[key]
							new_list.append(value)
							return_dict[key] = new_list
		self.category_dict = dict(return_dict)


	def recipe_exists(self, needle_name):
		self.cursor.execute("SELECT %s FROM %s WHERE %s = '%s';"
							% (self.key, self.main_table, self.key, needle_name))
		if len(self.cursor.fetchall()) != 0:
			return True

		return False

	def get_table(self):
		self.cursor.execute("SELECT * FROM %s ORDER BY %s" % (self.main_table, self.key))
		return self.cursor.fetchall()


	# Purpose: Add a row to the recipe database
	# Input: the info for every column in that row, i.e the recipe name, ingredients, instructions, and various tags
	# Output: 0 for success, -1 if not added to the database
	def add_recipe(self, recipe_info):
		sql = "INSERT INTO %s VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s');"
		vals = (self.main_table, recipe_info["name"], recipe_info["ingredients"], recipe_info["instructions"],
					recipe_info["category"], recipe_info["meal"], recipe_info["prep time"],
					recipe_info["difficulty"], recipe_info["price"], recipe_info["ethnicity"])
		print(sql % vals)
		self.cursor.execute(sql % vals)

		self.mydb.commit()

		if not self.recipe_exists(recipe_info["name"]):
			print("The recipe could not be added")
			return False
		print("The recipe has successfully been added")

		#COULD TAKE A LONG TIME
		self.build_recipe_dict()
		self.build_categories()
		return True


	# Purpose: change values in a certain recipe in the database
	# Input: the existing name of the recipe, what you would like the new name to be, and then
	#        all of the "new" recipe information. If you want certain information to stay the same, just input the
	#        same value for that tag
	# Output: 0 on success, -1 if your new name matches another recipe, or if the existing recipe could not be found
	def edit_recipe(self, original_name, recipe_info):
		if not self.recipe_exists(original_name):
			print("Cannot find old recipe")
			return False
		if self.recipe_exists(recipe_info["name"]) and recipe_info["name"] != original_name:
			print("That recipe already exists ")
			return False

		sql = "UPDATE %s SET recipe_name = '%s', ingredients = '%s', instructions = '%s', category = '%s', " \
		      "meal = '%s', prep_time = '%s', difficulty = '%s', price = '%s', ethnicity = '%s' WHERE %s = '%s'"
		vals = (self.main_table, recipe_info["name"], recipe_info["ingredients"], recipe_info["instructions"], recipe_info["category"],
		        recipe_info["meal"], recipe_info["prep time"], recipe_info["difficulty"], recipe_info["price"], recipe_info["ethnicity"], self.key, original_name)

		self.cursor.execute(sql % vals)
		self.mydb.commit()

		if not self.recipe_exists(recipe_info["name"]):
			print("The recipe could not be added")
			return False
		print("The recipe has been successfully edited")

		# COULD TAKE A LONG TIME BUT BETTER SAFE THAN SORRY
		self.build_recipe_dict()
		self.build_categories()
		return True


	# Purpose: remove a certain recipe from the database
	# Input: the name of the recipe
	# Output: 0 if deleted or -1 if the recipe was already not in the database
	def delete_recipe(self, recipe_name):
		self.cursor.execute("SELECT %s FROM %s WHERE %s = '%s';"
							% (self.key, self.main_table, self.key, recipe_name))
		if len(self.cursor.fetchall()) == 0:
			print("That recipe is not in the database")
			return False
		self.cursor.execute("DELETE FROM %s WHERE %s = '%s' LIMIT 1" % (self.ref_table, self.key, recipe_name))
		self.cursor.execute("DELETE FROM %s WHERE %s = '%s' LIMIT 1" % (self.main_table, self.key, recipe_name))

		self.mydb.commit()

		if self.recipe_exists(recipe_name):
			print("The recipe could not be deleted")
			return False

		# COULD TAKE A LONG TIME
		self.build_recipe_dict()
		return True


	# Purpose: filter through recipes to find all those that match ALL of the parameters
	#           Really more for the multiple ingredient search function
	# Input: a dictionary of all parameters, with the category as the key
	#   and the value to search for in that category as the value
	# Output: a list of the recipe names that match ALL of the input search parameters
	def filter_recipes(self, search_dict):
		valid_list = self.recipe_dict.values()
		#check if search_dict is empty and you should just return all recipes
		if not (search_dict.get("") == ""):
			for key in search_dict:
				# maybe switch order of key/ value?
				print("key: ", key, " value: ", search_dict[key])
				valid_list = self.filter_one_param(key, search_dict[key], valid_list)

		name_list = []
		for recipe in valid_list:
			name_list.append(recipe.recipe_name)

		return name_list

	# Return all recipes that match a single search term
	def filter_one_param(self, column, needle, search_list):
		return_list = []
		for recipe in search_list:
			if recipe.check_category(column, needle):
				print(recipe.recipe_name)
				return_list.append(recipe)

		return return_list

	# Does simple search of recipe names
	def name_search(self, search_list):
		return_list = []
		for recipe in self.recipe_dict:
			for word in search_list:
				if word in recipe:
					return_list.append(recipe)
		return return_list

	def get_recipe(self, recipe_name):
		if recipe_name in self.recipe_dict:
			return self.recipe_dict[recipe_name]
		else:
			print("Can't find recipe")

	def get_category_values(self, upper_level_cat):
		return self.category_dict[upper_level_cat]





model = RecipeBook("andrew", "password", "localhost", "recipes", "recipes", "ingredients", "recipe_name")
for item in model.get_table():
	print(item)
#dict = {
# 	"cream": "ingredients"
# }
# list = model.filter_recipes(dict).copy()
#print("Final List:")
#for item in list:
	#print(item)
