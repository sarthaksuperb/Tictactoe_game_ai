from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

if __name__ == '__main__':
    server = ThreadingHTTPServer(('0.0.0.0', 8080), SimpleHTTPRequestHandler)
    server.serve_forever()
