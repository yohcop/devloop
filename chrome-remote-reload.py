#!/usr/bin/env python

# Start chrome with flag:
# google-chrome --remote-debugging-port=9234
#
# To get the websocketDebugUrl for a given tab, go to:
# http://localhost:9234/json
#
# Run with either a websocketDebugUrl, or a URL directly.
# Note that the chrome dev tools must be closed in the given tab
# for the connection to the websocket work (otherwise, no websocket
# connection is accepted by chrome)

import json
import sys
import websocket

CHROME_URL="localhost:9234"

if len(sys.argv) != 2:
  print "Run with websocketDebugUrl or url as command line argument."
  sys.exit(1)

if sys.argv[1].startswith('ws://'):
  ids = [sys.argv[1]]
else:
  url = sys.argv[1]
  import urllib2
  cfg = json.loads(urllib2.urlopen("http://%s/json" % CHROME_URL).read())
  ids = []
  for page in cfg:
    if ((page['url'].startswith(url) or
         page['url'].startswith('http://' + url)) and
        'webSocketDebuggerUrl' in page):
      ids.append(page['webSocketDebuggerUrl'])
  if not ids:
    print ("Could not find a page starting with %s - " +
           "or the dev tools are already open for this " +
           "tab. Close them first.") % url
    sys.exit(0)

# Not sure what id is here, I guess it doesn't matter.
for id in ids:
  ws = websocket.create_connection(id)
  ws.send("""{"id":1,"method":"Page.reload"}""")


