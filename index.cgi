#!/bin/bash




if [[ "$REQUEST_METHOD" == "POST" ]]
then
  read POST_DATA
fi



echo "Content-Type: text/html"
echo
echo "<html>"
echo "<head>"
echo "<title>New Test Page</title>"
echo "<link rel='stylesheet' type='text/css' href='style.css' />"
echo "</head>"
echo "<body>"
echo "<div class='container'>"

echo "<div class='title'>Environment</div>"
env | sort | while read line
do
  echo "<p>$line</p>"
done
echo "<p>PWD: $(pwd)</p>"

echo "</div>"
echo "</body>"
echo "</html>"
