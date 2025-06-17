import logging
from .socket_manager import SocketManager
from .request_handler import RequestHandler
from .request import HttpRequest
from .response import HttpResponse
from src.utils.logger import Logger
class WebServer:
    def __init__(self, host='127.0.0.1', port=8080):
        self.logger = Logger('web_server')
        self.socket_manager = SocketManager(host, port)
        self.request_handler = RequestHandler()
        self.running = False
        
    def start(self):
        """Start the web server."""
        if self.socket_manager.initialize():
            self.running = True
            self.logger.info(f"Web server started on http://{self.socket_manager.host}:{self.socket_manager.port}")
            
            try:
                # Start the event loop
                self.socket_manager.run_event_loop(self._process_client_request)
            except KeyboardInterrupt:
                self.logger.info("Server shutdown requested")
            finally:
                self.stop()
        else:
            self.logger.error("Failed to start web server")
    
    def _process_client_request(self, client_socket):
        """Process a client request."""
        try:
            # Receive data from client
            data = self.socket_manager._handle_client_data(client_socket)
            
            if data:
                # Parse the HTTP request
                request = HttpRequest.parse(data.decode('utf-8', errors='replace'))
                
                # Handle the request
                response = self.request_handler.handle_request(request)
                
                # Send the response
                self.socket_manager.send_response(client_socket, str(response).encode('utf-8'))
                
                # Close connection if not keep-alive
                if not request.headers.get('Connection') == 'keep-alive':
                    self.socket_manager._close_connection(client_socket)
        except Exception as e:
            self.logger.error(f"Error processing request: {e}")
            # Send error response
            error_response = HttpResponse(500, "Internal Server Error")
            self.socket_manager.send_response(client_socket, str(error_response).encode('utf-8'))
            self.socket_manager._close_connection(client_socket)
    
    def stop(self):
        """Stop the web server."""
        if self.running:
            self.socket_manager.shutdown()
            self.running = False
            self.logger.info("Web server stopped")