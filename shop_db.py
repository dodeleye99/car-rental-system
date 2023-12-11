import os
import random
import string

import pandas as pd


# === CONSTANTS ===

# Represents the name of the parent directory where shop databases are
# stored in.
_DATABASE_DIRECTORY = ".databases"

# The names (ignoring file extension) of each of the database files.
_CARS = "cars"
_CAR_RENTALS = "car_rentals"
_CAR_TYPES = "car_types"


class ShopDatabase(object):

	def __init__(self, shop_id):

		self.__shop_id = shop_id

		self.__check_db_exists()

	# === INTERFACE METHODS ===

	def get_cars(self):
		return self._get_data(_CARS)

	def get_car_rentals(self):
		return self._get_data(_CAR_RENTALS)

	def get_car_types(self):
		return self._get_data(_CAR_TYPES)

	def get_available_cars(self, cars=None, rentals=None):
		"""
		Outputs a dataset of all the cars that are currently available
		for renting.

		:param cars: a DataFrame representing the 'cars' file that may
		be passed if one exists locally (for caching purposes).
		Otherwise, it will be imported as normal.
		:param rentals: a DataFrame representing the 'car_rentals' file
		that may be passed if one exists locally (for caching purposes).
		Otherwise, it will be imported as normal.

		:return: a DatFrame consisting of all the listings of cars that
		as of present are available for renting.
		"""
		# Import the 'cars' file and 'car_rentals' files if any were not
		# passed as arguments.
		if cars is None:
			cars = self._get_data(_CARS)
		if rentals is None:
			rentals = self._get_data(_CAR_RENTALS)

		# Output only the non-rented cars - these will be considered
		# the ones that are available to rent.
		return cars.drop(rentals.index)

	def update_rentals(self, data):
		self._store_data(data, _CAR_RENTALS)

	# === INTERNAL METHODS ===
	def __check_db_exists(self, create=True):
		"""
		To be called during initialisation to check whether a database
		for the shop actually exists. If not, and the create parameter
		is set to True, then a default version is set up.

		:param create: a flag used to determine if a new database
		should be created if it turns out that one does not already
		exist. By default, it is True, indicating that a new one will
		be created.

		:return: True if it does already exist, False otherwise.
		"""

		# Construct the directory where the shop's database is expected
		# to be located at.
		db_dir = f"./{_DATABASE_DIRECTORY}/{self.__shop_id}"

		# If the directory already exists, do nothing more and
		# output True.
		if os.path.isdir(db_dir):
			return True
		else:
			# If it does not already exist and the create parameter
			# is True, then setup new files representing the database.
			if create:
				os.makedirs(db_dir, exist_ok=True)
				# Setup for the 'cars' table
				_setup_cars(db_dir)
				# Setup for the 'car_rentals' table
				_setup_rentals(db_dir)
				# Setup for the 'car_types' table
				_setup_car_types(db_dir)
			return False

	def _get_data(self, name, index_col=0):
		"""
		Used to import one of the rental shop's database files.

		:param name: the name of the file to use
		(either 'cars', 'car_types', or 'car_rentals')
		:param index_col: the column to use as the index for the
		imported dataset. By default it is 0 (first column).
		:return: a DataFrame object representing the imported database
		file.
		"""
		dtypes = None

		if name == _CAR_RENTALS:
			dtypes = {"customer_number": str}

		# Construct the path to the data file.
		path = self._get_file_dir(name)

		# Read the data, constructing a DataFrame out of it
		# (and specifying the column to use as an index) and then
		# returning it.
		return pd.read_csv(
			path,
			index_col=index_col,
			dtype=dtypes,
		)

	def _store_data(self, data, name):
		"""
		Overwrites (or newly creates) a given database file with
		updated data.

		:param data: the updated data to replace the current
		contents of the database file with.
		:param name: the name of the database file to overwrite.
		:return: None
		"""

		# Send the contents of the updated data the CSV file representing
		# the database file, overwriting the current contents.
		data.to_csv(
			self._get_file_dir(name),
		)

	def _get_file_dir(self, name):
		"""
		Outputs the path to the given database file's name.
		:param name: the name of the database file
		:return: a string containing the relative path to the database
		file.
		"""

		"""
		The format is as follows:

		./<DB-DIR>/<SHOP-ID>/<name>.csv

		- DB-DIR: name of the directory for all car shop databases
		- SHOP-ID: the identifier for the car rental shop
		- name: the name of the database file (or 'table') to extract.
		"""
		return f"./{_DATABASE_DIRECTORY}/{self.__shop_id}/{name}.csv"


# ========== DATABASE SETUP FUNCTIONS ==========

