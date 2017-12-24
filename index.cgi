#!/bin/bash





echo "Content-Type: text/html"

echo
echo "<html><body>"
env | sort | while read line;
do
  echo "<p>$line</p>"
done
echo "</body>"
echo "</html>"
