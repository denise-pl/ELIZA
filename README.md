# ELIZA - Workshop

Files used for Natural Language Processing Workshop inspired by Joseph's Weizenbaum work from year 1966: [ELIZA - A Computer Program For the Study of Natural Language Communication Between Man and Machine](https://web.stanford.edu/class/linguist238/p36-weizenabaum.pdf).

## How to run

Start chat in the console:
```
python console_client.py
```

See an example conversation:
```
python console_client.py --demo
```

To get more details in the output add '-v' or '-vv' or '-vvv':
```
python console_client.py -v
```

Start chat in the browser:
```
python web_client.py
```

It is possible to create custom chatbots and make them talk to each other in a multi-agent chat (the code below will create 5 agents, of which three are using default 'eliza' identity and two are custom, user defined identities):
```
python console_client.py eliza ./my_custom_chatbot.py ./my_second_custom_chatbot.py eliza eliza
```

To create a custom identity, based on the ELIZA algorithm, you may use the [identity_template_eliza.py](identity_template_eliza.py) file.

To create a custom identity, based on a different algorithm, you may use the [identity_template.py](identity_template.py) file.

To chat with the custom identity, just pass the path to it as argument:
```
python console_client.py ./my_custom_chatbot.py
```

# Feedback & ideas

szymon [dot] denise [ at ] gmail [ dot ] com

# License

Copyright (c) 2017-2023, Szymon Jessa

All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
