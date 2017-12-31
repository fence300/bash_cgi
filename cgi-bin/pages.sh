# Some useful Strings
present_time=$(date +%s)
expire_now="$( TZ=GMT date +"%a, %d %b %Y %T %Z" )"
expire_soon="$( TZ=GMT date -d@$((present_time + 900)) +"%a, %d %b %Y %T %Z" )"
expire_later="$( TZ=GMT date -d@$((present_time + 3600)) +"%a, %d %b %Y %T %Z" )"

dummy_form="<h1>Dummy Form</h1>
<form method='post'>
<input type='hidden' name='key1' value='val1'/>
<input type='hidden' name='key2' value='val2'/>
<input type='hidden' name='key3' value='val3'/>
<input type='submit' value='post' />
</form>"

login_form="<table><form method='post'>
<tr><td>Username:</td><td><input type='text' width='30' name='un'/></td></tr>
<tr><td>Password:</td><td><input type='password' width='30' name='pw'/></td></tr>
<tr><td><input type='submit' value='Log In' /></td><td><a href='create'>Create an Account</a></td></tr>
</form></table>"

upload_form="<h1>Upload Test</h1><p>placeholder</p>"
