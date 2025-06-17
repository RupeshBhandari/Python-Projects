import http.server

class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Handle GET requests
        if self.path == '/':
            self.path = 'index.html'  # Serve index.html for root path
        return super().do_GET()

    def log_message(self, format, *args):
        # Override to customize logging
        print("%s - - [%s] %s" %
              (self.client_address[0], self.log_date_time_string(), format % args))
        

def run(server_class=http.server.HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print('Server stopped.')


if __name__ == "__main__":
    run(port=8000)  # You can change the port number if needed