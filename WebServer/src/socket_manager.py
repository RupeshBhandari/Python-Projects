import socket
import selectors
import time
import queue
from collections import defaultdict
from src.response import HttpResponse
from src.utils.logger import Logger


class SocketManager:
    def __init__(self, host="127.0.0.1", port=8080, backlog=5, connection_timeout=30):
        self.host = host
        self.port = port
        self.backlog = backlog
        self.server_socket = None
        self.selector = selectors.DefaultSelector()
        self.logger = Logger("socket_manager")
        self.running = False

        # New attributes for improved selector usage
        self.connection_timeout = connection_timeout  # Timeout in seconds
        self.client_last_activity = {}  # Track when clients were last active
        self.outgoing_data = defaultdict(
            queue.Queue
        )  # Queued data to be sent to clients
        self.request_queue = queue.Queue(maxsize=100)  # Queue for pending requests

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
            self.selector.register(
                self.server_socket, selectors.EVENT_READ, self._accept_connection
            )

            self.logger.info(f"Socket initialized on {self.host}:{self.port}")
            return True
        except Exception as e:
            self.logger.error(f"Socket initialization failed: {e}")
            return False

    def start(self):
        """Start the socket manager's main event loop."""
        self.running = True
        last_cleanup_time = time.time()

        # Main server loop
        while self.running:
            # Wait for I/O events with a short timeout
            events = self.selector.select(timeout=1)

            # Process any events
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)

            # Periodically clean up idle connections (every 5 seconds)
            current_time = time.time()
            if current_time - last_cleanup_time > 5:
                self._cleanup_idle_connections()
                last_cleanup_time = current_time

    def _accept_connection(self, server_socket, mask):
        """Accept a new connection from a client."""
        client_socket, addr = server_socket.accept()
        self.logger.info(f"Accepted connection from {addr[0]}:{addr[1]}")

        # Set client socket to non-blocking
        client_socket.setblocking(False)

        # Track the client's last activity time
        self.client_last_activity[client_socket] = time.time()

        # Register client socket with the selector for READ events initially
        self.selector.register(
            client_socket, selectors.EVENT_READ, self._handle_client_data
        )

        return client_socket, addr

    def _handle_client_data(self, sock, mask):
        """Handle client data, parse request and send response."""
        try:
            # Update the client's last activity time
            self.client_last_activity[sock] = time.time()

            data = sock.recv(4096)

            if data:
                # Process the received data
                from src.request import HttpRequest

                # Parse the HTTP request (for logging/debugging purposes)
                HttpRequest.create_http_request(data=data)

                # Create a response (this could be processed more thoroughly)
                response = HttpResponse()
                response_data = response.with_text("hello").build()

                # Ensure response is bytes
                if isinstance(response_data, str):
                    response_data = response_data.encode("utf-8")

                # Queue the response data for sending
                self.outgoing_data[sock].put(response_data)

                # Update the selector to also monitor for WRITE events
                self.selector.modify(
                    sock,
                    selectors.EVENT_READ | selectors.EVENT_WRITE,
                    self._handle_client_io,
                )

                return data
            else:
                # No data means client closed connection
                self.logger.info("Client disconnected")
                self._close_connection(sock)

        except Exception as e:
            self.logger.error(f"Error handling client data: {e}")
            self._close_connection(sock)
            return None

    def _close_connection(self, client_socket):
        """Close a client connection and clean up related resources."""
        try:
            # Unregister from the selector
            self.selector.unregister(client_socket)

            # Clean up related data structures
            if client_socket in self.client_last_activity:
                del self.client_last_activity[client_socket]

            if client_socket in self.outgoing_data:
                del self.outgoing_data[client_socket]
        except Exception as e:
            self.logger.error(f"Error during connection cleanup: {e}")

        # Close the socket
        try:
            client_socket.close()
        except Exception as e:
            self.logger.error(f"Error closing socket: {e}")

    def send_response(self, client_socket, response_data):
        """Send data to the client."""
        try:
            # Ensure we always send bytes, not strings
            if isinstance(response_data, str):
                response_data = response_data.encode("utf-8")

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
                print(key, mask)
                callback_function = key.data
                client_socket = key.fileobj
                callback_function(client_socket)

    def _handle_client_io(self, sock, mask):
        """Handle both reading from and writing to client sockets based on events."""
        # Update the client's last activity time
        self.client_last_activity[sock] = time.time()

        # Handle read events
        if mask & selectors.EVENT_READ:
            try:
                data = sock.recv(4096)

                if data:
                    # Process received data
                    from src.request import HttpRequest

                    # Parse the HTTP request
                    HttpRequest.create_http_request(data=data)

                    # Create and queue a response
                    response = HttpResponse()
                    response_data = response.with_text(
                        "hello from improved selector"
                    ).build()

                    # Ensure response is bytes
                    if isinstance(response_data, str):
                        response_data = response_data.encode("utf-8")

                    # Queue the response data for sending
                    self.outgoing_data[sock].put(response_data)
                else:
                    # No data means client closed connection
                    self.logger.info("Client disconnected")
                    self._close_connection(sock)
                    return
            except Exception as e:
                self.logger.error(f"Error handling client data: {e}")
                self._close_connection(sock)
                return

        # Handle write events
        if mask & selectors.EVENT_WRITE:
            try:
                # Check if we have data to send for this client
                if not self.outgoing_data[sock].empty():
                    data_to_send = self.outgoing_data[sock].get()
                    bytes_sent = sock.send(data_to_send)

                    # If we couldn't send all data at once, queue the remainder
                    if bytes_sent < len(data_to_send):
                        remaining_data = data_to_send[bytes_sent:]
                        self.outgoing_data[sock].put(remaining_data)
                    else:
                        self.logger.info(
                            f"Successfully sent {bytes_sent} bytes to client"
                        )

                        # If this is an HTTP response, we can close the connection
                        # or reset to just listen for new requests (READ only)
                        if self.outgoing_data[sock].empty():
                            self.selector.modify(
                                sock, selectors.EVENT_READ, self._handle_client_io
                            )
            except Exception as e:
                self.logger.error(f"Error sending data to client: {e}")
                self._close_connection(sock)

    def _cleanup_idle_connections(self):
        """Close connections that have been idle for too long."""
        current_time = time.time()

        # Create a list of sockets to check (copy to avoid modification during iteration)
        sockets_to_check = list(self.client_last_activity.keys())

        for sock in sockets_to_check:
            # Skip the server socket
            if sock == self.server_socket:
                continue

            last_activity_time = self.client_last_activity.get(sock)
            if (
                last_activity_time
                and (current_time - last_activity_time) > self.connection_timeout
            ):
                self.logger.info(
                    f"Closing idle connection (inactive for {self.connection_timeout}s)"
                )
                self._close_connection(sock)

    def shutdown(self):
        """Clean shutdown of the socket manager."""
        self.running = False

        # Close all client connections
        for sock in list(self.client_last_activity.keys()):
            if sock != self.server_socket:
                self.logger.info("Closing client connection during shutdown")
                self._close_connection(sock)

        # Close the server socket
        if self.server_socket:
            try:
                self.selector.unregister(self.server_socket)
            except Exception:
                pass
            self.server_socket.close()
            self.server_socket = None

        # Close the selector
        self.selector.close()

        self.logger.info("Socket manager shutdown completed")
