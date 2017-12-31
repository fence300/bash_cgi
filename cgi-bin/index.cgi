#!/bin/bash

[ "$REQUEST_METHOD" = "POST" ] && { read POST_DATA;}

crit_err() { echo -e "Status: 500\nContent-type: text/html\n\n$*"; exit;}
[ -e config.sh ] && source config.sh || crit_err "could not find config"
for i in dir ses_dir; do [ -d "${!i}" ] || mkdir -p ${!i}; [ -d "${!i}" ] || crit_err "could not find $i"; done
[ -e "$dir"/functions.sh ] && source "$dir"/functions.sh || crit_err "could not load functions file"
[ -e "$dir"/pages.sh ] && source "$dir"/pages.sh || crit_err "could not load pages file"

mysql_call "CREATE TABLE IF NOT EXISTS users (
  user_id INT(10) NOT NULL AUTO_INCREMENT,
  username VARCHAR(255) NOT NULL,
  passhash VARCHAR(255) NOT NULL,
  firstname VARCHAR(255) NOT NULL,
  PRIMARY KEY(user_id)
)"

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

  for p in ${POST_DATA//&/ };
  do
    [[ "$p" =~ ^fn ]] && name=${p:3};
    [[ "$p" =~ ^un ]] && user=${p:3};
    [[ "$p" =~ ^pw ]] && pass=${p:3};
  done

  declare -a debug_msg
  case ${REQUEST_URI#${CONTEXT_PREFIX%/}} in
    (/) echo -e "Location: home\n\n"; exit ;;
    (/home) body_content+="<h1>Home</h1>"; site_title+=" | Home" ;;
    (/user/) body_content=$(view_profile);;

    (/upload)
    site_title+=" | Upload"
    body_content=$upload_form
    ;;

    (/create)
    debug_msg+=("Attempting to create account")
    if [ -n "$POST_DATA" ]
    then
      debug_msg+=("Detected POST request")
      if [[ "$user" && "$pass" && "$name" ]]
      then
        debug_msg+=("Found needed information")
        conflict=$(mysql_call "SELECT * FROM users WHERE username='$user'")
        if [[ -z "$conflict" ]]
        then
          debug_msg+=("Detected No Conflict")
          mysql_call "INSERT INTO users ( username, passhash, firstname ) VALUES ( '$user' , MD5('$pass'), '$name')"
          user_id=$(mysql_call "SELECT user_id FROM users WHERE username='$user' AND passhash=MD5('$pass')")
          sed -i 's|AUTHED=0|AUTHED=1|' "$ses_dir/$sess"
          declare -p user name user_id >> "$ses_dir/$sess"
          [[ "$rdr" ]] || rdr=home
          echo -e "Set-Cookie: rdr=NULL; expires=$expire_now\nLocation: $rdr\n\n"
          exit
        else
          debug_msg+=("Detected Conflict")
          message+="<h2>Sorry. That username is taken.</h2>"
        fi
      else
        debug_msg+=("Incomplete Form")
        message+="<h2>Please complete the form.<h2>"
      fi
      debug_msg+=("No Post Data sent")
    fi
    site_title+=" | Create Account"
    body_content+="<h1>Create An Account</h1>$message$create_account_form"
    ;;

    (/login)
    if [ -n "$POST_DATA" ]
    then
      if [[ "$user" && "$pass" ]]
      then
        user_id=$(mysql_call "SELECT user_id FROM users WHERE username='$user' AND passhash=MD5('$pass')")
        if [[ "$user_id" ]]
        then
          name=$(mysql_call "SELECT firstname FROM users WHERE username='$user' AND passhash=MD5('$pass')")
          sed -i 's|AUTHED=0|AUTHED=1|' "$ses_dir/$sess"
          declare -p user name user_id >> "$ses_dir/$sess"
          [[ "$rdr" ]] || rdr=home
          echo -e "Set-Cookie: rdr=NULL; expires=$expire_now\nLocation: $rdr\n\n"
          exit
        else
          message="<h2>Sorry. That's not what I have on file.</h2>"
        fi
      else
        message="<h2>Username and Password are required.</h2>"
      fi
    fi

    if [ -n "$rdr" ]
    then
      echo "Set-Cookie: rdr=$rdr; expires=$expire_soon"
      message+="<h2>you will be redirected to ${rdr} after login</h2>"
    fi
    site_title+=" | Login"
    body_content+="<h1>Login</h1>$message$login_form"
    ;;

    (/logout)
    sed -i 's|AUTHED=1|AUTHED=0|;/^declare/d' "$ses_dir/$sess"
    AUTHED=0
    site_title+=" | Logged Out"
    body_content="<h1>Logged Out</h1><h2>Come back soon!</h2>"
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

  debug=1
  echo "<body><div class='con'>$body_content"
  (debug) && echo "<table>$(for i in ${!debug_msg[*]}; do echo "<tr><td>${debug_msg[$i]}</td></tr>"; done)</table>"
  echo "</div><div class='nav'>"
  if ((AUTHED))
  then
    echo "<p><a href='home'>Hello $name</a></p>"
    echo "<p><a href='logout'>Log out</a></p>"
    echo "<p><a href='env'>Environment</a></p>"
  else
    echo "<p><a href='home'>Home</a></p>"
    echo "<p><a href='login'>Log In</a></p>"
  fi
  echo "</div></body></html>"
  exit
elif [[ "$HTTP_ACCEPT" =~ ^"application/json" ]]
then
  echo "Content-Type: application/json"
  echo
  echo '{"status":1}'
else
  crit_err "unknown accept type"
fi
