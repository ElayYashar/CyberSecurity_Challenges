from urllib.request import urlopen
from bs4 import BeautifulSoup
from hashlib import sha512
import binascii

CHALLENGE_URL = "https://ringzer0ctf.com/challenges/14"
FLAG_URL = "http://challenges.ringzer0team.com:10014/"
ANSWER = "?r=" # + hashed flag

def getMessageFromHtml(html) -> str:
    response_list = html.split()
    message = response_list[-11]
    return message[0:len(message)-3]

def binaryToAscii(binary_msg: str):
    n = int(binary_msg, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()

def hashMessage(message: str) -> str:    
    return sha512(message.encode()).hexdigest()

def main():
    # Get the HTML for the msg to hash
    msg_html = urlopen(FLAG_URL).read().decode('utf-8')
    
    # Extract the message from the content
    message = getMessageFromHtml(msg_html)

    # Hash the message
    ascii_msg = binaryToAscii(message)
    flag = hashMessage(ascii_msg)
    
    # Form the answer URL
    answer_url = FLAG_URL + ANSWER + flag
        
    # Send the hashed message to the answer URL  - End of 2 second countdown
    answer_page_html = urlopen(answer_url).read().decode('utf-8')
        
    try:
        response = BeautifulSoup(answer_page_html, 'html.parser').find(class_="alert alert-info").getText()
        print(response)
    except:
        print("Wrong Message!")

if __name__ == '__main__': main()