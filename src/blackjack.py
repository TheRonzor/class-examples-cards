from __future__ import annotations

from src.cards import StandardCard, Hand

# This code extends the StandardCard and Hand for Blackjack
#
# Note the simplicity of the code, and the lack of any need
# to define much of the behavior and constants from cards.py.
#
# This is one of the upsides of using inheritance.
# The downside is that changes to cards.py could inadvertantly
# break this code.

class BlackjackCard(StandardCard):
    '''
    A BlackjackCard is a type of StandardCard.
    It has one additional property, which
    is its numerical value in a Blackjack game.
    '''

    # This property is derived at runtime
    # based on the card itself, thus it
    # does not need a setter.
    @property
    def value(self) -> int:
        return min(self.face_num, 10)


class BlackjackHand(Hand):
    '''
    A BlacjackHand is a type of Hand.
    
    Differences vs. the base Hand class:
        - add_card verifies that all cards added to the deck are
          of type BlackjackCard. This is implemented by redefining
          the add_card method, which overrides the original definition
          in the Hand class.
            - Note that add_card is called in Hand.__init__
              By redefining add_card here, when the base class
              calls add_card, it will call this version.
        - A BlackjackHand has a score, while a regular Hand does not.
        - A BlackjackHand is considered a "bust" if its score is >21.
    '''
    def add_card(self, card: StandardCard) -> None:
        # If the card is not of type BlackjackCard,
        # convert it
        if not isinstance(card, BlackjackCard):
            card = BlackjackCard(card.face_num, card.suit)

        # Instead of appending the card to the list of cards,
        # as is done in Hand.add_card, we call the Hand class's
        # add_card method.
        # super() is a special function that returns the parent class,
        # also known as the superclass
        super().add_card(card)
        return None

    @property
    def score(self) -> int:
        total = sum(card.value for card in self.cards)

        # Upgrade one Ace from 1 to 11 if possible
        if total <= 11 and any(card.face_num == 1
                               for card in self.cards
                              ):
            total += 10
        return total

    @property
    def is_bust(self) -> bool:
        return self.score > 21

class BlackjackGame:
    '''
    If I were to continue with the full implementation
    of a game of Blackjack, I would do so here.
    '''
    def __init__(self):
        raise NotImplementedError('BlackjackGame has not yet been implemented.')