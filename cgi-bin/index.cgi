#!/bin/bash

site_title="Mirkre Sandbox"


echo "Content-Type: text/html"
echo
echo "<html>"
echo "<head>"
echo "<title>$site_title</title>"
echo "<link rel='stylesheet' type='text/css' href='/style.css' />"
echo "</head>"
echo "<body>"
echo "<div class='con'>"
echo "<h1>Environment</h1>$(env | sort | while read line; do echo "<p>$line</p>"; done)"
echo "</div>"
echo "</body>"
echo "</html>"
