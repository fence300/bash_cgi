#!/bin/bash
page_headers() {
  for arg in $*
  do
    case $arg in
      (--page-title=*) page_title=${arg#*=} ;;
    esac
  done
  [[ "$page_title" ]] || page_title="Test Page"
  echo "<head>"
  echo "<title>$page_title</title>"
  echo "<link rel='stylesheet' type='text/css' href='/style.css' />"
  echo "</head>"

}
environment_page() {
  echo "Content-Type: text/html"
  echo
  echo "<html>"
  page_headers --page-title="Environment"
  echo "<body>"
  echo "<div class='container'>"
  echo "<div class='title'>Environment Variables</div>"
  env | sort | while read line; do echo "<p>$line</p>"; done
  echo "</div>"
  echo "</body>"
  echo "</html>"
}

environment_page
