import os
import pandas as pd
import random
import string


class RentalShop(object):
	"""
	This class is used to represent a car rental shop, allowing customers to request for stock, hire a car to rent,
	and make returns.
	"""

	def __init__(self, shop_id):
		"""
		Used to initialise a new RentalShop instance.

		:param shop_id: a unique string identifier for the rental shop, which will be used to locate the rental shop's
		database system for managing its stock and rentals.
		"""

		self.__shop_id = shop_id
		"""
		Represents a connection to the rental shop's database, used to make queries on it as well as update it.
		"""

		# Set up a new database if it already does exist.
		self.__check_db_exists()

	def display_stock(self):
		"""
		Outputs the current available stock of each car type, as well as pricing for each type.
		"""

		# Import the cars, rentals, and car_types files from the database
		cars = self._get_data(_CARS)
		rentals = self._get_data(_CAR_RENTALS)
		car_types = self._get_data(_CAR_TYPES)

		# Consider only the non-rented cars - these will be considered the ones that are available to rent.
		available_cars = cars.drop(rentals.index)

		# If it turns out that there are none that are available, notify the user/customer.
		if len(available_cars) == 0:
			print("Sorry, there are currently no cars available for rent.")

		# Otherwise, output the available stock.
		else:
			# Create a new DataFrame showing the number of available cars of EACH car_type.
			car_type_stock = available_cars.groupby("car_type").size()

			"""
			Output the stock as a "pretty-printed" table, showing the number of cars of each type that are available to
			rent.
			"""
			output_stock = pd.DataFrame(car_type_stock).reset_index().to_string(
				index=False, header="")
			print("\nAvailable car types to rent and their stock:\n\n" + output_stock)

		"""
		Output the pricing information of each car type as a "pretty-printed" table, showing the following daily rates:
		- Under a week
		- At least one week.
		- VIP customers
		"""
		output_prices = car_types.to_string(
			header=[
				"", "<1w", "1w+", "VIP"
			],
			index=False, col_space=10,
			float_format="{:.2f}".format    # (Display the strings with 2 decimal places)
		)
		print("\nPricing information for every car type (daily rates, in GBP):\n"+output_prices+"\n")

		# len_max = max(map(len, car_type_stock.index))
		#
		# for c_type in car_type_stock.index:
		# 	print(
		# 		f"{c_type.rjust(len_max)}: {car_type_stock[c_type]}"
		# 	)
		#
		# print("\nPricing information:")
		# print(car_types.)

	def process_request(self, customer_number, car_type, days):
		pass

	def issue_bill(self, customer_number):
		pass

	# ====== AUXILIARY METHODS ======

	def __check_db_exists(self, create=True):
		"""
		To be called during initialisation to check whether a database for the shop actually exists.
		If not, and the create parameter is set to True, then a default version is set up.

		:param create: a flag used to determine if a new database should be created if it turns out that one does
		not already exist. By default, it is True, indicating that a new one will be created.

		:return: True if it does already exist, False otherwise.
		"""

		# Construct the directory where the shop's database is expected to be located at.
		db_dir = f"./{_DATABASE_DIRECTORY}/{self.__shop_id}"

		# If the directory already exists, do nothing more and output True.
		if os.path.isdir(db_dir):
			return True
		else:
			# If it does not already exist and the create parameter is True, then setup new files representing the
			# database.
			if create:
				os.makedirs(db_dir, exist_ok=True)
				# Setup for the 'cars' table
				_setup_cars(db_dir)
				# Setup for the 'car_rentals' table
				_setup_rentals(db_dir)
				# Setup for the 'car_types' table
				_setup_car_types(db_dir)
			return False

	def _get_data(self, name):
		"""
		Used to import one of the rental shop's database files.
		:param name: the name of the file to use (either 'cars', 'car_types', or 'car_rentals')
		:return: a DataFrame object representing the imported database file.
		"""

		# Construct the path to the data file.
		path = f"./{_DATABASE_DIRECTORY}/{self.__shop_id}/{name}.csv"

		# Read the data, constructing a DataFrame out of it and then returning it.
		return pd.read_csv(path)


# ========== DATABASE SETUP FUNCTIONS ==========
def _setup_cars(file_dir):
	"""
	Sets up a default file to store all the cars that exist in the rental shop.
	:param file_dir: the directory to store the file.
	:return: None
	"""

	"""
	Format of the file:

	car_id (ID): an identifier for a car. Will have a format similar to a numberplate.
	car_type: the type of the car. Can either be a hatchback, sedan, or suv.
	
	Example:
	-----------------
	car_id  car_type
	-----------------
	HN56XNF hatchback
	BA72LTQ     sedan
	EC21NKS     sedan
	LU71YPQ       suv
	...
	"""

	# Initial data will consist of 10 cars (4 hatchbacks, 3 sedans, 3 SUVs), with random IDs will be assigned to each.
	data = {
		"car_id": _random_car_ids(10),
		"car_type": [
			'hatchback', 'sedan', 'sedan', 'suv', 'suv',
			'hatchback', 'hatchback', 'hatchback', 'sedan', 'suv'
		],
	}

	# Create a DataFrame out of the above dictionary representing the car dataset.
	cars = pd.DataFrame(data).set_index("car_id")

	# Create a CSV file out of the DataFrame. The name of the file will be "cars.csv"
	cars.to_csv(f"{file_dir}/{_CARS}.csv")


