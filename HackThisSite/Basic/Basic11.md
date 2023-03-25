In this challenge we get no description.

This page cycles through songs of the Artist: "Elton John", if we view the page in DEV TOOLS we can see a comment that stats: 

<!--We even have our own collection - if you could find it!-->

This means there are other files or other directories we need to find.
By using the command gobuster to brute force directories, we can find the directory /e. If we open it we can cycle through directories until we get to the path /e/l/t/o/n. 
The file .htaccess is also on the machine:

IndexIgnore DaAnswer.* .htaccess
<Files .htaccess>
require all granted
</Files>

We can see there is a file named "DaAnswer", if we put it in the URL, it displays:

"The answer is close! Just look a little harder."

I tried many solutions but got none, until I realized the answer is right in front of me, literally.
(The password is  "close").
