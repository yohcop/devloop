#!/bin/sh
#
# Usage:
# watch-n-run.sh file_extension commands_to_run
#
# Where:
# - file_extension is a single file extension, such as html, js, cc, etc
# - commands_to_run is a space separated list of commands to execute when
#   a file of the above extension is changed. To specify commands with
#   spaces, use quotes.

ext=$1
shift

while [ 1 ] ; do
  files=`find . -name \\*.$ext`
  inotifywait -e modify $files
  for cmd in "$@"; do
    echo "### Running: $cmd"
    $cmd
  done
done
