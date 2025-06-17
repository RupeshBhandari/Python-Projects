from .socket_manager import SocketManager
from .request_handler import RequestHandler
from .request import HttpRequest
from .response import HttpResponse
from src.utils.logger import Logger


class WebServer:
    def __init__(self, host="127.0.0.1", port=8080, connection_timeout=30):
        self.logger = Logger("web_server")
        self.socket_manager = SocketManager(
            host, port, backlog=5, connection_timeout=connection_timeout
        )
        self.request_handler = RequestHandler()
        self.running = False

    def start(self):
        """Start the web server."""
        if self.socket_manager.initialize():
            self.running = True
            self.logger.info(
                f"Web server started on http://{self.socket_manager.host}:{self.socket_manager.port}"
            )

            try:
                # Start the event loop
                self.socket_manager.start()
            except KeyboardInterrupt:
                self.logger.info("Server shutdown requested")
            finally:
                self.stop()
        else:
            self.logger.error("Failed to start web server")

    def stop(self):
        """Stop the web server."""
        if self.running:
            self.socket_manager.shutdown()
            self.running = False
            self.logger.info("Web server stopped")
