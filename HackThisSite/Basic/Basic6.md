Description:
Network Security Sam has encrypted his password. The encryption system is publically available and can be accessed with this form:

You have recovered his encrypted password. It is:
69g4jh;k

Decrypt the password and enter it below to advance to the next level.

From <https://www.hackthissite.org/missions/basic/6/> 

In this challenge we get a button that runs an encryption script and Sam's encrypted password.
To test the encryption, we pass the String "12345" to the encryption program, it returns "13579".
We can understand that the first character will be the same, the second one will be the value of the ascii table plus 1, the third one will be the value of the ascii table plus 2 and so one.
{
X1=X1+0 --> 1 + 0 = 1
X2=X2+1 --> 2 + 1 = 3 
X3=X3+2 --> 3 + 2 = 5 
X4=X4+3 --> 4 + 3 = 7 
X5=X5+4 --> 5 + 4 = 9
}
By writing a python script we can decrypt Sam's encrypted password and get: 68e1fc5d
Sam's password can be encrypted manually as well, but a python script is more neat and organized.


    # Script to decrypt Sam's Password. Algorithm may change from session to session

    def decryptPassword(encryptedPassword):
        decryptedPassword = ""
        for i in range(len(encryptedPassword)):
            decryptedPassword = decryptedPassword + chr(ord(encryptedPassword[i]) - i)
        return decryptedPassword

    print(decryptPassword("The Decrypted Password is: 69g4jh;k")) # Final Answer