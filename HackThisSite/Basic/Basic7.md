Description:
This time Network Security Sam has saved the unencrypted level7 password in an obscurely named file saved in this very directory.

In other unrelated news, Sam has set up a script that returns the output from the UNIX cal command. Here is the script:

Enter the year you wish to view and hit 'view'.

From <https://www.hackthissite.org/missions/basic/7/> 

We know that Sam has saved the password file in the same directory that  we are at, and the he using a UNIX command and displaying it's content in a different page. If we know that there is a file in the same directory we are at and that a UNIX command is being used, the "ls" command can be of use to us, the problem is how to send our command to the server and to have the content of it displayed.
We can use an attack called "Command Injection", by passing "; ls" we tell the server to close the "cal" command and now to use the "ls" command. The file displays: 

index.php
level7.php
cal.pl
.
..
k1kh31b1n55h.php

If we pass the "k1kh31b1n55h.php" file in the URL, it's content is the password "b9020e61".