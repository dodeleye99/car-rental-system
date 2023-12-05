from customer import Customer
from rental_shop import RentalShop


def init():
	"""
	Used to initialise customer and rental shop objects
	:return:
	"""
	print("Initialising...(nothing yet to do, still unimplemented)")


def inquire():
	"""
	Used to request the car stock (and prices) from the rental shop.
	"""
	print("INQUIRING FROM CAR RENTAL SHOP:")
	print("Sorry, this service is currently unavailable.")


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

	print("Hello! Welcome to the Car Rental System")

	# Create a flag do determine whether the main loop should still br running
	running = True

	# Initialise the customer and the rental shop data
	init()

	# The main loop
	while running:
		# Prompt user for what they want to do
		user_option = input("What would you like to do? ")

		# Inquire : customer requests user stock
		if user_option == "inquire":
			inquire()

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