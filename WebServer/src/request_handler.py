import os
import mimetypes
import logging
from pathlib import Path
from .response import HttpResponse
from .request import HttpRequest

class RequestHandler:
    def __init__(self, document_root="public", routes=None):
        self.document_root = document_root
        self.routes = routes or {}  # Dictionary mapping paths to handler functions
        self.logger = logging.getLogger('request_handler')
        
        # Initialize mime types
        mimetypes.init()
        
    def handle_request(self, request):
        """Main entry point for handling an HTTP request"""
        try:
            # Log the request
            self.logger.info(f"{request.method} {request.path} HTTP/{request.version}")
            
            # Check if we have a registered route handler
            if self.routes and request.path in self.routes:
                print('routesss')
                handler = self.routes[request.path]
                return handler(request)
            
            # If no specific route, try to serve a file
            return self._serve_file(request)
        except Exception as e:
            self.logger.error(f"Error handling request: {e}")
            return HttpResponse(500, "Internal Server Error", 
                               {"Content-Type": "text/plain"}, 
                               "500 Internal Server Error")
                
    def _serve_file(self, request):
        """Serve a static file"""
        # Normalize path to prevent directory traversal attacks
        target_path = self._normalize_path(request.path)
        
        # Check if file exists
        if not os.path.exists(target_path) or not os.path.isfile(target_path):
            return HttpResponse(404, "Not Found", 
                               {"Content-Type": "text/plain"}, 
                               "404 Not Found")
        
        # Determine content type
        content_type, encoding = mimetypes.guess_type(target_path)
        if content_type is None:
            content_type = "application/octet-stream"
            
        # Read file content
        try:
            with open(target_path, 'rb') as f:
                content = f.read()
                
            # Return success response with file content
            headers = {
                "Content-Type": content_type,
                "Content-Length": str(len(content))
            }
            
            return HttpResponse(200, "OK", headers, content)
        except IOError as e:
            self.logger.error(f"Error reading file {target_path}: {e}")
            return HttpResponse(500, "Internal Server Error",
                               {"Content-Type": "text/plain"},
                               "500 Internal Server Error")
    
    def _normalize_path(self, path):
        """Convert URL path to file system path, preventing traversal attacks"""
        # Remove query string if present
        if '?' in path:
            path = path.split('?', 1)[0]
            
        # Convert URL path to filesystem path
        if path == '/':
            path = '/index.html'  # Default document
            
        # Ensure path starts with / and remove any ../ components
        path = os.path.normpath('/' + path.lstrip('/'))
        
        # Join with document root to get absolute path
        full_path = os.path.join(self.document_root, path.lstrip('/'))
        
        # Final security check to ensure we're still within document root
        root_path = os.path.abspath(self.document_root)
        full_path = os.path.abspath(full_path)
        
        if not full_path.startswith(root_path):
            # Attempt to access file outside document root
            return os.path.join(self.document_root, 'index.html')
            
        return full_path
    
    def register_route(self, path, handler_func):
        """Register a handler function for a specific path"""
        self.routes[path] = handler_func