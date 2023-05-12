"""Script for running examples during ELIZA Workshop

Copyright (c) 2017-2023, Szymon Jessa
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

import logging

USERNAME = "You"


class GroupChat:
    """Allows interaction between multiple agents in a loop:
    - first agent gets empty ("") message
    - each agent response is passed as input message to next agent
    - last agent response is passed as input message to first agent
    """

    def __init__(self, *agents):
        self._agents = agents
        self._activeAgent = 0
        self._message = ""
        logging.debug(f"Number of agents: {len(agents)}")

    def next(self):
        logging.debug(
            f"Active agent: {self._activeAgent+1} ({self._agents[self._activeAgent].name()})"
        )

        self._message = self._agents[self._activeAgent](self._message)
        result = (self._agents[self._activeAgent].name(), self._message)
        self._activeAgent = (self._activeAgent + 1) % len(self._agents)

        return result


def chat(agent):
    """Allows user interaction with a single chatbot (agent) in a loop:
    - start session with empty ("") message sent to the agent
    - read user message from console
    - get agent's response
    - write agent's response to console
    - exit if user presses enter without any input (message length is 0)
    """

    print("\n<press enter with no message to exit>")
    print(f"{agent.name()}: {agent('')}")
    msg = input(f"{USERNAME}: ")
    while msg:
        print(f"{agent.name()}: {agent(msg)}")
        msg = input(f"{USERNAME}: ")
