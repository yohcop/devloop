A couple of scripts that automates the compilation/refresh operations
when source files are saved in a project.

## watch-n-run.sh ##

Uses inotify to listen for changes to files with a given extension.
When any of those files change, a set of commands are executed.

For example:
`watch-n-run.sh gss ./gss.sh`

Will watch for update to *.gss files under the current directory and in
child directories recursively, and when one of them change, ./gss.sh is
executed.

You can run multiple instances of watch-n-run for different file
extensions, with different commands.

## chrome-remote-reload.py ##

Refreshes a chrome tab given a URL or a tab-id.
First, chrome must be ran with --remote-debugging-port=9234
(If you need to change the port, you need to change the python script
CHROME_URL variable).

For example:
`chrome-remote-reload.py localhost:8080`
Will search for all the tabs with a URL starting with "localhost:8080" (or
"http://localhost:8080"), connect to the chrome devtools for each tab, and
reload it.

It is also possible to pass the tab ID directly as well:
$ chrome-remote-reload.py 19
Will reload the tab with ID 19. Tab ids can be found by visiting
localhost:9234/json.

## Combining the 2 ##

Say you have to compile your css files with closure-stylesheets, and you do that with a gss.sh script. When the css file change, you want to recompile them, and reload the right browser tab. Your dev site is at localhost:8080.

`./watch-n-run.sh css ./gss.sh "./chrome-remote-reload.py localhost:8080"`

## devloop.py ##

See comments at the top of the file. It is basically a script that reads
a json configuration file that contains a list of commands to execute
when the files specified by a rule change.