def _setup_cars(file_dir):
	"""
	Sets up a default file to store all the cars that exist in the
	rental shop.

	:param file_dir: the directory to store the file.
	:return: None
	"""

	"""
	Format of the file:

	car_id (ID):    an identifier for a car. Will have a format similar 
					to a numberplate.

	car_type:       the type of the car. 
					Can either be a hatchback, sedan, or suv.

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

	# Initial data will consist of 10 cars
	# (4 hatchbacks, 3 sedans, 3 SUVs),
	# with random IDs will be assigned to each.
	data = {
		"car_id": _random_car_ids(10),
		"car_type": [
			'hatchback', 'sedan', 'sedan', 'suv', 'suv',
			'hatchback', 'hatchback', 'hatchback', 'sedan', 'suv'
		],
	}

	# Create a DataFrame out of the above dictionary representing
	# the car dataset.
	cars = pd.DataFrame(data).set_index("car_id")

	# Create a CSV file out of the DataFrame.
	# The name of the file will be "cars.csv"
	cars.to_csv(f"{file_dir}/{_CARS}.csv")


def _setup_rentals(file_dir):
	"""
	Sets up a default file to store all the current car rentals.
	:param file_dir: the directory to store the file.
	:return: None
	"""

	"""
	Format of the file:

	car_id (ID):        an identifier for the car being rented. 
						Will have a format similar to a numberplate.

	customer_number:    an identifier for the customer who rented 
						the car.

	rate:               the daily rate (in pounds) for the car being 
						rented.

	days:               the number of days the car is rented for.

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

	# Create a DataFrame out of the above dictionary representing the
	# car rentals dataset.
	rentals = pd.DataFrame(data)

	# Ensure that each column has the right type.
	rentals = rentals.astype({
		'car_id': "object",
		'customer_number': "object",
		'rate': float,
		'days': int
	})

	# Use the "car_id" field as the index.
	rentals = rentals.set_index("car_id")

	# Create a CSV file out of the DataFrame. The name of the file will
	# be "car_rentals.csv"
	rentals.to_csv(
		f"{file_dir}/{_CAR_RENTALS}.csv",
	)


def _setup_car_types(file_dir):
	"""
	Sets up a default file to store the pricing of each of the different
	car types in the rental shop.

	:param file_dir: the directory to store the file.
	:return: None
	"""

	"""
	Format of the file:

	type_name (ID):     the name of the car type

	abbrev:             used to indicate whether the name is an 
						abbreviation of the real name.

	short_term_rate:    the daily rate charged for renting the car for 
						less than a week

	long_term_rate:     the daily rate charged for renting the car for 
						one week or more.

	vip_rate:           the daily rate charged for VIP customers.


	The expected dataset:
	--------------------------------------------------------------------
	type_name   abbrev       short_term_rate   long_term_rate   vip_rate
	--------------------------------------------------------------------
	hatchback   False         0.0              50.0             100.0
	sedan       False        25.0              40.0              90.0
	suv         True         20.0              35.0              80.0
	"""

	data = {
		"type_name": ["hatchback", "sedan", "suv"],
		"abbrev": [False, False, True],
		"short_term_rate": [30.0, 50.0, 100.0],
		"long_term_rate": [25.0, 40.0, 90.0],
		"vip_rate": [20.0, 35.0, 80.0]
	}

	# Create a DataFrame out of the above dictionary representing the
	# car types dataset.
	car_types = pd.DataFrame(data).set_index("type_name")

	# Create a CSV file out of the DataFrame. The name of the file will
	# be "car_types.csv"
	car_types.to_csv(
		f"{file_dir}/{_CAR_TYPES}.csv",
	)


# ========== AUXILIARY FUNCTIONS ==========

def _random_car_ids(n, seed=0):
	"""
	A function used to set up a given number of random IDs to be
	assigned to cars.
	They will be of the form 'LLddLLL', where
	- L is a random upper-case letter (A-Z)
	- d is a random digit (0-9).
	(Similar to the format of a numberplate)

	:param n: The number of IDs to generate.
	:param seed: the seed to use for the random generator
	(for reproducibility purposes). By default it is 0.

	:return: A list of n strings representing randomly generated car ids
	of the form above.
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
		:return: A list of m randomly generated digits
		(represented as strings).
		"""
		return random.choices(string.digits, k=m)

	# Initialise new list to store the ids.
	id_list = []

	# Initialise random generator with given seed.
	random.seed(seed)

	# Iterate n times to create n ids
	for i in range(n):
		# Create a random id consisting of 2 letters, followed by 3
		# digits, followed by 3 letters.
		car_id = "".join(rand_letters(2) + rand_digits(3) + rand_letters(3))

		# Add it to the list.
		id_list.append(car_id)

	# Output the list, now filled with random IDs.
	return id_list
