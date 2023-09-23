"""Script for running ELIZA in web browser

Copyright (c) 2023, Szymon Jessa
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""
import os
import http.server
import socketserver
import webbrowser

PORT = 8000

os.chdir("web")
url = f'http://localhost:{PORT}'
webbrowser.open(url)

handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(("", PORT), handler) as httpd:
    print(f"Serving ELIZA web client at: {url}")
    httpd.serve_forever()
