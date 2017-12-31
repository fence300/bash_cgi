#!/bin/bash

[ "$REQUEST_METHOD" = "POST" ] && { read POST_DATA;}
crit_err() { echo -e "Status: 500\nContent-type: text/html\n\n$*"; exit;}
test -e config.sh && source config.sh || crit_err "could not find config"
html_headers() {
  echo "<head>"
  echo "<title>$site_title</title>"
  echo "<style>"
  echo "p {margin:0px;border:0px;}"
  echo "h1 { text-align:center;}"
  echo ".con { margin-left:20%;}"
  echo "</style>"
  echo "</head>"
}

if [[ "$HTTP_ACCEPT" =~ ^"text/html" ]]
then
  echo "Set-Cookie: randint=$((RANDOM % 1000))"
  echo "Content-Type: text/html"
  echo
  html_headers
  echo "<h1>Environment</h1>"
  env | sort | while read line; do echo "<p>$line</p>"; done
elif [[ "$HTTP_ACCEPT" =~ ^"application/json" ]]
then
  echo "Content-Type: application/json"
  echo
  echo '{"status":1}'
else
  crit_err "unknown accept type"
fi
