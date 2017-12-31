#!/bin/bash

[ "$REQUEST_METHOD" = "POST" ] && read POST_DATA

echo "Content-Type: text/html"
echo
echo "<html>"
echo "<head><title>Test Page</title><style>p{margin:0px;border:0px}h1{text-align:center}body{margin-left:10%}</style></head>"
echo "<body>"
echo "<h1>Posts</h1>$(for p in ${POST_DATA//&/ }; do echo "<p>$p</p>"; done)"
echo "</body>"
echo "</html>"
