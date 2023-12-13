from shop_db import ShopDatabase


class RentalShop:
	"""
	This class is used to represent a car rental shop, allowing
	customers to request for stock, hire a car to rent, and make
	returns.
	"""

	def __init__(self, shop_id):
		"""
		Used to initialise a new RentalShop instance.

		:param shop_id: a unique string identifier for the rental shop,
		which will be used to locate the rental shop's database system
		for managing its stock and rentals.
		"""

		self._shop_id = shop_id
		"""
		Represents a unique string identifier for the rental shop.
		"""

		# "Connect" to the database
		# (setting it up if it does not yet exist)
		self._shop_db = ShopDatabase(shop_id)
		"""
		Represents a connection to the rental shop's database, used to 
		make queries on it as well as update it.
		"""

	# === INTERFACE METHODS ===

	def display_stock_and_prices(self):
		"""
		Outputs the current available stock of each car type, as well as
		pricing for each type.
		:return: True if there is at least one car in stock.
		False otherwise.
		"""

		# Output the stock of each car types and the rates charged for
		# them, and obtaining whether there were any available at all.
		in_stock = self._output_stock(
			msg="The stock of each car type and pricing information",
			show_prices=True
		)

		# If everything was out of stock, give an appropriate message.
		if not in_stock:
			print("\n(Sorry, there are currently no cars available for rent.)")

		# Output the flag to enable the caller to know whether there
		# were any cars in stock.
		return in_stock

	def process_request(
			self, customer_number, car_type, days, loyalty_number=None
	):
		"""
		Takes in a customer's request to rent a particular kind of car
		for a certain number of days, and after checking whether it
		would be possible (i.e. stock availability), it proceeds to
		process the request and store it in the system's database.

		:param customer_number: the numerical ID of the customer who
		would like to rent a car.
		:param car_type: the type of car they would like to rent.
		:param days: the number of days they would like to rent the
		car.
		:param loyalty_number: the identification number of the
		customer's loyalty card (if they possess one; if not it
		defaults to None).
		:return: True if the process was successful. False otherwise.
		"""

		"""
		=== 1) VALIDATION OF THE CAR TYPE ===
		"""

		# Import the 'car_types' file from the database
		car_types = self._shop_db.get_car_types()

		# If it turns out that the requested car type does not exist as
		# a record in the 'car_types' file, notify the user and exit
		# returning False to indicate an unsuccessful process.
		if car_type not in car_types.index:
			print(
				f"\nSorry, but the car type you entered ({car_type})"
				f"is unknown to the system."
			)
			return False

		"""
		=== 2) CHECKING IF THE CAR TYPE IS IN STOCK ===
		"""

		# Get the 'car_rentals' file, to obtain all the cars currently
		# being rented.
		car_rentals = self._shop_db.get_car_rentals()
		# Get a listing of all the cars available to rent.
		available_cars = self._shop_db.get_available_cars(
			rentals=car_rentals
		)

		# Form a "selection" of all the cars that are og the given car
		# type.
		type_selection = available_cars["car_type"] == car_type
		# Extract all such cars from the availability listing.
		cars_of_type = available_cars[type_selection]

		# If it turns out that there are no cars of the requested
		# car type in stock, notify the user and exit returning False
		# to indicate an unsuccessful process.
		if len(cars_of_type) == 0:
			print(
				f"\nUnfortunately, no cars of the selected type "
				f"({car_type}) are in stock."
			)
			return False

		"""
		=== 3) PROCESSING THE CAR RENTAL REQUEST ===
		"""

		# Get the ID of the first car listed - let it be the one allocated
		# to the customer.
		car_id = cars_of_type.index[0]

		# Get the current pricing information of the customer's
		# desired car type.
		rates = car_types.loc[car_type]

		"""
		The number of days the customer wants to rent the car determines 
		the daily rate:
		-   If under one week (i.e. less than 7 days), then the short 
			term daily rate is applied.
		-   Any longer (i.e. 7 days or more), then the long term daily 
			rate is applied (cheaper than the short term rate)
			
		But if the customer is using a loyalty card, they automatically
		get the VIP discount regardless of the number of days they are
		renting the car for.
		"""
		if loyalty_number is not None:
			print(
				"\n(Loyalty card detected! "
				"You get access to a special discount!)"
			)
			r = rates["vip_rate"]
		elif days < 7:
			r = rates["short_term_rate"]
		else:
			r = rates["long_term_rate"]

		"""
		Add a new row to the car rentals dataset, containing the 
		following:
		- The ID of the car being rented.
		- The customer's number
		- The daily rate charged
		- THE number of days the car is being rented for.
		"""
		car_rentals.loc[
			car_id, ["customer_number", "rate", "days"]
		] = [str(customer_number), float(r), int(days)]

		# Apply these changes to the 'car_rentals' database file.
		self._shop_db.update_rentals(car_rentals)

		# Convert the customer's selected car type to upper case if
		# it is an abbreviated name.
		if car_type in self._get_abbrev_types(car_types):
			car_type = car_type.upper()

		# Output a message confirming that the rental was successfully
		# made.
		print(
			f"\nOrder successful! "
			f"You have rented a {car_type} car for {days} days.\n"
			f"The car's vehicle registration plate is {car_id}.\n"
			f"You will be charged £{r:.2f} per day.\n"
			f"We hope that you enjoy our service.\n")

		# Display the updated stock
		in_stock = self._output_stock(
			msg="Updated stock for each car type:", show_prices=False
		)

		# If there were no cars in stock, give an appropriate message.
		if not in_stock:
			print("(There are now no more cars available for rent.)")

		# At this point the rental was successful, so output True to
		# indicate this.
		return True

	def issue_bill(self, customer_number, car_number):
		"""
		Attempts to process a customer's return request, and if
		successful, issues a bill.
		:param customer_number: the numerical ID of the customer
		making the return.
		:param car_number: the "numberplate" of the car to be
		returned.
		:return: True if the return request is valid, False otherwise.
		"""

		# Import the 'car_rentals' file.
		car_rentals = self._shop_db.get_car_rentals()

		# Create string representing the message to output if the
		# return request is invalid.
		invalid_msg = (
			f"No car(s) you are renting "
			f"have that number ({car_number})"
		)

		# Output the message if no such car number is being rented.
		if car_number not in car_rentals.index:
			print(invalid_msg)
			# Output False to indicate that the request was
			# unsuccessful.
			return False

		# Get the rental information of the car being returned.
		rental = car_rentals.loc[car_number]

		# Output the message if it is a different customer who has/is
		# renting the car.
		if rental["customer_number"] != customer_number:
			print(invalid_msg)
			# Output False to indicate that the request was
			# unsuccessful.
			return False

		"""
		Processing the return
		"""
		# Remove the rental record from the dataset.
		car_rentals.drop(car_number)
		# Update the database file accordingly.
		self._shop_db.update_rentals(car_rentals)

		# Output message indicating that the return was successful.
		print("Return successful!")

		"""
		Issuing the bill
		"""
		# Import the 'cars' file.
		cars = self._shop_db.get_cars()

		# Get the type of the car being returned
		c_type = cars.loc[car_number, "car_type"]

		# Get the names of the car types that are abbreviation.
		abbrev_types = self._get_abbrev_types()

		# If the car type is an abbreviation, convert it to uppercase.
		if c_type in abbrev_types:
			c_type = c_type.upper()

		# Get the number of days the car was rented, and the daily rate.
		period_days = rental['days']
		rate_per_day = rental['rate']
		# Calculate the total cost.
		total = period_days * rate_per_day

		"""
		Finally output the billing information, showing:
		- Customer Number, 
		- Vehicle Registration Number, 
		- Car Type, 
		- Period (in days), 
		- Daily Rate,
		- Total Payment.
		"""
		print("\n====== CAR RENTAL BILL ======")
		print(
			f"Customer Number:              {customer_number}\n"
			f"Vehicle Registration Number:  {car_number}\n"
			f"Car Type:                     {c_type}\n"
			f"Period:                       {period_days} days\n"
			f"------------------------------\n"
			f"Rate:                         £{rate_per_day:.2f} per day\n"
			f"Total:                        £{total:.2f}\n"
			f"==============================\n"
		)

		# Output True to indicate that the request was successful.
		return True

	# === AUXILIARY METHODS ===

	def _output_stock(
			self, msg="The stock of each car type:", show_prices=False
	):
		"""
		Outputs the current available stock of each car type.
		:param msg: the message/caption to output accompanying the
		displayed stock.
		:param show_prices: a flag that, when set to True, will cause
		the pricing of each car type to also be displayed.
		:return: True if there is at least one car in stock.
		False otherwise.
		"""

		# Import the 'car_types' file from the database
		car_types = self._shop_db.get_car_types()

		"""
		1) Obtaining a list of stocks for each car type
		"""
		# Get a dataset of all the cars that are currently available for
		# renting.
		available_cars = self._shop_db.get_available_cars()

		# Create a new Series showing the number of available cars
		# of EACH car_type.
		car_type_stock = available_cars.groupby("car_type").size()

		"""
		2) Adding also the unavailable car types to the list.
		"""
		# Obtain a list of all the car types recorded on the system.
		types_list = car_types.index.to_list()
		# Construct a list of all the available car types
		avail_types_list = car_type_stock.index.to_list()

		# Use these lists to get the set of all car types that are
		# not in stock.
		missing_types = set(types_list) - set(avail_types_list)

		# List each of them in the car_type_stock Series as
		# "out of stock".
		for t in missing_types:
			car_type_stock[t] = "out of stock"

		"""
		3) Adding pricing information to the stock
		"""
		car_types['stock'] = car_type_stock

		"""
		4) Upper-casing abbreviated names
		"""
		# Get the names of all the car types that are abbreviations,
		# to know which ones need to be capitalised when displayed to
		# the user.
		abbrev_types = self._get_abbrev_types()

		# Cast the abbreviated type names to uppercase.
		car_types = car_types.rename(
			lambda x: x.upper() if x in abbrev_types else x
		)
		# Ensure the type names are listed in alphabetical order
		car_types = car_types.sort_index(key=lambda x: x.str.lower())

		"""
		5) Output the stock (and if applicable prices) as a 
		"pretty-printed" table, showing the number of cars of each type 
		that are available to rent.
		"""
		# Include the pricing information if the show_prices flag
		# is True
		if show_prices:
			output_stock = car_types.to_string(
				columns=[
					"stock",
					"short_term_rate",
					"long_term_rate",
					"vip_rate",
				],
				header=[
					"Stock",
					"<1w Rate",
					"1w+ Rate",
					"VIP Rate",
				],
				index=True,
				index_names=False,  # Don't show index title 'car_types'
				col_space=10,
				float_format="{:.2f}".format  # Display strings with 2dp
			)
		# Only show the stock if the show_prices flag is False (default)
		else:
			output_stock = car_types.to_string(
				columns=["stock"],  # Only display the 'stock' column
				header=[""],        # Don't show the column's label
				index=True,
				index_names=False   # Don't show index title 'car_types'
			)
		print(f"{msg}\n\n" + output_stock)

		# Output if there were any cars available (True) or not (False)
		return len(available_cars) != 0

	def _get_abbrev_types(self, car_types=None):
		"""
		Outputs all the car type names that are abbreviations
		(i.e. made up of initials of some multi-word name).
		The purpose of identifying such names is so that when displayed
		to the user they can be capitalised.
		(E.g. 'suv' displayed as 'SUV')

		:param car_types: a DataFrame representing the 'car_types' file
		that may be passed if one exists locally (for caching purposes).
		:return: a list containing all the car types that are
		abbreviations.
		"""
		# Import the 'car_types' file if it was not passed as an
		# argument.
		if car_types is None:
			car_types = self._shop_db.get_car_types()

		# Ensure the index of the car_types dataset is 'type_name'.
		if car_types.index.name != 'type_name':
			car_types = car_types.set_index('type_name', drop=False)

		# Extract the car types that are abbreviations
		# (i.e the "abbrev" field is True.), outputting result as a
		# list.
		return car_types[car_types["abbrev"]].index.to_list()