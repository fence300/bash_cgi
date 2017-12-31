# Define a wrapper for mysql
mysql_call() { mysql $db_name -u "$db_user" -p"$db_pass" -h "$db_host" -sNe "$*";}

# Ensure that it's going to work
error_message=$(mysql_call "SHOW TABLES" 2>&1 >/dev/null) || crit_err "database error: $error_message"

# make sure the users table exists as expected
mysql_call "CREATE TABLE IF NOT EXISTS users (
  user_id INT(10) NOT NULL AUTO_INCREMENT,
  username VARCHAR(255) NOT NULL,
  passhash VARCHAR(255) NOT NULL,
  firstname VARCHAR(255) NOT NULL,
  PRIMARY KEY(user_id)
)"
