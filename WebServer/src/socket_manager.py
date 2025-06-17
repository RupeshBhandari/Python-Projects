import socket
import selectors
import logging

class SocketManager:
    def __init__(self, host='127.0.0.1', port=8080, backlog=5):
        self.host = host
        self.port = port
        self.backlog = backlog
        self.server_socket = None
        self.selector = selectors.DefaultSelector()
        self.logger = logging.getLogger('socket_manager')
        
    def initialize(self):
        """Create and configure the server socket."""
        try:
            # Create an IPv4 TCP socket
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Set socket options
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Bind the socket to the host and port
            self.server_socket.bind((self.host, self.port))
            
            # Start listening for connections
            self.server_socket.listen(self.backlog)
            
            # Set to non-blocking mode
            self.server_socket.setblocking(False)
            
            # Register the server socket with the selector
            self.selector.register(self.server_socket, selectors.EVENT_READ, self._accept_connection)
            
            self.logger.info(f"Socket initialized on {self.host}:{self.port}")
            return True
        except Exception as e:
            self.logger.error(f"Socket initialization failed: {e}")
            return False
    
    def _accept_connection(self, server_socket):
        """Accept a new connection from a client."""
        client_socket, addr = server_socket.accept()
        self.logger.info(f"Accepted connection from {addr[0]}:{addr[1]}")
        
        # Set client socket to non-blocking
        client_socket.setblocking(False)
        
        # Register client socket with the selector
        self.selector.register(client_socket, selectors.EVENT_READ, self._handle_client_data)
        
        return client_socket, addr
    
    def _handle_client_data(self, client_socket):
        """Basic handler for client data, to be overridden."""
        try:
            data = client_socket.recv(4096)
            if data:
                return data
            else:
                # No data means client closed connection
                self._close_connection(client_socket)
                return None
        except Exception as e:
            self.logger.error(f"Error handling client data: {e}")
            self._close_connection(client_socket)
            return None
    
    def _close_connection(self, client_socket):
        """Close a client connection."""
        self.selector.unregister(client_socket)
        client_socket.close()
    
    def send_response(self, client_socket, response_data):
        """Send data to the client."""
        try:
            client_socket.sendall(response_data)
            return True
        except Exception as e:
            self.logger.error(f"Error sending response: {e}")
            self._close_connection(client_socket)
            return False
    
    def run_event_loop(self, callback):
        """Run the event loop, calling callback with client data."""
        while True:
            events = self.selector.select()
            for key, mask in events:
                callback_function = key.data
                client_socket = key.fileobj
                callback_function(client_socket)
    
    def shutdown(self):
        """Clean shutdown of the socket manager."""
        if self.server_socket:
            self.selector.unregister(self.server_socket)
            self.server_socket.close()
            self.server_socket = None
        self.selector.close()