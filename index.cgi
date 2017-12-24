#!/bin/bash

if [[ "$REQUEST_METHOD" == "POST" ]]
then
  :;
fi



echo "Content-Type: text/html"

echo
echo "<html><body>"

echo "<form>
<input type='hidden' name='key' value='val'></input>
<input type='hidden' name='key2' value='val2'></input>
<button type='submit' formmethod='post'>post</button>
<button type='submit' formmethod='get'>get</button>
</form>"

echo "<button method='post'>
Post Button Outside Form
</button>"

echo "<button method='get'>
Get Button Outside Form
</button>"
env | sort | while read line;
do
  echo "<p>$line</p>"
done
echo "</body>"
echo "</html>"
