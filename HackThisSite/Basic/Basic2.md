Description: 
Network Security Sam set up a password protection script. He made it load the real password from an 
unencrypted text file and compare it to the password the user enters. However, he neglected to 
upload the password file...
From <https://www.hackthissite.org/missions/basic/2/> 
Because Sam didn’t upload any password file, the program is comparing the password to an empty 
string, and so if we put an empty string in the password it will return true and let us through.
