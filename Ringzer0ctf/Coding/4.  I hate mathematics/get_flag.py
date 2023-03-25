import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen

CHALLENGE_URL = "http://challenges.ringzer0team.com:10032/"
BEGIN_MESSAGE = '----- BEGIN MESSAGE -----'
END_MESSAGE = '----- END MESSAGE -----'

def getEquation(html) -> list:
    list = html.split()
    dec = list[-17]
    hex = list[-15]
    bin = list[-13]
    
    equation: list = [dec, hex, bin]
    return equation

def solve(equation: list) -> int:
    dec = int(equation[0])
    hex = int(equation[1], 16)
    bin = int(equation[2], 2)

    return dec + hex - bin

def main():
    html = urlopen(CHALLENGE_URL).read().decode('utf-8')
    equation = getEquation(html)
    
    flag_html = urlopen(CHALLENGE_URL + "?r=" + str(solve(equation))).read().decode('utf-8')
    # flag
    print(BeautifulSoup(flag_html, 'html.parser').find(class_='alert alert-info').getText())

if __name__ == '__main__': main()