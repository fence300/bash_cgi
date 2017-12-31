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
  echo ".nav { position:fixed; top:0px; left:0px;}"
  echo ".nav p { color:white; background-color:black; padding:5px;}"
  echo ".nav p:hover { background-color:white; color:black}"
  echo "</style>"
  echo "</head>"
}

html_body()
{
  echo "<body>"
  echo "<div class='con'>"
  echo "$body_content"
  echo "</div>"
  echo "<div class='nav'>"
  for i in {1..3}; do echo "<p><a>Item $i</a></p>"; done
  echo "</div>"
  echo "</body>"
}

if [[ "$HTTP_ACCEPT" =~ ^"text/html" ]]
then
  echo "Set-Cookie: randint=$((RANDOM % 1000))"
  echo "Content-Type: text/html"
  echo
  html_headers
  echo "<body>"
  echo "<h1>Environment</h1>$(env | sort | while read line; do echo "<p>$line</p>"; done)"
  echo "<body>"
elif [[ "$HTTP_ACCEPT" =~ ^"application/json" ]]
then
  echo "Content-Type: application/json"
  echo
  echo '{"status":1}'
else
  crit_err "unknown accept type"
fi
