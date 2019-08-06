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
		# Weigh timing of splitting into lists during search or building list in recipe constructor
		if column in self.recipe_info and needle in self.recipe_info[column]:
				return True
		return False


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
		self.recipe_dict = {}

		self.build_recipe_dict()


	def build_recipe_dict(self):
		self.recipe_dict.clear()

		table = self.get_table()
		for row in table:
			new_recipe = Recipe(row)
			self.recipe_dict[new_recipe.recipe_name] = new_recipe


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
	def add_recipe(self, recipe_name, ingredients, instructions, category,
						meal, prep_time, difficulty, price, ethnicity):
		sql = "INSERT INTO %s VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s');"
		vals = (self.main_table, recipe_name, ingredients, instructions, category,
					meal, prep_time, difficulty, price, ethnicity)
		self.cursor.execute(sql % vals)

		self.mydb.commit()

		if not self.recipe_exists(recipe_name):
			print("The recipe could not be added")
			return False

		#COULD TAKE A LONG TIME
		self.build_recipe_dict()
		return True


	# Purpose: change values in a certain recipe in the database
	# Input: the existing name of the recipe, what you would like the new name to be, and then
	#        all of the "new" recipe information. If you want certain information to stay the same, just input the
	#        same value for that tag
	# Output: 0 on success, -1 if your new name matches another recipe, or if the existing recipe could not be found
	def edit_recipe(self, current_name, new_name, new_ing, new_ins, new_cat, new_meal, new_prep, new_dif, new_price,
	                new_ethnic):
		if not self.recipe_exists(current_name):
			print("Cannot find old recipe")
			return False
		if self.recipe_exists(new_name) and new_name != current_name:
			print("That recipe already exists ")
			return False

		sql = "UPDATE %s SET recipe_name = '%s', ingredients = '%s', instructions = '%s', category = '%s', " \
		      "meal = '%s', prep_time = '%s', difficulty = '%s', price = '%s', ethnicity = '%s' WHERE %s = '%s'"
		vals = (self.main_table, new_name, new_ing, new_ins, new_cat,
		        new_meal, new_prep, new_dif, new_price, new_ethnic, self.key, current_name)

		self.cursor.execute(sql % vals)
		self.mydb.commit()

		#COULD TAKE A LONG TIME
		self.build_recipe_dict()
		return self.recipe_exists(new_name)



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
	# Input: a dictionary of all parameters, with the category as the key
	#   and the value to search for in that category as the value
	# Output: a list of the recipe names that match ALL of the input search parameters
	def filter_recipes(self, search_dict):
		valid_list = self.recipe_dict.values()
		if not (search_dict.get("") == ""):
			for key in search_dict:
				valid_list = self.filter_one_param(search_dict[key], key, valid_list)
		name_list = []
		for recipe in valid_list:
			name_list.append(recipe.recipe_name)

		return name_list


	def filter_one_param(self, column, needle, search_list):
		return_list = []
		for recipe in search_list:
			if recipe.check_category(column, needle):
				return_list.append(recipe)

		return return_list


	def get_recipe(self, recipe_name):
		if recipe_name in self.recipe_dict:
			return self.recipe_dict[recipe_name]




model = RecipeBook("andrew", "password", "localhost", "recipes", "recipes", "ingredients", "recipe_name")
for item in model.get_table():
	print(item)
dict = {
	"cream": "ingredients"
}
list = model.filter_recipes(dict).copy()
print("Final List:")
for item in list:
	print(item)
