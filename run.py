"""Script for running examples during ELIZA Workshop

Copyright (c) 2017-2023, Szymon Jessa
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

import logging
import argparse
from importlib import import_module
from chat import GroupChat
from chat import chat


def demo(*agents):
    """Runs interaction between multiple agents in a loop:
    - first agent gets empty ("") message
    - each agent response is passed as input message to next agent
    - user must press enter after each response to continue the process
    - last agent response is passed as input message to first agent
    """
    session = GroupChat(*agents)

    idx = 0
    print("<press enter to continue; ctrl-c or q+enter to exit>")
    print()
    while input() != "q":
        if idx % len(agents) == 0:
            print(f"****** Round #{int(idx/(len(agents)))+1} ******")
            print()
        name, msg = session.next()
        if msg == None:
            print(f"{name}: (END)")
            break

        print(f"{name}: {msg}")
        idx += 1


if __name__ == "__main__":
    logging.basicConfig(format="%(levelname)s: %(message)s")

    parser = argparse.ArgumentParser()
    parser.add_argument("agents", nargs="*", default=["eliza"])

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--example", "-e", type=int)
    group.add_argument("--demo", "-d", nargs="?", const=True, default=False)

    parser.add_argument("--verbose", "-v", action="count", default=0)
    args = parser.parse_args()

    if args.verbose == 1:
        logging.getLogger().setLevel(logging.INFO)
    elif args.verbose >= 2:
        logging.getLogger().setLevel(logging.DEBUG)

    agents = []
    for name in args.agents:
        logging.info("Loading agent: %s", name)
        module = import_module(f"{name}")
        agents.append(module)

    if len(agents) >= 2:
        demo(*[i.create() for i in agents])
    elif args.demo:
        demo(agents[0].create(name="Therapist"), agents[0].create(name="Eliza"))
    elif args.example:
        for msg in agents[0].example(args.example):
            print(msg)
    else:
        chat(agents[0].create())
