"""Script for running examples during ELIZA Workshop

Copyright (c) 2017-2022, Szymon Jessa
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

import logging
import argparse
from importlib import import_module

# show warnings and errors (don't show info or debug messages)
logging.basicConfig(format='%(levelname)s: %(message)s')


def group_chat(*agents):
    """Allows interaction between multiple agents in a loop:
    - first agent gets empty ("") message
    - each agent response is passed as input message to next agent
    - user must press enter after each response to continue the process
    - last agent response is passed as input message to first agent
    """

    i = 0
    msg = ""
    print("<press enter to continue; ctrl-c or q+enter to exit>\n")
    while input() != 'q':
        msg = agents[i](msg)
        print(f"{agents[i].name()}: {msg}")
        i = (i + 1) % len(agents)


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
    msg = input("User: ")
    while msg:
        print(f"{agent.name()}: {agent(msg)}")
        msg = input("User: ")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('agents', nargs="*", default=["eliza"])

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--example', '-e', type=int)
    group.add_argument('--demo', '-d', nargs="?", const=True, default=False)

    parser.add_argument('--verbose', '-v', action='count', default=0)
    args = parser.parse_args()

    if args.verbose == 1:
        logging.getLogger().setLevel(logging.INFO)
    elif args.verbose >= 2:
        logging.getLogger().setLevel(logging.DEBUG)

    agents = []
    for name in args.agents:
        logging.info("Loading agent: %s", name)
        module = import_module(name)
        agents.append(module)

    if len(agents) >= 2:
        group_chat(*[i.create() for i in agents])
    elif args.demo:
        group_chat(agents[0].create(name="Therapist"),
                    agents[0].create(name="Eliza"))
    elif args.example:
        agents[0].example(args.example)
    else:
        chat(agents[0].create())
