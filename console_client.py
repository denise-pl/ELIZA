"""Script for running examples during ELIZA Workshop

Copyright (c) 2017-2023, Szymon Jessa
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

import os
import logging
import argparse
from web.eliza.base_eliza import load_default_identity
from web.eliza.base_eliza import load_identity_from_path
from web.eliza.base_eliza import MultiAgentSession

USERNAME_IN_CHAT = "You"


def single_agent_chat(agent):
    """Allows user interaction in console with a single chatbot (agent) in a loop:
    - start session with empty ("") message sent to the agent
    - read user message from console
    - get agent's response
    - write agent's response to console
    - exit if user presses enter without any input (message length is 0)
    """

    print("\n<press enter with no message to exit>")
    print(f"{agent.name()}: {agent('')}")
    msg = input(f"{USERNAME_IN_CHAT}: ")
    while msg:
        print(f"{agent.name()}: {agent(msg)}")
        msg = input(f"{USERNAME_IN_CHAT}: ")


def multi_agent_chat(*agents):
    """Runs interaction between multiple agents in a turn based conversation.
    User must press enter after each response to continue the process.
    """
    session = MultiAgentSession(*agents)

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


def identity_type(value):
    if os.path.isfile(value):
        return (value, "custom")

    return (value, "default")


if __name__ == "__main__":
    logging.basicConfig(format="%(levelname)s: %(message)s")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "identities",
        nargs="*",
        default=[("eliza", "default")],
        type=identity_type,
        help="List of default identities or custom identities with paths to load.",
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--example",
        "-e",
        type=int,
        help="Runs examples demonstrating various concepts behind Eliza's algorithm",
    )
    group.add_argument(
        "--demo",
        "-d",
        nargs="?",
        const=True,
        default=False,
        help="Starts a chat between two Eliza agents: Eliza and Patient",
    )

    parser.add_argument("--verbose", "-v", action="count", default=0)
    args = parser.parse_args()

    if args.verbose == 1:
        logging.getLogger().setLevel(logging.INFO)
    elif args.verbose >= 2:
        logging.getLogger().setLevel(logging.DEBUG)

    if args.demo:
        eliza_identity = load_default_identity("eliza")
        patient_identity = load_default_identity("eliza_demo")
        multi_agent_chat(
            eliza_identity.create(name="Eliza"), patient_identity.create(name="Patient")
        )
    elif args.example:
        eliza_identity = load_default_identity("eliza")
        for msg in eliza_identity.example(args.example):
            print(msg)
    else:
        identities = []
        for identity_name, identity_type in args.identities:
            logging.info(f"Loading '{identity_type}' identity: {identity_name}")
            if identity_type == "default":
                identity_module = load_default_identity(identity_name)
            else:
                identity_module = load_identity_from_path(identity_name)

            identities.append(identity_module)

        if len(identities) >= 2:
            multi_agent_chat(*[i.create() for i in identities])
        else:
            single_agent_chat(identities[0].create())
