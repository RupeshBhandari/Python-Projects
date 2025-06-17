class HttpRequest:
    def __init__(self, method, path, protocol, headers, data=None):
        self.method = method
        self.path = path
        self.protocol = protocol
        self.headers = headers
        self.data = data

    @classmethod
    def parse(cls, raw_request):
        # Parse the raw HTTP request
        # First, ensure we're working with a string
        if isinstance(raw_request, bytes):
            raw_request = raw_request.decode("utf-8")

        # Split the request into lines
        lines = raw_request.strip().split("\n")

        # Parse the request line (first line)
        if lines:
            method, path, protocol = lines[0].split()
        else:
            method, path, protocol = "", "", ""

        # Parse headers
        headers = {}
        i = 1
        while i < len(lines) and lines[i]:
            key, value = lines[i].split(":", 1)
            headers[key.strip()] = value.strip()
            i += 1

        # Parse body if any
        data = None
        if i < len(lines) - 1:
            data = "\n".join(lines[i + 1 :])

        return method, path, protocol, headers, data

    @classmethod
    def create_http_request(cls, data):
        # Parse the request and create a new HttpRequest object
        method, path, protocol, headers, body = cls.parse(data)
        return HttpRequest(method, path, protocol, headers, body)


if __name__ == "__main__":
    http_request_object = HttpRequest.create_http_request(
        """
GET /acca/ HTTP/1.1
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: en-US,en;q=0.9
Cache-Control: no-cache
Connection: keep-alive
Host: opentuition.com
Pragma: no-cache
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36
sec-ch-ua: "Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "macOS"
"""
    )
    print(http_request_object.method)
    print(http_request_object.path)
    print(http_request_object.protocol)
    print(http_request_object.headers)
