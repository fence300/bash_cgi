#!/bin/bash



if [[ "$REQUEST_METHOD" == "POST" ]]
then
  :;
fi



echo "Content-Type: text/html"
echo
echo "<html><body>"

echo "<h1>From tests</h1>"

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

echo "<h1>ENV</h1>"
env | sort | while read line;
do
  echo "<p>$line</p>"
done

echo "<h1>Parsing</h1>"
for i in ${QUERY_STRING//&/ }
do
  echo "<p>THING=$i</p>"
done


echo "</body></html>"
