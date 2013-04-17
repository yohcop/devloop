#!/usr/bin/env python

"""
Reads a json config file, such as (note there are no trailing commas)
>>>>>
[
  {
    "dir": "genfiles",
    "match": "*.html",
    "cmds": [
      "ls",
      "echo 'hello world'"
    ]
  },
  {
    "dir": "src",
    "match": "*.js",
    "cmds": [
      "pwd",
      "ls"
    ]
  }
]
<<<<<
Listens for changes to the files matching the blobs, and execute
the list of commands for each file when they change.

If a file is matched by multiple rules, then all the commands are
executed. If the same command appear in multiple list of commands, it is
only executed once.

If one of the commands returns a non-zero value, the following commands of
the same list of commands are not executed.
"""

import fnmatch
import json
import os
import pyinotify
import sys

wm = pyinotify.WatchManager()
mask = pyinotify.IN_MODIFY

# a map filename -> [config which added that filename]
watches = {}

class PTmp(pyinotify.ProcessEvent):
  def process_default(self, event):
    # Add the watch back to keep getting events for that file.
    wm.add_watch(event.path, mask)
    try:
      # Get the list of configs for that path.
      w = watches[event.path]
      ran = {}
      for config in w:
        # For each config, get the list of commands to run.
        for cmd in config['cmds']:
          # We run each command only once.
          if not cmd in ran:
            print "=== Running", cmd, "==="
            ret = os.system(cmd)
            if ret != 0:
              break
            else:
              ran[cmd] = True
    except:
      pass


def findFiles(src, ext):
  res = []
  for root, _, filenames in os.walk(src):
    res += [os.path.join(root, f)
            for f in fnmatch.filter(filenames, ext)]
  return res


notifier = pyinotify.Notifier(wm, PTmp())

cfg = json.loads(open(sys.argv[1]).read())
for d in cfg:
  # For each config, get the files that should be watched.
  files = findFiles(d['dir'], d['match'])
  for f in files:
    # Normalize the paths (seems to be what inotify provides)
    n = os.path.normpath(f)
    # Save an inverted mapping file -> list of configs.
    if n in watches:
      watches[n].append(d)
    else:
      watches[n] = [d]
  wm.add_watch(files, mask, rec=True)

while True:
  try:
    notifier.process_events()
    if notifier.check_events():
      notifier.read_events()
  except KeyboardInterrupt:
    notifier.stop()
    break
