Description:
Network Security Sam is going down with the ship - he's determined to keep obscuring the password file, no matter how many times people manage to recover it. This time the file is saved in /var/www/hackthissite.org/html/missions/basic/9/.

In the last level, however, in my attempt to limit people to using server side includes to display the directory listing to level 8 only, I have mistakenly screwed up somewhere.. there is a way to get the obscured level 9 password. See if you can figure out how...

This level seems a lot trickier then it actually is, and it helps to have an understanding of how the script validates the user's input. The script finds the first occurrence of '<--', and looks to see what follows directly after it.

From <https://www.hackthissite.org/missions/basic/9/> 

We know the password file is once again in the directory we are currently at, and that we can use the function from the last challenge that we injected a PHP script, we can do that once again only to list the content of our current directory, we pass the string "<!--#exec cmd="ls ../../9"-->" and the file displays:
"Hi, index.php p91e283zc3.php! Your name contains 24 characters."
We put the "p91e283zc3.php" file in the our current directory in the URL and get the password: "80013d75"
