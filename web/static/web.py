"""Script for running examples in the browser during ELIZA Workshop

Copyright (c) 2023, Szymon Jessa
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""
import logging
import js
from pyodide.ffi import create_proxy
from eliza.identities import eliza, eliza_demo
from eliza.base_eliza import MultiAgentSession

USERNAME = "You"
CHAT_WINDOW = "chat-window"
INPUT_ID = "user-input"


class HTMLStream:
    def __init__(self, target=CHAT_WINDOW):
        self._target = target

    def write(self, text):
        display(f"{text}", target=self._target)

    def flush(self):
        pass


def scrollToBottom():
    js.window.scrollTo(0, js.document.body.scrollHeight)


def start(evt=None):
    global eliza_agent
    display("", target=CHAT_WINDOW, append=False)
    eliza_agent = eliza.create()
    display(f"{eliza_agent.name()}: {eliza_agent.start()}", target=CHAT_WINDOW)
    js.document.getElementById(INPUT_ID).focus()

def demo(evt=None):
    display("", target=CHAT_WINDOW, append=False)
    session = MultiAgentSession(
        eliza.create(name="Therapist"), eliza_demo.create(name="Patient")
    )

    idx = 0
    while True:
        if idx % 2 == 0:
            display(f"****** Round #{int(idx/2)+1} ******", target=CHAT_WINDOW)
        name, msg = session.next()
        if msg == None:
            display(f"{name}: (END)", target=CHAT_WINDOW)
            break

        display(f"{name}: {msg}", target=CHAT_WINDOW)
        idx += 1

    scrollToBottom()


def set_logging(evt=None):
    global html_stream

    levels = {
        "CRITICAL": logging.CRITICAL,
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
    }

    level = js.document.querySelector("[name='output-level']:checked").value
    if level in levels:
        logging.getLogger().setLevel(levels[level])


def get_answer(evt=None):
    global eliza_agent

    user_msg = Element(INPUT_ID).value.strip()
    if len(user_msg) > 0:
        display(f"{USERNAME}: {user_msg}", target=CHAT_WINDOW)
        answer = eliza_agent(user_msg)
        display(f"{eliza_agent.name()}: {answer}", target=CHAT_WINDOW)
        Element(INPUT_ID).clear()

    scrollToBottom()
    js.document.getElementById(INPUT_ID).focus()


def on_user_input_keypress(evt):
    if evt.key == "Enter":
        get_answer()


def set_event_listeners():
    js.document.getElementById(INPUT_ID).addEventListener(
        "keypress", create_proxy(on_user_input_keypress)
    )
    js.document.getElementById("btn-demo").addEventListener("click", create_proxy(demo))
    js.document.getElementById("btn-send").addEventListener(
        "click", create_proxy(get_answer)
    )
    js.document.getElementById("btn-restart").addEventListener("click", create_proxy(start))
    js.document.getElementById("output-level-critical").addEventListener(
        "change", create_proxy(set_logging)
    )
    js.document.getElementById("output-level-info").addEventListener(
        "change", create_proxy(set_logging)
    )
    js.document.getElementById("output-level-debug").addEventListener(
        "change", create_proxy(set_logging)
    )


def main():
    html_stream = logging.StreamHandler(HTMLStream(CHAT_WINDOW))
    formatter = logging.Formatter("%(levelname)s: %(message)s")
    html_stream.setFormatter(formatter)
    logging.getLogger().addHandler(html_stream)
    start()

    set_event_listeners()

main()
