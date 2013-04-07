#!/usr/bin/env python

# Start chrome with flag:
# google-chrome --remote-debugging-port=9234
#
# To get the id number to pass as first argument, go
# to:
# http://localhost:9234/json
#
# Run with either a URL, or an id

import json
import sys
import websocket

CHROME_URL="localhost:9234"

if len(sys.argv) != 2:
  print "Run with id or url as command line argument."
  sys.exit(1)

try:
  ids = [int(sys.argv[1])]
except:
  url = sys.argv[1]
  import urllib2
  cfg = json.loads(urllib2.urlopen("http://%s/json" % CHROME_URL).read())
  ids = []
  for page in cfg:
    if (page['url'].startswith(url) or
        page['url'].startswith('http://' + url)):
      ids.append(int(page['id']))
  if not ids:
    print "Could not find a page starting with %s" % url
    sys.exit(0)

# Not sure what id is here, I guess it doesn't matter.
for id in ids:
  ws = websocket.create_connection(
    "ws://%s/devtools/page/%d" % (CHROME_URL, id))
  ws.send("""{"id":1,"method":"Page.reload"}""")


