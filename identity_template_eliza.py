"""Template for creating custom ELIZA scripts

Copyright (c) 2017-2023, Szymon Jessa
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""
import doctest

from web.eliza.identities.eliza import KEYWORD_START, KEYWORD_NONE
from web.eliza.identities.eliza import Chatbot

DEFAULT_NAME = "blank"
"""Agent's default name
"""

script = dict()

script[KEYWORD_START] = {
    "rules": [
        {"reassembly": [
            "MY KEYWORD_START ANSWER: I'm Blank! Feed my script!"]}
    ]
}

script[KEYWORD_NONE] = {
    "rules": [{
        "reassembly": [
            "MY KEYWORD_NONE ANSWER: I'm Blank! Feed my script!"
        ]}]
}

script["MYKEYWORD"] = {
    "rank": 0,
    "rules": [{
        "reassembly": [
            "MYANSWER"
        ]}]
}


def create(name=DEFAULT_NAME, script=script):
    """Returns default agent object
    """
    return Chatbot(name, script)


def example(length):
    """
    >>> agent = Chatbot()
    """
    messages = [
        # Fill in with your example / test inputs
    ]

    agent = Chatbot()
    for idx, msg in enumerate(messages[:length], 1):
        print(f"****** Round #{idx} ******")
        print(f"User: {msg}")
        print(f"{agent.name()}: {agent(msg)}")
        print()


if __name__ == '__main__':
    doctest.testmod(verbose=False)  # try verbose=True for more output
    print("If you don't see any errors, you are fine.")
