"""Template for creating chatbot identities with custom algorithms

Copyright (c) 2023, Szymon Jessa
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""
import logging
import doctest

DEFAULT_NAME = "blank"
"""Agent's default name
"""

class Chatbot:
    """Chatbot processing algorithm"""

    def __init__(self, name=DEFAULT_NAME):
        self._name = name
        """Chatbot name (may be used in chat)
        """
        self._idx = 0
        """Current message index
        """

    def name(self):
        """Get chatbot name"""
        return self._name

    def start(self):
        """Make the chatbot start the conversation"""
        self._idx = 0
        return self.__call__()

    def __call__(self, msg=None):
        """Return next message."""

        resp = None
        logging.info(f"Response {self._idx+1}: {resp}")

        self._idx += 1
        return str(resp)


def create(name=DEFAULT_NAME):
    """Returns default agent object"""
    return Chatbot(name)


def example():
    """Example conversation for script validation and debugging

    >>> agent = Chatbot()
    >>> agent("How do you do. Please tell me your problem")
    'None'
    """
    pass

if __name__ == "__main__":
    doctest.testmod(verbose=False)  # try verbose=True for more output
    print("If you don't see any errors, you are fine.")
