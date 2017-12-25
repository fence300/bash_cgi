#!/bin/bash

if [ -e pages.sh ]
then
  source pages.sh
fi


if [[ "$REQUEST_METHOD" == "POST" ]]
then
  read POST_DATA
fi


environment_page
