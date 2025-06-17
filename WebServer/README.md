# Plan
1. Create a basic web server without using Python's built-in HTTP server.
2. Implement request handling to serve HTML files.
3. Add support for serving static files (CSS, JS, images).
4. Implement a simple routing mechanism for different endpoints.
5. Add error handling for 404 Not Found and 500 Internal Server Error.

custom-web-server/
├── core/
│   ├── server.py       # Main server class
│   ├── socket_manager.py
│   ├── request.py      # HTTP request parsing
│   ├── response.py     # HTTP response generation
│   └── config.py       # Server configuration
├── routing/
│   ├── router.py       # URL routing system
│   └── middleware.py   # Request/response interceptors
├── handlers/
│   ├── base_handler.py # Abstract handler class
│   ├── static_handler.py
│   └── api_handler.py
├── utils/
│   ├── logger.py       # Logging functionality
│   ├── errors.py       # Error handling
│   └── helpers.py      # Utilities
├── public/             # Static files directory
├── templates/          # HTML templates
├── config/
│   └── server.json     # Configuration files
├── main.py             # Server entry point
└── tests/              # Test directory



# Web Server Implementation
- Request
    - parsing and creating the request object   
- Response
    - generating and sending the response
    -  handling different response types (HTML, JSON, etc.)
- Routing
  -  handling different routes and endpoints