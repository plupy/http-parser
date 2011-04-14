#!/usr/bin/env python
import socket

from http_parser.parser import HttpParser


def main():

    p = HttpParser()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    body = []
    try:
        s.connect(('gunicorn.org', 80))
        s.send("GET / HTTP/1.1\r\nHost: gunicorn.org\r\n\r\n")
        
        while True:
            data = s.recv(1024)
            if not data:
                break

            recved = len(data)
            nparsed = p.execute(data, recved)
            assert nparsed == recved

            if p.is_headers_complete():
                print p.get_headers()

            if p.is_partial_body():
                body.append(p.recv_body())

            if p.is_message_complete():
                break

        print "".join(body)
    
    finally:
        s.close()

if __name__ == "__main__":
    main()


