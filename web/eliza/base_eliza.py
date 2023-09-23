"""Script for running examples during ELIZA Workshop

Copyright (c) 2017-2023, Szymon Jessa
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

import os
import logging
import importlib.util
from importlib import import_module

DEFAULT_IDENTITIES_PATH = "web.eliza.identities"

def load_default_identity(identity_name):
    module_path = f"{DEFAULT_IDENTITIES_PATH}.{identity_name}"
    try:
        identity_module = import_module(module_path)
    except ModuleNotFoundError:
        logging.critical(f"Failed to load a default identity: {identity_name}.\n" \
                         "If you are trying to load a custom identity, provide full path to the file including the .py extension.\n")
        raise

    return identity_module

def load_identity_from_path(identity_path):
    spec = importlib.util.spec_from_file_location('custom_module', identity_path)
    custom_identity = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(custom_identity)
    return custom_identity

class MultiAgentSession:
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
