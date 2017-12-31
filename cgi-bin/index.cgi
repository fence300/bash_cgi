#!/bin/bash

[ "$REQUEST_METHOD" = "POST" ] && { read POST_DATA;}

crit_err() { echo -e "Status: 500\nContent-type: text/html\n\n$*"; exit;}
[ -e config.sh ] && source config.sh || crit_err "could not find config"
for i in dir ses_dir; do [ -d "${!i}" ] || mkdir -p ${!i}; [ -d "${!i}" ] || crit_err "could not find $i"; done
[ -e "$dir"/functions.sh ] && source "$dir"/functions.sh || crit_err "could not load functions file"
[ -e "$dir/pages.sh" ] && source "$dir/pages.sh" || crit_err "could not load pages file"


if [[ "$HTTP_ACCEPT" =~ ^"text/html" ]]
then
  for c in ${HTTP_COOKIE//;/ };
  do
    [ "${c:0:5}" = "sess=" ] && sess="${c:5}";
    [ "${c:0:4}" = 'rdr=' ] && rdr="${c:4}";
  done
  [ -z "$sess" ] || ! [ -e "$ses_dir/$sess" ] && { sess=$(rand_string); echo "AUTHED=0" >> "$ses_dir/$sess";}
  echo "Set-Cookie: sess=$sess; expires=$expire_soon";
  source "$ses_dir/$sess"

  case ${REQUEST_URI#${CONTEXT_PREFIX%/}} in
    (/) echo -e "Status: 302\nLocation: home\n\n"; exit ;;
    (/home) body_content+="<h1>Home</h1>"; site_title+=" | Home" ;;
    (/user/) body_content=$(view_profile);;
    (/upload)
    site_title+=" | Upload"
    body_content=$upload_form
    ;;

    (/login)
    for c in
    for p in ${POST_DATA//&/ };
    do
      [[ "$p" =~ ^un ]] && user=${p:3};
      [[ "$p" =~ ^pw ]] && pass=${p:3};
    done
    if [[ "$user" && "$pass" ]]
    then
      user_id=$(mysql_call "SELECT user_id FROM uses WHERE username='$user' AND passhash=MD5('$pass')")
      if [[ "$user_id" ]]
      then
        [ -z "$rdr" ] || rdr="home"

      else
        message="<h2>sorry, that's not what I have on file</h2>"
      fi
    else
      message="<h2>username and password are required</h2>"
    fi

    site_title+=" | Login"
    body_content+="<h1>Login</h1>$message"

    ;;

    (/env)
    site_title+=" | Environment"
    body_content+="<h1>Environment</h1>$(env | sort | while read line; do echo "<p>$line</p>"; done)"
    body_content+="<h1>Cookies</h1>$(for c in ${HTTP_COOKIE//;/ }; do echo "<p>$c</p>"; done)"
    body_content+="$dummy_form"
    [ -n "$POST_DATA" ] && body_content+="<h1>Post Data</h1>$(for p in ${POST_DATA//&/ }; do echo "<p>$p</p>"; done)"
    ;;

  esac


  echo "Content-Type: text/html"
  echo
  echo "<html>"
  html_headers
  html_body
  echo "</html>"

elif [[ "$HTTP_ACCEPT" =~ ^"application/json" ]]
then
  echo "Content-Type: application/json"
  echo
  echo '{"status":1}'
else
  crit_err "unknown accept type"
fi
