# General Functions
rand_string() { head -c 1000 /dev/urandom | LANG=C sed 's|[^0-9a-zA-Z]||g' | tr -d '\n' | head -c30;}
mysql_call() { mysql $db_name -u "$db_user" -p"$db_pass" -h "$db_host" -sNe "$*";}

# For composing HTML pages
html_headers() {
  echo "<head>"
  echo "<title>$site_title</title>"
  echo "<style>"
  echo "p {margin:0px;border:0px;}"
  echo "h1 { text-align:center;}"
  echo "body { font-family:serif;}"
  echo ".con { margin-left:20%;}"
  echo ".nav { position:fixed; height:100%;top:0px;left:0px;width:20%;text-align:center;background-color:grey;}"
  echo ".nav p {color:white;background-color:black;padding:5px;font-weight:bold;width=100%}"
  echo ".nav p:hover { background-color:white; color:black}"
  echo "</style>"
  echo "</head>"
}
html_body() {
  echo "<body>"
  echo "<div class='con'>$body_content</div>"
  echo "<div class='nav'>"
  if ((AUTHED))
  then
    echo ""
  else

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
