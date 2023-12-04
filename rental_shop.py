import sqlite3


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

		self.__db_con = sqlite3.connect(f"{shop_id}.db")
		"""
		Represents a connection to the rental shop's database, used to make queries on it as well as update it.
		"""

	def display_stock(self):
		"""
		Outputs the current available stock of each car type.
		"""
		pass

	def process_request(self, customer_number, car_type, days):
		pass

	def issue_bill(self, customer_number):
		pass

