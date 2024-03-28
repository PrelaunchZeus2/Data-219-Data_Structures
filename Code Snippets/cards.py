import random

class Card(object):
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
    
    def __str__(self):
        return self.value + " of " + self.suit
    
    def setSuit(self, suit):
        self.suit = suit
        
    def setValue(self, value):
        self.value = value
        
    def getSuit(self):
        return self.suit
    
    def getValue(self):
        return self.value
    
    
class Deck(object):
    def __init__(self):
        self.cards = []
        self.build()
        self.counter = 0
        
    def build(self):
        """populaes a deck of cards with the 52 standard playing cards"""
        for suit in ["Hearts", "Diamonds", "Spades", "Clubs"]:
            for value in range(1, 14):
                self.cards.append(Card(suit, value))
                
    def shuffle(self):
        """Shuffles the deck of cards."""
        for i in range(len(self.cards)):
            j = random.randint(0, len(self.cards) - 1)
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]
            
    def deal(self, number):
        """Returns a list of cards of length number.
        @param number: int - the number of cards to deal in a hand
        @return: list - a list of cards of length number"""
        hand = []
        for i in range(number):
            hand.append(self.cards[self.counter])
            self.counter += 1
        return hand