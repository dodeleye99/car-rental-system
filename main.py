from customer import Customer
from rental_shop import RentalShop


def init_objects():
	"""
	Used to initialise customer and rental shop objects.
	The user will be allowed to enter an identifier to use for the customer.

	:return: a tuple consisting of a Customer object followed by a RentalShop object.
	"""

	# Initialise a car shop with identifier 'shop1'
	car_shop = RentalShop("shop1")

	# Create a variable that will store the customer number inputted by the user.
	customer_number = "000000"

	# Use a flag for validating the user's input for the customer number.
	validated = False

	# As long as validation is not complete, have the user enter their customer number.
	while not validated:

		# Prompt the user to enter their customer number.
		customer_number = input("Please enter your six-digit customer number: ")

		# Validation #1: make sure that their input consists of only digits
		if not customer_number.isdigit():
			print("Invalid format (must contain only digits)\n")

		# Validation #1: make sure that their input consists of six characters (i.e. a 6-digit number)
		elif len(customer_number) != 6:
			print("Invalid format (must be a six-digit number)\n")

		# At this point, validation is complete, so prepare to end the loop.
		else:
			print("Customer number accepted!")
			validated = True

	# Instantiate a Customer object with the inputted customer number.
	customer = Customer(customer_number)

	# Output the newly created Customer and RentalShop objects (as a tuple).
	return customer, car_shop


def inquire(customer, car_shop):
	"""
	Used to request the car stock (and prices) from the rental shop.

	:param customer: the customer inquiring from a rental shop
	:param car_shop: the rental shop being inquired from
	:return: None
	"""

	print("INQUIRING FROM CAR RENTAL SHOP:")
	customer.inquire(car_shop)


def rent_car():
	"""
	Used to allow the user to rent a car.
	"""
	print("RENTING A CAR:")
	print("Sorry, this service is currently unavailable.")


def return_car():
	"""
	Used to allow the user to return a car.
	"""
	print("RETURNING A CAR:")
	print("Sorry, this service is currently unavailable.")


def main():
	"""
	Represents the main entry point of the program, immediately run when this script is executed
	"""

	print("Hello! Welcome to the Car Rental System\n")

	# Create a flag do determine whether the main loop should still br running
	running = True

	# Initialise the customer and the rental shop data
	customer, rental_shop = init_objects()

	# The main loop
	while running:
		# Prompt user for what they want to do
		user_option = input("What would you like to do? ")

		# Inquire : customer requests user stock
		if user_option == "inquire":
			inquire(customer, rental_shop)

		# Rent : customer makes a car rental request
		elif user_option == "rent":
			rent_car()

		# Return : customer returns a car they borrowed
		elif user_option == "return":
			return_car()

		# Exit : user wants to end the program
		elif user_option == "exit":
			# Switch the flag to end the main loop
			running = False

	print("Goodbye!")


if __name__ == "__main__":
	main()
