from datetime import datetime
import json
from typing import Any, Dict, List, Optional, Union, Tuple

class HttpResponse:
    """
    An RFC-compliant HTTP response class supporting multiple content types.
    
    Generates actual HTTP response strings or byte arrays that can be sent
    directly to web browsers or HTTP clients.
    """
    
    # Content types
    CONTENT_TYPE_JSON = "application/json"
    CONTENT_TYPE_HTML = "text/html; charset=utf-8"
    CONTENT_TYPE_TEXT = "text/plain; charset=utf-8"
    CONTENT_TYPE_XML = "application/xml"
    CONTENT_TYPE_BINARY = "application/octet-stream"
    
    # HTTP version
    HTTP_VERSION = "HTTP/1.1"
    
    # RFC 7231 Standard Status Codes
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    CONFLICT = 409
    UNPROCESSABLE_ENTITY = 422
    INTERNAL_SERVER_ERROR = 500
    
    # Status code descriptions per RFC 7231
    _STATUS_MESSAGES = {
        200: "OK",
        201: "Created",
        202: "Accepted",
        204: "No Content",
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed",
        409: "Conflict",
        422: "Unprocessable Entity",
        500: "Internal Server Error"
    }
    
    def __init__(self, status_code: int = 200, content_type: str = None):
        """Initialize a new HTTP response with default values."""
        self.status_code = status_code
        self.status_message = self._STATUS_MESSAGES.get(status_code, "")
        self.headers = {
            "Date": self._format_http_date(datetime.utcnow()),
            "Server": "Python HttpResponse",
            "Connection": "close"
        }
        
        # Set default content type (JSON) if none specified
        self._content_type = content_type or self.CONTENT_TYPE_JSON
        if self._content_type:
            self.headers["Content-Type"] = self._content_type
        
        # Initialize different body representations
        self._raw_body = None
        self._json_body = {
            "data": None,
            "errors": [],
            "meta": {}
        } if self._content_type == self.CONTENT_TYPE_JSON else None
    
    def with_status(self, status_code: int) -> 'HttpResponse':
        """Set the status code and corresponding status message."""
        self.status_code = status_code
        self.status_message = self._STATUS_MESSAGES.get(status_code, "")
        return self
    
    def with_json_data(self, data: Any) -> 'HttpResponse':
        """Set JSON response payload data."""
        self._ensure_content_type(self.CONTENT_TYPE_JSON)
        self._json_body["data"] = data
        return self
    
    def with_error(self, 
                  message: str, 
                  code: Optional[str] = None, 
                  details: Optional[Union[List, Dict]] = None) -> 'HttpResponse':
        """Add a structured error to the JSON response."""
        self._ensure_content_type(self.CONTENT_TYPE_JSON)
        error = {"message": message}
        if code:
            error["code"] = code
        if details:
            error["details"] = details
        
        self._json_body["errors"].append(error)
        return self
    
    def with_meta(self, key: str, value: Any) -> 'HttpResponse':
        """Add metadata to the JSON response."""
        self._ensure_content_type(self.CONTENT_TYPE_JSON)
        self._json_body["meta"][key] = value
        return self
    
    def with_html(self, html_content: str) -> 'HttpResponse':
        """Set HTML content for the response."""
        self._content_type = self.CONTENT_TYPE_HTML
        self.headers["Content-Type"] = self.CONTENT_TYPE_HTML
        self._raw_body = html_content
        self._json_body = None
        return self
    
    def with_text(self, text_content: str) -> 'HttpResponse':
        """Set plain text content for the response."""
        self._content_type = self.CONTENT_TYPE_TEXT
        self.headers["Content-Type"] = self.CONTENT_TYPE_TEXT
        self._raw_body = text_content
        self._json_body = None
        return self
    
    def with_binary(self, binary_data: bytes) -> 'HttpResponse':
        """Set binary content for the response."""
        self._content_type = self.CONTENT_TYPE_BINARY
        self.headers["Content-Type"] = self.CONTENT_TYPE_BINARY
        self._raw_body = binary_data
        self._json_body = None
        return self
    
    def with_content(self, content: Any, content_type: str) -> 'HttpResponse':
        """Set arbitrary content with a specific content type."""
        self._content_type = content_type
        self.headers["Content-Type"] = content_type
        self._raw_body = content
        self._json_body = None
        return self
        
    def with_header(self, name: str, value: str) -> 'HttpResponse':
        """Set an HTTP header according to RFC specifications."""
        canonical_name = '-'.join(word.capitalize() for word in name.split('-'))
        self.headers[canonical_name] = value
        return self
        
    def _format_http_date(self, dt: datetime) -> str:
        """Format a datetime as per RFC 7231 section 7.1.1.1."""
        return dt.strftime("%a, %d %b %Y %H:%M:%S GMT")
    
    def _ensure_content_type(self, required_type: str):
        """Ensure the response has the required content type."""
        if self._content_type != required_type:
            self._content_type = required_type
            self.headers["Content-Type"] = required_type
            if required_type == self.CONTENT_TYPE_JSON and self._json_body is None:
                self._json_body = {
                    "data": None,
                    "errors": [],
                    "meta": {}
                }
                self._raw_body = None
    
    def _prepare_body(self) -> Tuple[Optional[Union[str, bytes]], bool]:
        """Prepare the response body based on content type."""
        is_binary = False
        
        if self.status_code == self.NO_CONTENT:
            # No content responses should not include a body
            if "Content-Type" in self.headers:
                del self.headers["Content-Type"]
            if "Content-Length" in self.headers:
                del self.headers["Content-Length"]
            return None, is_binary
        
        # Prepare the body based on content type
        if self._content_type == self.CONTENT_TYPE_JSON and self._json_body is not None:
            # Clean up empty collections for JSON
            json_body = dict(self._json_body)
            if not json_body["errors"]:
                json_body["errors"] = None
                
            if not json_body["meta"]:
                json_body["meta"] = None
            
            # Serialize JSON
            body = json.dumps(json_body)
            
        elif isinstance(self._raw_body, bytes):
            # Binary content
            body = self._raw_body
            is_binary = True
        else:
            # Other string-based content (HTML, text, etc)
            body = self._raw_body
        
        # Calculate content length
        if body is not None:
            if isinstance(body, str):
                self.headers["Content-Length"] = str(len(body.encode("utf-8")))
            elif isinstance(body, bytes):
                self.headers["Content-Length"] = str(len(body))
        
        return body, is_binary
    
    def build(self) -> Union[str, bytes]:
        """
        Generate a complete HTTP response ready to be sent to a client.
        
        Returns:
            str or bytes: Complete HTTP response including status line,
                         headers and body. Returns bytes for binary content
                         or string for text content.
        """
        body, is_binary = self._prepare_body()
        
        # Build status line
        status_line = f"{self.HTTP_VERSION} {self.status_code} {self.status_message}"
        
        # Build headers
        header_lines = []
        for name, value in self.headers.items():
            header_lines.append(f"{name}: {value}")
        
        # Combine parts with proper CRLF line endings
        if is_binary:
            # For binary responses, return bytes
            response_head = (status_line + "\r\n" + "\r\n".join(header_lines) + "\r\n\r\n").encode('utf-8')
            if body is not None:
                return response_head + body
            return response_head
        else:
            # For text responses, return string
            response = status_line + "\r\n" + "\r\n".join(header_lines) + "\r\n\r\n"
            if body is not None:
                response += body
            return response
    
    @classmethod
    def json(cls, data: Any = None, meta: Optional[Dict] = None) -> 'HttpResponse':
        """Create a JSON response."""
        response = cls(cls.OK, cls.CONTENT_TYPE_JSON).with_json_data(data)
        if meta:
            for key, value in meta.items():
                response.with_meta(key, value)
        return response
    
    @classmethod
    def html(cls, html_content: str) -> 'HttpResponse':
        """Create an HTML response."""
        return cls(cls.OK, cls.CONTENT_TYPE_HTML).with_html(html_content)
    
    @classmethod
    def text(cls, text_content: str) -> 'HttpResponse':
        """Create a plain text response."""
        return cls(cls.OK, cls.CONTENT_TYPE_TEXT).with_text(text_content)
    
    @classmethod
    def created(cls, data: Any = None, location: Optional[str] = None) -> 'HttpResponse':
        """Create a 201 Created response with proper Location header."""
        response = cls(cls.CREATED, cls.CONTENT_TYPE_JSON).with_json_data(data)
        if location:
            response.with_header("Location", location)
        return response
    
    @classmethod
    def no_content(cls) -> 'HttpResponse':
        """Create a 204 No Content response."""
        return cls(cls.NO_CONTENT)
    
    @classmethod
    def error(cls, 
             status_code: int = 400, 
             message: str = "An error occurred", 
             code: Optional[str] = None, 
             details: Optional[Union[List, Dict]] = None) -> 'HttpResponse':
        """Create a JSON error response."""
        return cls(status_code, cls.CONTENT_TYPE_JSON).with_error(message, code, details)
    
    @classmethod
    def not_found(cls, resource_type: str = "Resource", content_type: str = None) -> 'HttpResponse':
        """Create a 404 Not Found response."""
        if content_type == cls.CONTENT_TYPE_HTML:
            html = f"<html><body><h1>404 Not Found</h1><p>The requested {resource_type} could not be found.</p></body></html>"
            return cls(cls.NOT_FOUND, cls.CONTENT_TYPE_HTML).with_html(html)
        else:
            message = f"{resource_type} not found"
            return cls(cls.NOT_FOUND, cls.CONTENT_TYPE_JSON).with_error(message, "NOT_FOUND")