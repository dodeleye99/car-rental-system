from customer import Customer, VIPCustomer
from rental_shop import RentalShop


# ============ COMPONENT FUNCTIONS OF THE PROGRAM ============

def init_objects():
	"""
	Used to initialise customer and rental shop objects.
	The user will be allowed to enter an identifier to use for the
	customer.

	:return: a tuple consisting of a Customer object followed by a
	RentalShop object.
	"""

	# Initialise a car shop with identifier 'shop1'
	car_shop = RentalShop("shop1")

	"""
	1) PROMPTING FOR THE USER'S CUSTOMER NUMBER
	"""
	# Create a variable that will store the customer number inputted
	# by the user.
	customer_number = "000000"

	# Use a flag for validating the user's input for the
	# customer number.
	validated = False

	# As long as validation is not complete, have the user enter their
	# customer number.
	while not validated:

		# Prompt the user to enter their customer number.
		customer_number = input(
			"Please enter your six-digit customer number: "
		)

		# Validation #1: make sure that their input consists of
		# only digits
		if not customer_number.isdigit():
			print("Invalid format (must contain only digits)\n")

		# Validation #2: make sure that their input consists of
		# six characters (i.e. a 6-digit number)
		elif len(customer_number) != 6:
			print("Invalid format (must be a six-digit number)\n")

		# At this point, validation is complete, so prepare to
		# end the loop.
		else:
			print("Customer number accepted!")
			validated = True

	"""
	2) PROMPTING FOR LOYALTY CARD STATUS.
	"""

	# Create a variable that will store the loyalty card number inputted
	# by the user (unless they do not have one).
	loyalty_number = ""

	# Use a flag for validating the user's input for the
	# loyalty card.
	validated = False

	# As long as validation is not complete, have the user enter the
	# loyalty card number (or press enter if they do not have one).
	while not validated:

		# Prompt the user for their loyalty card number. If they lack
		# one, allow them to proceed by pressing just enter.
		loyalty_number = input(
			"\nDo you have a valid loyalty card? "
			"If so enter its 10-digit number.\n"
			"Otherwise simply press ENTER to continue.\n"
		).strip()  # Strip leading and trailing whitespace.

		# Exit the validation if they entered nothing
		# (i.e. they pressed ENTER indicating they do not have a valid
		# loyalty card).
		if loyalty_number == "":
			break

		# If their input for the card number is valid (10-digits),
		# accept the input by setting the flag to True
		if customer_number.isdigit() and len(customer_number) != 10:
			validated = True
		# Otherwise notify user that their input is invalid.
		else:
			print("Invalid number!")

	# If it was successfully validated, accept the customer as a VIP
	# member.
	if validated:
		print("Welcome VIP customer!")
		customer = VIPCustomer(customer_number, loyalty_number)

	# Otherwise (i.e. they do not have a loyalty card), accept them as
	# a normal customer.
	else:
		print("(Preceding as regular customer.)")
		# Instantiate a Customer object with the inputted customer number.
		customer = Customer(customer_number)

	# Output the newly created Customer and RentalShop objects
	# (as a tuple).
	return customer, car_shop


def inquire(customer: Customer, car_shop: RentalShop):
	"""
	Used to request the car stock (and prices) from the rental shop.

	:param customer: the customer inquiring from a rental shop
	:param car_shop: the rental shop being inquired from
	:return: None
	"""

	print_menu_text("INQUIRING FROM CAR RENTAL SHOP")

	# Have the customer ask the rental shop for the stock and prices.
	customer.inquire(car_shop)


