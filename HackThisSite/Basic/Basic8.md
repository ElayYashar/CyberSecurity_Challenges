Description:
Sam remains confident that an obscured password file is still the best idea, but he screwed up with the calendar program. Sam has saved the unencrypted password file in /var/www/hackthissite.org/html/missions/basic/8/

However, Sam's young daughter Stephanie has just learned to program in PHP. She's talented for her age, but she knows nothing about security. She recently learned about saving files, and she wrote a script to demonstrate her ability.

From <https://www.hackthissite.org/missions/basic/8/> 

We know that once again the password file is in same directory we are currently at, so we need to use the "ls" command once again, but there is no use of UNIX commands, but there is a PHP function that displays our input, we can pass the string:
<!--#exec cmd="ls ../"-->
Which 
And the function returns: 
"Hi, au12ha39vc.php index.php level8.php tmp! Your name contains 39 characters."
We can take the "au12ha39vc.php" file and pass it in the URL and get the password: "48c67862"
