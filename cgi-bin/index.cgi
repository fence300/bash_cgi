#!/bin/bash

[ "$REQUEST_METHOD" = "POST" ] && { read POST_DATA;}
crit_err() { echo -e "Status: 500\nContent-type: text/html\n\n$*"; exit;}
test -e config.sh && source config.sh || crit_err "could not find config"
html_headers() { echo "<head><title>$site_title</title></head>";}

if [[ "$HTTP_ACCEPT" =~ ^"text/html" ]]
then
  :
elif [[ "$HTTP_ACCEPT" =~ ^"application/json" ]]
then
  :
else
  crit_err "unknown accept type"
fi

echo "Set-Cookie: randint=$((RANDOM % 1000))"
echo "Content-Type: text/html"
echo
env | sort
echo "post data: $POST_DATA"
