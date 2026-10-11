# Class Examples - Card Games

This repo contains the beginnings of what could become a card game library.

The goal is to demonstrate practical and easily understood examples of basic class concepts in Python such as:

- Inheritance: `is a` type relationships. For example:
    - A `BlackjackCard` is a type of `StandardCard` that has an additional attribute - its value in a game of Blackjack
    - A `Deck`, interestingly enough, is defined here as a type of `Hand`. This is not necessarily grounded in any sort of intuitive logic - it serves as an example that sometimes the way we decompose problems in programming does not correspond to how we think of the real, physical world. In this case I noticed that a `Deck` would basically use all of the same functionality as a `Hand`, with a few extra methods like `shuffle` and `deal`.

- Composition: `has a` type relationships. For example, hands contain cards.

- `dunder` methods. The name refers to the fact that they start and end with double underscores. These are special built-in methods you can use to define behavior such as:

    - What it means to compare two instances of a class. For example:
        - There is intentionally no equality (`__eq__`) defined for `StandardCard`, because without knowing what game we are playing, we might be assuming a bit too much to define it yet!
        - The `__len__` method is defined for `Hand`s as the length of the list of cards they store.
        - `__repr__` and `__str__` methods, both which define string representations of an object. The former is more meant for developers, the latter for users. Compare their output in the included `Examples.ipynb`.
