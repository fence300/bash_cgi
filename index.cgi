#!/bin/bash

if [[ "$REQUEST_METHOD" == "POST" ]]
then
  :;
fi



echo "Content-Type: text/html"

echo
echo "<html><body>"

echo "<button formmethod='post'>post</button>"

env | sort | while read line;
do
  echo "<p>$line</p>"
done
echo "</body>"
echo "</html>"
