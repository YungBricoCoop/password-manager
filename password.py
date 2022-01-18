import os
import base64
from rich.console import Console
from rich.table import Table
from rich import print
from getpass import getpass
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random

ENCODING = "latin-1"

def encrypt(key, source, encode=True):
    key = key.encode(ENCODING)
    source = source.encode(ENCODING)
    key = SHA256.new(key).digest()  
    IV = Random.new().read(AES.block_size)  
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    padding = AES.block_size - len(source) % AES.block_size 
    source += bytes([padding]) * padding 
    data = IV + encryptor.encrypt(source)  
    return base64.b64encode(data).decode(ENCODING) if encode else data

def decrypt(key, source, decode=True):
    try:
        key = key.encode(ENCODING)
        if decode:
            source = base64.b64decode(source.encode(ENCODING))
        key = SHA256.new(key).digest() 
        IV = source[:AES.block_size]
        decryptor = AES.new(key, AES.MODE_CBC, IV)
        data = decryptor.decrypt(source[AES.block_size:])  
        padding = data[-1]  
        return data[:-padding].decode(ENCODING) 
    except:
        return ""

def writeLine(username,password,lines):
    with open("password.txt","a") as f:
        f.write(username+" : "+password+"\n")
    lines.append([username,password])

def readlines():
    result = []
    with open("password.txt") as f:
        for l in f.readlines():
            l = l.strip().split(" : ")
            result.append(l)
    return result

def decryptAll(password,lines):
    for l in lines:
        l[1] = decrypt(password,l[1])

def createPasswordFile():
    if(not os.path.isfile("password.txt")):
        f = open("password.txt","w+")
        f.close()

def displayAccounts(lines,table):
    n = 0
    for l in lines :
        n+=1
        if(len(l)==2):
            table.add_row(
                str(n),
                l[0],
                l[1],)

if __name__ == "__main__":
    createPasswordFile()
    
    console = Console()

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=12)
    table.add_column("Account")
    table.add_column("Password")

    password = getpass()
    lines = readlines()
    displayAccounts(lines,table)
    console.print(table)
    run = True
    while run:
        result = Table(show_header=True, header_style="bold magenta")
        result.add_column("ID", style="dim", width=12)
        result.add_column("Account")
        result.add_column("Password")
        lines = readlines()
        print("1 : Decrypt an account\n2 : Decrypt all accounts\n3 : Add an account")
        param = input("Choose an option : ")

        if(param == "1"):
            number = input("Account ID : ")
            lines = [[lines[int(number)-1][0],decrypt(password,lines[int(number)-1][1])]]

        if(param == "2"):
            decryptAll(password,lines)

        if(param == "3"):
            account = input("Account name : ")
            accountPassword = input("Password : ")
            writeLine(account,encrypt(password,accountPassword),lines)

        displayAccounts(lines,result)
        console.print(result)
        
        run = "y" == input("Do you want to continue ? (y/n) : ")
    