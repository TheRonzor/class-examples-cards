from __future__ import annotations
import random

# Constants
#   Assumption is that we are always talking about
#   a standard deck of 52 cards with the usual suits

# The values are unicode symbols for the suits,
# i.e., ♣ ♦ ♥ ♠
SYMBS = {
    'Clubs'   : '\u2663',
    'Diamonds': '\u2666',
    'Hearts'  : '\u2665',
    'Spades'  : '\u2660'
}
SUITS = list(SYMBS.keys())
SUIT_INITIALS = {s[0].lower(): s for s in SUITS}

# Single letter abbreviations of some faces, 
# primarily for display purposes.
FACES = {
    1:  'A',
    10: 'T', 
    11: 'J', 
    12: 'Q', 
    13: 'K'
}

# Helpers
def num2card(n: int) -> StandardCard:
    '''
    Convert a number to a StandardCard.
    Uses 0-based input.
    '''
    if 0 <= n <= 51:
        suit = SUITS[n//13]
        num = 1+(n%13)
    else:
        raise ValueError(f'{n} is not a valid card number, 0 through 51 only.')
    return StandardCard(suit=suit, face_num=num)

# These two helpers could easily have been implemented
# within the classes. They are extracted and defined here
# to keep the logic visible, as they seem likely candidates
# for future adjustment
def format_card(face: str, suit: str) -> str:
    '''
    Basic text art to display a card.
    '''
    return f'|{suit}  |\n| {face} |\n|  {suit}|'

def join_multiline(strings: list[str]) -> str:
    '''
    Primarily used to join multiple text-art
    representations of cards and print as one row.
    '''
    rows = [s.splitlines() for s in strings]
    return '\n'.join(' '.join(row) for row in zip(*rows))


class StandardCard:
    '''
    A card from a standard 52-card deck.
    This class only defines the card itself,
    independent of any particular game.
    '''

    # __slots__ prevents creation of additional attributes
    # at runtime. For example, if we first create a card:
    #
    #  c = StandardCard(3, 'clubs')
    #
    # then the following would not be allowed:
    #  c.x = 42
    
    __slots__ = (
        '_suit',
        '_face_num'
    )
    
    def __init__(self,
                 face_num: int,
                 suit: str
                ):

        # Since we have defined setters below,
        # assigning the values automatically
        # triggers the validation code
        self.face_num = face_num
        self.suit = suit
        return

    # Using the @property decorator
    # allows us to reference these functions
    # as though they are variables rather than functions.
    # This goes hand-in-hand with the setter method below it.
    @property
    def suit(self) -> str:
        return self._suit

    # When we assign a value to suit, this
    # code is triggered. This is a good way
    # to validate data rather than allowing
    # any old value to be assigned to the property.
    @suit.setter
    def suit(self, suit: str) -> None:
        suit_in = suit
        suit = suit.strip().capitalize()
        
        if len(suit) == 1:
            suit = SUIT_INITIALS.get(suit.lower(), suit)
    
        if suit not in SUITS:
            raise ValueError(f'{suit_in} is not a valid suit.')
    
        self._suit = suit
        return None

    # This property doesn't need a setter.
    # The symbol for the suit is quickly looked
    # up at runtime, so we don't need to actually
    # store its value. Doing so could also potentially
    # create a conflict between what is stored in
    # suit vs suit_symbol.
    @property
    def suit_symbol(self) -> str:
        return SYMBS[self.suit]
    
    @property
    def face_num(self) -> int:
        return self._face_num

    @face_num.setter
    def face_num(self, face_num: int) -> None:
        if 1 <= face_num <= 13:
            self._face_num = face_num
        else:
            raise ValueError(f'{face_num} is not a valid face number. 1 through 13 only.')
        return None

    # Similar to suit_symbol, this property
    # does not need a setter. It is derived at
    # runtime rather than stored.
    @property
    def face_str(self) -> str:
        if self.face_num in FACES:
            return FACES[self.face_num]
        else:
            return str(self.face_num)

    # __repr__ is a string representation
    # of the object and primarily intended for
    # developers. It is what prints if you just
    # type the name of the object in a notebook cell
    # for example, without using print()
    def __repr__(self) -> str:
        return (
            f'{type(self).__name__}('
            f'face_num={self.face_num}, '
            f'suit={self.suit})'
        )

    # __str__ is the string representation of the card
    # when you use print() or str() on the object.
    # Here, we use the format_card helper which prints
    # a text-art version of the card.
    def __str__(self) -> str:
        return format_card(self.face_str, self.suit_symbol)

    # We do not defind equality of cards in this class,
    # since the meaning of two cards being equal could vary between games.
    # Instead, we write methods for same_face, same_suit, and same_card.
    # Inherited versions of the class can define their own __eq__ method
    # based on specific game rules.
    def same_face(self, other) -> bool:
        return (self.face_num == other.face_num)

    def same_suit(self, other) -> bool:
        return (self.suit == other.suit)

    def same_card(self, other) -> bool:
        return self.same_face(other) and self.same_suit(other)

class Hand:
    '''
    A Hand of cards. This is also a bare minimum implementation.
    It stores the cards and defines:
        add_card:  A method to add cards to the hand
        __len__ :  Number of cards in the hand
        __repr__:  A compact representation of the hand
        __str__ :  A "pretty" display of the hand as text art
    '''
    def __init__(self, cards: list[StandardCard]):
        self.cards = []
        for card in cards:
            self.add_card(card)
        return
    
    def add_card(self, card: StandardCard) -> None:
        self.cards.append(card)
        return None

    def __len__(self) -> int:
        return len(self.cards)

    def __repr__(self) -> str:
        return f'{type(self).__name__} with {len(self)} cards.'
    
    def __str__(self) -> str:
        return join_multiline([str(card) for card in self.cards])

class Deck(Hand):
    '''
    One might argue, an awkward implementation!
    Is a Deck really a type of Hand?
    I wouldn't say so, but as far as the code as written,
    seems like it could be implemented this way.
    '''
    def __init__(self):
        self.cards = []
        for n in range(52):
            card = num2card(n)
            super().add_card(card)
        return

    def shuffle(self, seed: int = None) -> None:
        if seed is not None:
            random.seed(seed)
        random.shuffle(self.cards)
        return None

    def deal(self) -> StandardCard:
        '''
        Return a card and remove from the deck.

        Raise a ValueError if the deck is empty
        '''
        if not len(self):
            raise ValueError('Deck is empty.')
        else:
            return self.cards.pop()
    