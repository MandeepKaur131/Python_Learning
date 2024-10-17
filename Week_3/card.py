import random

class Card:
    """
    The Card class represents a single playing card and is initialised by passing a suit and number.

    Attributes:
        suit (str): The suit of the card.
        number (str): The value of the card.
    """
    def __init__(self, suit, number):
        """
        Initializes a Card with a specific suit and number.

        Parameters:
            suit (str): The suit of the card.
            number (str): The rank of the card.
        """
        self._suit = suit
        self._number = number

    def __repr__(self):
        """
        Returns the string representation of card.

        Retruns:
            str:A string in the format "<number> of <suit>" .
        """
        return self._number + " of " + self._suit

    @property
    def suit(self):
        """
        Gets the suit of the card.

        Returns:
            str: The suit of the card.
        """
        return self._suit

    @suit.setter
    def suit(self, suit):
        """
        Sets the suit of the card after validating it.

        Parameters:
            suit (str): The new suit for the card. Must be one of "hearts",
            "clubs", "diamonds", or "spades".

        Returns:
            Prints the error message if suit is not valid.
        """
        if suit in ["hearts", "clubs", "diamonds", "spades"]:
            self._suit = suit
        else:
            print("That's not a suit!")

    @property
    def number(self):
        """
        Gets the number of the card.

        Returns:
            str: The number of the card.
        """
        return self._number

    @number.setter
    def number(self, number):
        """
        Sets the number of the card after validating it.

        Parameters:
            number (str): The new number for the card. Must be between "2"
            and "10", or one of "J", "Q", "K", "A".

        Returns:
            Prints the error message if number is not valid.
        """
        valid = [str(n) for n in range(2,11)] + ["J", "Q", "K", "A"]
        if number in valid:
            self._number = number
        else:
            print("That's not a valid number")


class Deck:
    """
    The Deck class rpresents a deck of playing cards, containing 52 cards by default.

    Attributes:
        cards (list): A list of card objects representing the deck.
    """

    def __init__(self):
        """
        Initializes a Deck object and populates it with 52 cards.
        """
        self._cards = []
        self.populate()

    def populate(self):
        """
        Populates the deck with 52 unique cards.
        """
        suits = ["hearts", "clubs", "diamonds", "spades"]
        numbers = [str(n) for n in range(2,11)] + ["J", "Q", "K", "A"]
        self._cards = [ Card(s, n) for s in suits for n in numbers ]

    def shuffle(self):
        """
        Shuffles the deck randomly.
        """
        random.shuffle(self._cards)

    def deal(self, no_of_cards):
        """
        Deals a specified number of card from the top of the deck.

        Parameters:
            no_of_cards (int): The number of cards to deal.

        Returns:
            list: A list of Card object that have been dealt.
        """
        dealt_cards = []
        for _ in range(no_of_cards):
            dealt_card = self._cards.pop(0)
            dealt_cards.append(dealt_card)
        return dealt_cards

    def __repr__(self):
        """
        Returns the string representation of the deck, showing how many cards remain.

        Returns:
            str: A string in the format "Deck of <n> cards", where <n> is the number of remaining cards.
        """
        cards_in_deck = len(self._cards)
        return "Deck of " + str(cards_in_deck) + " cards"

deck = Deck()
print(deck)