def rent_car(customer: Customer, car_shop: RentalShop):
	"""
	Used to allow the user to rent a car.

	:param customer: the customer inquiring from a rental shop
	:param car_shop: the rental shop being inquired from
	:return: None
	"""

	print_menu_text("RENTING A CAR")

	# === Prompt user for the type of car to rent and number of days ===

	# Convert input of car_type to lowercase so that it is
	# not case-sensitive.
	car_type = input("Enter the type of car you would like to rent:\n").lower()
	days = input("Enter the number of days you would like to rent the car:\n")

	# Validation 1: ensure that the number of days is an integer.
	if not days.isdigit():
		print("The number of days must be an integer!")
	else:
		# Convert to an integer (since we can be sure that it is one)
		days = int(days)

		# Validation 2: ensure that number of days is greater than 0.
		if days <= 0:
			print("The number of days must be positive!")
		else:
			# At this point, validation is complete. Have the customer
			# ask the car shop to make the rental.
			customer.rent_car(car_type, days, car_shop)


def return_car(customer: Customer, car_shop: RentalShop):
	"""
	Used to allow the user to return a car.

	:param customer: the customer returning a car they have rented
	:param car_shop: the rental shop the customer is returning the car to.
	:return: None
	"""

	print_menu_text("RETURNING A CAR")

	# Have the user enter the "number plate" of the car they are returning.
	car_number = input(
		"Enter the vehicle registration number of the car you would like "
		"to return:\n")

	# Have the customer return the car to the rental shop.
	customer.return_car(car_number, car_shop)


# ============ THE MAIN FUNCTION ============

def main():
	"""
	Represents the main entry point of the program, immediately run when
	this script is executed.
	"""

	# Output an initial ribbon as a separator from whatever came
	# before it.
	print("=" * 80)

	# Output "welcome" text.
	print("Hello! Welcome to the Car Rental System.\n")

	# Create a flag do determine whether the main loop should still
	# be running
	running = True

	# Initialise the customer and the rental shop data
	customer, rental_shop = init_objects()

	# The main loop
	while running:

		print_menu_text("MAIN MENU")

		# Prompt user for what they want to do
		print(
			"What would you like to do?\n"
			"1 INQUIRE for car stock and prices.\n"
			"2 RENT a particular type of car for a number of days.\n"
			"3 RETURN a rented car.\n"
			"4 EXIT the program."
		)
		# Get the user's input (converting it to lowercase.)
		user_option = input(
			"Input the number (or the first word) "
			"corresponding to your option:\n"
		).lower()

		# Inquire : customer requests user stock
		if user_option in ("1", "inquire"):
			inquire(customer, rental_shop)

		# Rent : customer makes a car rental request
		elif user_option in ("2", "rent"):
			rent_car(customer, rental_shop)

		# Return : customer returns a car they borrowed
		elif user_option in ("3", "return"):
			return_car(customer, rental_shop)

		# Exit : user wants to end the program
		elif user_option in ("4", "exit"):
			# Switch the flag to end the main loop
			running = False

		# At this point, the input is invalid, so notify the user before
		# restarting the loop.
		else:
			print(
				"\nSorry, but I don't understand your input. "
				"Read the prompt and try again."
			)

	# Say goodbye to user as a way to mark the (official) end of the
	# program.
	print("Goodbye!")

	# Output a final ribbon as a separator from whatever will come
	# after it.
	print("=" * 80)


# ============ "HELPER" FUNCTIONS ============

def print_menu_text(label, nchar=80, nl_1=True, nl_2=True):
	"""
	A "helper" function for outputting menu text, represented as a
	horizontal "ribbon" containing an appropriate heading when a user is
	brought to one of the services of the system
	(i.e. inquiring, renting, returning).

	:param label: the text to display for the heading
	:param nchar: the total number of characters to use for the "ribbon"
	:param nl_1: a flag determining whether to print a new line BEFORE
	outputting the "ribbon" (True by default)
	:param nl_2: a flag determining whether to print a new line AFTER
	outputting the "ribbon" (True by default)

	:return: None
	"""

	# 1) Begin to construct the string: surround it with single
	# whitespace
	s = " " + label + " "

	# 2) Surround the text with the "=" character to make its
	# appearance similar to a "ribbon".
	s = s.center(nchar, "=")

	# 3) Add a leading/ending new line according to the flags.
	if nl_1:
		s = "\n" + s
	if nl_2:
		s = s + "\n"

	# 4) Output this constructed string.
	print(s)


if __name__ == "__main__":
	main()
