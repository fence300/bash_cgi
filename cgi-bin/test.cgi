#!/bin/bash

## Startup Sequence

# the post requst demand to be heard
[ "$REQUEST_METHOD" = "POST" ] && read POST_DATA

# A wrapper for graceful failure
crit_err() { echo -e "Status: 500\nContent-type: text/html\n\n$*"; exit;}

# Load the configruations and resources
[ -e config.sh ] && source config.sh || crit_err "could not find config"
for i in dir ses_dir; do mkdir -p ${!i}; [ -d "${!i}" ] || crit_err "could not find dir: $i"; done
for i in func page; do [ -e "$dir/$i.sh" ] && source "$dir/$i.sh" || crit_err "couldn not load: $i"; done

echo "Content-Type: text/html"
echo
echo "<html><body><h1><center>Env</center></h1>"
env | sort | while read line; do echo "<p>$line</p>"; done
echo "</body></html>"