def _setup_rentals(file_dir):
	"""
	Sets up a default file to store all the current car rentals.
	:param file_dir: the directory to store the file.
	:return: None
	"""

	"""
	Format of the file:

	car_id (ID): an identifier for the car being rented. Will have a format similar to a numberplate.
	customer_number : an identifier for the customer who rented the car.
	rate: the daily rate (in pounds) for the car being rented.
	days: the number of days the car is rented for.
	
	Example:
	---------------------------------
	car_id  customer_number rate days
	---------------------------------
	EW23FBN          018974   40    8
	HN56XNF          052581   30    5
	...
	"""

	data = {
		"car_id": [],
		"customer_number": [],
		"rate": [],
		"days": []
	}

	# Create a DataFrame out of the above dictionary representing the car rentals dataset.
	rentals = pd.DataFrame(data).set_index("car_id")

	# Create a CSV file out of the DataFrame. The name of the file will be "car_rentals.csv"
	rentals.to_csv(f"{file_dir}/{_CAR_RENTALS}.csv")


def _setup_car_types(file_dir):
	"""
	Sets up a default file to store the pricing of each of the different car types in the rental shop.
	:param file_dir: the directory to store the file.
	:return: None
	"""

	"""
	Format of the file:

	type_name (ID): the name of the car type
	short_term_rate: the daily rate charged for renting the car for less than a week
	long_term_rate: the daily rate charged for renting the car for one week or more.
	vip_rate: the daily rate charged for VIP customers.
	
	
	The expected dataset:
	--------------------------------------------------
	type_name  short_term_rate long_term_rate vip_rate
	--------------------------------------------------
	hatchback             30.0           50.0    100.0
	sedan                 25.0           40.0     90.0
	suv                   20.0           35.0     80.0
	"""

	data = {
		"type_name": ["hatchback", "sedan", "suv"],
		"short_term_rate": [30.0, 50.0, 100.0],
		"long_term_rate":  [25.0, 40.0, 90.0],
		"vip_rate":        [20.0, 35.0, 80.0]
	}

	# Create a DataFrame out of the above dictionary representing the car types dataset.
	car_types = pd.DataFrame(data).set_index("type_name")

	# Create a CSV file out of the DataFrame. The name of the file will be "car_types.csv"
	car_types.to_csv(f"{file_dir}/{_CAR_TYPES}.csv")


# ========== AUXILIARY FUNCTIONS ==========

def _random_car_ids(n, seed=0):
	"""
	A function used to set up a given number of random IDs to be assigned to cars.
	They will be of the form 'LLddLLL', where
	- L is a random upper-case letter (A-Z)
	- d is a random digit (0-9).
	(Similar to the format of a numberplate)

	:param n: The number of IDs to generate.
	:param seed: the seed to use for the random generator (for reproducibility purposes). By default it is 0.
	:return: A list of n strings representing randomly generated car ids of the form above.
	"""

	def rand_letters(m):
		"""
		A "helper" function to generate a random set of letters (A-Z).
		:param m: the number of letters to generate
		:return: A list of m randomly generated letters.
		"""
		return random.choices(string.ascii_uppercase, k=m)

	def rand_digits(m):
		"""
		A "helper" function to generate a random set of digits (0-9).
		:param m: the number of letters to generate
		:return: A list of m randomly generated digits (represented as strings).
		"""
		return random.choices(string.digits, k=m)

	# Initialise new list to store the ids.
	id_list = []

	# Initialise random generator with given seed.
	random.seed(seed)

	# Iterate n times to create n ids
	for i in range(n):
		# Create a random id consisting of 2 letters, followed by 3 digits, followed by 3 letters.
		car_id = "".join(rand_letters(2) + rand_digits(3) + rand_letters(3))
		# Add it to the list.
		id_list.append(car_id)

	# Output the list, now filled with random IDs.
	return id_list


# === CONSTANTS ===

# Represents the name of the parent directory where shop databases are stored in.
_DATABASE_DIRECTORY = ".databases"

# The names (ignoring file extension) of each of the database files.
_CARS = "cars"
_CAR_RENTALS = "car_rentals"
_CAR_TYPES = "car_types"
