#!/bin/bash

[ "$REQUEST_METHOD" = "POST" ] && { read POST_DATA;}
crit_err() { echo -e "Status: 500\nContent-type: text/html\n\n$*"; exit;}
test -e config.sh && source config.sh || crit_err "could not find config"
for i in dir ses_dir; do [ -d "${!i}" ] || mkdir -p ${!i}; [ -d "${!i}" ] || crit_err "could not find $i"; done
rand_string() { head -c 1000 /dev/urandom | LANG=C sed 's|[^0-9a-zA-Z]||g' | tr -d '\n' | head -c30;}
html_headers() {
  echo "<head>"
  echo "<title>$site_title</title>"
  echo "<style>"
  echo "p {margin:0px;border:0px;}"
  echo "h1 { text-align:center;}"
  echo "body { font-family:serif;}"
  echo ".con { margin-left:20%;}"
  echo ".nav {position:fixed;top:0px;left:0px;width:20%;text-align:center;}"
  echo ".nav p {color:white;background-color:black;padding:5px;font-weight:bold;width=100%}"
  echo ".nav p:hover { background-color:white; color:black}"
  echo "</style>"
  echo "</head>"
}
html_body() {
  echo "<body>"
  echo "<div class='con'>$body_content</div>"
  echo "<div class='nav'>$(for i in {1..3}; do echo "<p><a>Item $i</a></p>"; done)</div>"
  echo "</body>"
}

present_time=$(date +%s)
if [[ "$HTTP_ACCEPT" =~ ^"text/html" ]]
then
  expire_now="$( TZ=GMT date +"%a, %d %b %Y %T %Z" )"
  expire_soon="$( TZ=GMT date -d@$((present_time + 900)) +"%a, %d %b %Y %T %Z" )"
  expire_later="$( TZ=GMT date -d@$((present_time + 3600)) +"%a, %d %b %Y %T %Z" )"

  for c in ${HTTP_COOKIE//;/ }; do [ "${c:0:5}" = "sess=" ] && sess="${c:5}"; done
  [ -z "$sess" ]||[ ! -e "$ses_dir/$sess" ]&&{ sess=$(rand_string); echo "AUTHED=0" >> "$ses_dir/$sess";}
  echo "Set-Cookie: sess=$sess; expires=$expire_soon";
  source "$ses_dir/$sess"


  body_content+="<h1>Environment</h1>$(env | sort | while read line; do echo "<p>$line</p>"; done)"
  body_content+="<h1>Cookies</h1>$(for c in ${HTTP_COOKIE//;/ }; do echo "<p>$c</p>"; done)"
  body_content+="<h1>Dummy Form</h1>
  <form method='post'>
  <input type='hidden' name='key1' value='val1'/>
  <input type='hidden' name='key2' value='val2'/>
  <input type='hidden' name='key3' value='val3'/>
  <input type='submit' value='post' />
  </form>"
  test -n "$POST_DATA" && body_content+="<h1>Post Data</h1>$(for p in ${POST_DATA//&/ }; do echo "<p>$p</p>"; done)"

  echo "Set-Cookie: randint=$((RANDOM % 1000))"
  echo "Content-Type: text/html"
  echo
  html_headers
  html_body


elif [[ "$HTTP_ACCEPT" =~ ^"application/json" ]]
then
  echo "Content-Type: application/json"
  echo
  echo '{"status":1}'
else
  crit_err "unknown accept type"
fi
