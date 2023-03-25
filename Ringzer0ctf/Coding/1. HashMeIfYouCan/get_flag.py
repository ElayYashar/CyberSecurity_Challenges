#! The challenge is now different and thus this solution is not relevent

import requests
import hashlib

#Functions

def hashMessage(messageToHash):
    h = hashlib.sha512()
    h.update(messageToHash.encode("utf-8"))

    return h.hexdigest()


def getMessage(challangeContent):
    startIndex = challangeContent.rfind(beginMessage) + len(beginMessage)
    stopIndex = challangeContent.rfind(endMessage)
    message = challangeContent[startIndex:stopIndex].replace(br,'').strip()

    return message


def getFlag(flagContent):
    flagStop = "<strong>You"
    flagStartIndex = flagContent.rfind("FLAG-") + len("FLAG-")
    flagStopIndex = flagContent.rfind(flagStop)
    flag = flagContent[flagStartIndex:flagStopIndex].strip()
    flag = "FLAG-" + flag.replace("</div>","")

    return flag

#Functions

loginUrl = 'https://ringzer0ctf.com/login'
challangeUrl = 'https://ringzer0ctf.com/challenges/13'
beginMessage = '----- BEGIN MESSAGE -----'
endMessage = '----- END MESSAGE -----'
br = '<br />'

#Session
s = requests.Session()

#Login
s.post(loginUrl,dict(username='username',password='password'))

#Get the challange content
challangeContent = s.post(challangeUrl).text

#Extract the message
message = getMessage(challangeContent)

#Hash the message
hashedMessage = hashMessage(message)

#Send the message to the challange
flagUrl = challangeUrl + '/' + str(hashedMessage)

flagContent = s.get(flagUrl).text

#Get the flag
flag = getFlag(flagContent)

print(flag)
