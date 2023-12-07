import os
import pandas as pd
import random
import string
import numpy as np


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
		:return: None
		"""

		# Import the 'car_types' file from the database
		car_types = self._get_data(_CAR_TYPES)

		# Get a dataset of all the cars that are currently available for renting.
		available_cars = self._get_available_cars()

		# Get the names of all the car types that are abbreviations, to know which ones need to be capitalised when
		# displayed to the user.
		abbrev_types = self._get_abbrev_types(car_types)

		# If it turns out that there are none that are available, notify the user/customer.
		if len(available_cars) == 0:
			print("Sorry, there are currently no cars available for rent.")

		# Otherwise, output the available stock.
		else:
			# Create a new DataFrame showing the number of available cars of EACH car_type.
			car_type_stock = available_cars.groupby("car_type").size()

			# Cast the abbreviated type names to uppercase.
			car_type_stock = car_type_stock.rename(lambda x: x.upper() if x in abbrev_types else x)
			
			"""
			Output the stock as a "pretty-printed" table, showing the number of cars of each type that are available to
			rent.
			"""
			output_stock = car_type_stock.to_string(header=False)
			print("\nAvailable car types to rent and their stock:\n\n" + output_stock)

		# Cast the abbreviated type names to uppercase.
		car_types = car_types.rename(lambda x: x.upper() if x in abbrev_types else x)
		"""
		Output the pricing information of each car type as a "pretty-printed" table, showing the following daily rates:
		- Under a week
		- At least one week.
		- VIP customers
		"""
		output_prices = car_types.to_string(
			columns=["short_term_rate","long_term_rate","vip_rate"],
			header=[
				"<1w", "1w+", "VIP"
			],
			index=True,
			index_names=False,   # (Do not show the index title 'car_types')
			col_space=10,
			float_format="{:.2f}".format    # (Display the strings with 2 decimal places)
		)
		print("\nPricing information for every car type (daily rates, in GBP):\n"+output_prices+"\n")

	def process_request(self, customer_number, car_type, days):
		"""
		Takes in a customer's request to rent a particular kind of car for a certain number of days, and after checking
		whether it would be possible, it proceeds to process the request and store it in the system's database.

		:param customer_number: the numerical ID of the customer who would like to rent a car.
		:param car_type: the type of car they would like to rent.
		:param days: the number of days they would like to rent the car.
		:return: True if the process was successful. False otherwise.
		"""

		"""
		=== 1) VALIDATION OF THE CAR TYPE ===
		"""

		# Import the 'car_types' file from the database
		car_types = self._get_data(_CAR_TYPES)

		# If it turns out that the requested car type does not exist as a record in the 'car_types' file, notify the
		# user and exit returning False to indicate an unsuccessful process.
		if car_type not in car_types.index:
			print(f"Sorry, but the car type you entered ({car_type}) is unknown to the system.")
			return False

		"""
		=== 2) CHECKING IF THE CAR TYPE IS IN STOCK ===
		"""

		# Get the 'car_rentals' file, to obtain all the cars currently being rented.
		car_rentals = self._get_data(_CAR_RENTALS)
		# Get a listing of all the cars available to rent.
		available_cars = self._get_available_cars(rentals=car_rentals)

		# Form a "selection" of all the cars that are og the given car type.
		type_selection = available_cars["car_type"] == car_type
		# Extract all such cars from the availability listing.
		cars_of_type = available_cars[type_selection]

		# If it turns out that there are no cars of the requested car type in stock, notify the
		# user and exit returning False to indicate an unsuccessful process.
		if len(cars_of_type) == 0:
			print(f"Unfortunately, no cars of the selected type ({car_type}) are in stock.")
			return False

		"""
		=== 3) PROCESSING THE CAR RENTAL REQUEST ===
		"""

		# Get the ID of the first car listed - let it be the one allocated to the customer.
		car_id = cars_of_type.index[0]

		# Get the current pricing information of the customer's desired car type.
		rates = car_types.loc[car_type]

		"""
		The number of days the customer wants to rent the car determines the daily rate:
		-   If under one week (i.e. less than 7 days), then the short term daily rate is applied.
		-   Any longer (i.e. 7 days or more), then the long term daily rate is applied 
			(cheaper than the short term rate)
		"""
		if days < 7:
			r = rates["short_term_rate"]
		else:
			r = rates["long_term_rate"]

		"""
		Add a new row to the car rentals dataset, containing the following:
		- The ID of the car being rented.
		- The customer's number
		- The daily rate charged
		- THE number of days the car is being rented for.
		"""
		car_rentals.loc[car_id, ["customer_number", "rate", "days"]] = [customer_number, r, days]

		# Apply these changes to the 'car_rentals' database file.
		car_rentals.to_csv(self._get_file_dir(_CAR_RENTALS))

		# Convert the customer's selected car type to upper case if it is an abbreviated name.
		if car_type in self._get_abbrev_types(car_types):
			car_type = car_type.upper()

		# Output a message confirming that the rental was successfully made.
		print(
			f"SUCCESS! You have rented a {car_type} car for {days} days. "
			f"You will be charged £{r:.2f} per day.\n"
			f"We hope that you enjoy our service.")

		# At this point the rental was successful, so output True to indicate this.
		return True

		# print("\nUpdated stock for each car type:\n")
		# self._output_current_stock()

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

	def _get_data(self, name, index_col=0):
		"""
		Used to import one of the rental shop's database files.
		:param name: the name of the file to use (either 'cars', 'car_types', or 'car_rentals')
		:param index_col: the column to use as the index for the imported dataset. By default it is 0 (first column).
		:return: a DataFrame object representing the imported database file.
		"""

		# Construct the path to the data file.
		path = self._get_file_dir(name)

		# Read the data, constructing a DataFrame out of it (and specifying the column to use as an index)
		# and then returning it.
		return pd.read_csv(path, index_col=index_col)

	def _get_available_cars(self, cars=None, rentals=None):
		"""
		Outputs a dataset of all the cars that are currently available for renting.
		:param cars: a DataFrame representing the 'cars' file that may be passed if one exists locally
		(for caching purposes). Otherwise, it will be imported as normal.
		:param rentals: a DataFrame representing the 'car_rentals' file that may be passed if one exists locally
		(for caching purposes). Otherwise, it will be imported as normal.

		:return: a DatFrame consisting of all the listings of cars that as of present are available for renting.
		"""
		# Import the 'cars' file and 'car_rentals' files if any were not passed as arguments.
		if cars is None:
			cars = self._get_data(_CARS)
		if rentals is None:
			rentals = self._get_data(_CAR_RENTALS)

		# Output only the non-rented cars - these will be considered the ones that are available to rent.
		return cars.drop(rentals.index)

	def _get_file_dir(self, name):
		"""
		Outputs the path to the given database file's name.
		:param name: the name of the database file
		:return: a string containing the relative path to the database file.
		"""

		"""
		The format is as follows:
		
		./<DB-DIR>/<SHOP-ID>/<name>.csv
		
		- DB-DIR: name of the directory for all car shop databases
		- SHOP-ID: the identifier for the car rental shop
		- name: the name of the database file (or 'table') to extract.
		"""
		return f"./{_DATABASE_DIRECTORY}/{self.__shop_id}/{name}.csv"

	def _get_abbrev_types(self, car_types=None):
		"""
		Outputs all the car type names that are abbreviations (i.e. made up of initials of some multi-word name).
		The purpose of identifying such names is so that when displayed to the user they can be capitalised.
		(E.g. 'suv' displayed as 'SUV')
		:param car_types: a DataFrame representing the 'car_types' file that may be passed if one exists locally
		(for caching purposes).
		:return: a list containing all the car types that are abbreviations.
		"""
		# Import the 'car_types' file if it was not passed as an argument.
		if car_types is None:
			car_types = self._get_data(_CAR_TYPES)

		# Ensure the index of the car_types dataset is 'type_name'.
		if car_types.index.name != 'type_name':
			car_types = car_types.set_index('type_name', drop=False)

		# Extract the car types that are abbreviations (i.e the "abbrev" field is True.), outputting result as a list.
		return car_types[car_types["abbrev"]].index.to_list()


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
	abbrev: used to indicate whether the name is an abbreviation of the real name.
	short_term_rate: the daily rate charged for renting the car for less than a week
	long_term_rate: the daily rate charged for renting the car for one week or more.
	vip_rate: the daily rate charged for VIP customers.
	
	
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
		"abbrev":    [False, False, True],
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

		assert len(car_id) == 8, f"The car id should consist of exactly 8 digits, but it has {len(car_id)}"
		assert car_id[:2].isalpha() and car_id[2:5].isdigit() and car_id[5:].isalpha(),\
			f"The car id should be of form LLddLLL, (L = A-Z, d = 0-9), but it is {car_id}"

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
