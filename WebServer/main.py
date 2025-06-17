from src.server import WebServer


def main():
    # Use a different port to avoid conflicts and set a short connection timeout for testing
    server = WebServer(port=9090, connection_timeout=15)
    print("Starting improved web server with advanced selector handling...")
    print("- Monitoring for both READ and WRITE events")
    print("- Idle connection timeout: 15 seconds")
    print("- Queued response handling")
    print("Press Ctrl+C to stop the server")
    server.start()


if __name__ == "__main__":
    main()
