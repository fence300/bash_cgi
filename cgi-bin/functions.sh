# General Functions
rand_string() { head -c 1000 /dev/urandom | LANG=C sed 's|[^0-9a-zA-Z]||g' | tr -d '\n' | head -c30;}
mysql_call() { mysql $db_name -u "$db_user" -p"$db_pass" -h "$db_host" -sNe "$*";}

# For composing HTML pages
html_headers() {
  echo "<head>"
  echo "<title>$site_title</title>"
  echo "<link rel='stylesheet' type='text/css' href='/style.css' />"
  echo "</head>"
}
html_body() {
  debug=1
  echo "<body>"
  echo "<div class='con'>$body_content"
  (debug) && echo "<table>$(for i in ${!debug_msg[*]}; do echo "<tr><td>${debug_msg[$i]}</td></tr>"; done)</table>"
  echo "</div>"
  echo "<div class='nav'>"
  if ((AUTHED))
  then
    echo "<p><a href='home'>$user</a></p>"
    echo "<p><a href='logout'>logout</a></p>"
  else
    echo "<p><a href='home'>Home</a></p>"
    echo "<p><a href='login'>Log In</a></p>"
  fi
  echo "$(for i in {1..3}; do echo "<p><a>Dummy Item $i</a></p>"; done)"
  echo "</div>"
  echo "</body>"
}


view_profile()
{
  profile_id="${REQUEST_URI#${CONTEXT_PREFIX}user/}"
  [[ -z "$profile_id" ]] && profile_id=user_id
}
