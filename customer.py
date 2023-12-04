
class Customer(object):
	"""
	This class is used to represent a customer that wishes to do business with any rental shop.
	"""

	def __init__(self, c_num):
		"""
		Used to initialise a new Customer instance.
		:param c_num: represents the numerical identifier to be assigned to the customer.
		"""

		self.__customer_number = c_num
		"""
		Represents the customer's unique numerical identifier. It will be used by the rental shop as a way to record 
		the customer when they make a rental, so that their order can be easily identified when they make a return.
		"""

	def inquire(self, rental_shop):
		"""
		Used to have the customer request the car stock of a given rental shop.
		:param rental_shop:
		:return:
		"""
		pass

	def rent_car(self, car_type, rental_shop):
		pass

	def return_car(self, rental_shop):
		pass

