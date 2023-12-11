from rental_shop import RentalShop


class Customer(object):
    """
    This class is used to represent a customer that wishes to do
    business with any rental shop.
    """

    def __init__(self, c_num):
        """
        Used to initialise a new Customer instance.
        :param c_num: represents the numerical identifier to be
        assigned to the customer.
        """

        self.__customer_number = c_num
        """
        Represents the customer's unique numerical identifier. It will 
        be used by the rental shop as a way to record the customer when
        they make a rental, so that their order can be easily identified
        when they make a return.
        """

    def inquire(self, rental_shop: RentalShop):
        """
        Used to have the customer request the car stock of a given
        rental shop (as well as the prices).

        :param rental_shop: a RentalShop object representing the car
        rental shop to inquire from.
        :return: None
        """
        # Simply ask for the rental shop to display the available stock
        # (and pricing).
        rental_shop.display_stock_and_prices()

    def rent_car(self, car_type, days, rental_shop: RentalShop):
        """
        Used to allow the customer to request a rental of a particular
        type of car from a given rental shop.

        :param car_type: the type of the car to be rented
        :param days: the number of days to rent the car
        :param rental_shop: a RentalShop object representing the car
        rental shop to rent from
        :return: True if the renal was successfully made.
        False otherwise.
        """
        # Call the rental shop to process the customer's request
        # (whether successful or not).
        return rental_shop.process_request(
            self.__customer_number, car_type, days
        )

    def return_car(self, car_number, rental_shop: RentalShop):
        """
        Used to allow a customer to return a car that they have
        previously rented from a rental shop

        :param car_number: the identifier for the car being returned.
        :param rental_shop: a RentalShop object representing the car
        rental shop they are returning a car to.
        :return: None
        """

        # Call the rental shop to return the car being rented (if valid)
        # and issue a bill.
        rental_shop.issue_bill(self.__customer_number, car_number)
