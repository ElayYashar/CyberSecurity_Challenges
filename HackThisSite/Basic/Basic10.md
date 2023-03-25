Description:
Please enter a password to gain access to level 10

From <https://www.hackthissite.org/missions/basic/10/> 

If we try to submit any password we get:
"You are not authorized to view this page"
This means we need to make to server think have authorization. We can use Burp Suite and change level10_authorized's value to "yes", or go to Application , and then Cookies in DEV TOOLS and do the same.
If we try to submit any password again we will be granted access.
