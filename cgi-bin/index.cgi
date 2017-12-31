#!/bin/bash

[ "$REQUEST_METHOD" = "POST" ] && { read POST_DATA;}

echo "Content-Type: text/html"
echo
env | sort
echo "post data: $POST_DATA"
