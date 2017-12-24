#!/bin/bash

if [ "$SCRIPT_FILENAME" = "$PWD/index.cgi" ]
then
  echo 'Status: 403'
  echo 'Location: index.cgi'
  echo
fi
