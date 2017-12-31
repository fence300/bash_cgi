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
  echo "body { font-family:sans-serif;}"
  echo ".con { margin-left:20%;}"
  echo ".nav {position:fixed;top:0px;left:0px;width:20%;text-align:center;}"
  echo ".nav p {color:white;background-color:black;padding:5px;font-weight:bold;width=100%}"
  echo ".nav p:hover { background-color:white; color:black}"
  echo "</style>"
  echo "</head>"
}

html_body()
{
  echo "<body>"
  echo "<div class='con'>$body_content</div>"
  echo "<div class='nav'>"
  for i in {1..3}; do echo "<p><a>Item $i</a></p>"; done
  echo "</div>"
  echo "</body>"
}

if [[ "$HTTP_ACCEPT" =~ ^"text/html" ]]
then
  body_content+="<h1>Environment</h1>$(env | sort | while read line; do echo "<p>$line</p>"; done)"
  body_content+="<h1>Cookies</h1>$(for c in ${HTTP_COOKIE//;/ }; do echo "<p>$c</p>"; done)"
  echo "Set-Cookie: randint=$((RANDOM % 1000))"
  echo "Content-Type: text/html"
  echo
  html_headers
  html_body


elif [[ "$HTTP_ACCEPT" =~ ^"application/json" ]]
then
  echo "Content-Type: application/json"
  echo
  echo '{"status":1}'
else
  crit_err "unknown accept type"
fi
