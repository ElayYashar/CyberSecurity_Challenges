Description:
This time Network Security Sam remembered to upload the password file, but there were deeper 
problems than that.
From <https://www.hackthissite.org/missions/basic/3/> 
This time we know there is a file, so by going into the DEV TOOLS and checking the form element, we 
can see this code: 
<input type="hidden" name="file" value="password.php">
By that we can understand that there is a file named "password.php" in the same directory we are in, 
after opening the file, it states the password: 8b1e0271