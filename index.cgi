#!/bin/bash


echo "Content-Type: text/html"
echo
echo "<html><body>"
env | while read line;
do
  echo "<p>$line</p>"
done
echo "</body>"
echo "</html>"
