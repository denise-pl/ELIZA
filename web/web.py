import logging
import js
from pyodide.ffi import create_proxy
import eliza
import eliza_demo
from chat import GroupChat
from chat import USERNAME


class HTMLStream:
    def __init__(self, target="chat-window"):
        self._target = target

    def write(self, text):
        display(f"{text}", target=self._target)

    def flush(self):
        pass


def scrollToBottom():
    js.window.scrollTo(0, js.document.body.scrollHeight)


html_stream = logging.StreamHandler(HTMLStream("chat-window"))
formatter = logging.Formatter("%(levelname)s: %(message)s")
html_stream.setFormatter(formatter)
logging.getLogger().addHandler(html_stream)

eliza_agent = None


def start(evt=None):
    global eliza_agent
    display("", target="chat-window", append=False)
    eliza_agent = eliza.create()
    display(f"{eliza_agent.name()}: {eliza_agent.start()}", target="chat-window")
    js.document.getElementById("user-input").focus()


start()


def demo(evt=None):
    display("", target="chat-window", append=False)
    session = GroupChat(
        eliza.create(name="Therapist"), eliza_demo.create(name="Patient")
    )

    idx = 0
    while True:
        if idx % 2 == 0:
            display(f"****** Round #{int(idx/2)+1} ******", target="chat-window")
        name, msg = session.next()
        if msg == None:
            display(f"{name}: (END)", target="chat-window")
            break

        display(f"{name}: {msg}", target="chat-window")
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
    user_msg = Element("user-input").value.strip()
    if len(user_msg) > 0:
        display(f"{USERNAME}: {user_msg}", target="chat-window")
        answer = eliza_agent(user_msg)
        display(f"{eliza_agent.name()}: {answer}", target="chat-window")
        Element("user-input").clear()

    scrollToBottom()
    js.document.getElementById("user-input").focus()


def on_user_input_keypress(evt):
    if evt.key == "Enter":
        get_answer()


js.document.getElementById("user-input").addEventListener(
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
