class Elapsed:
    def __init__(self, elapsed: float) -> None:
        self.elapsed = elapsed

    def total_seconds(self):
        return self.elapsed


class Request:
    def __init__(self, url: str = '', text: str = '', headers: dict = {}) -> None:
        if not url:
            return
        self.headers = headers
        self.text = text
        self.url = url
        protocol, url_parts = tuple(self.url.split('://', 1))
        host_and_port, path = tuple(url_parts.split('/', 1)) if '/' in url_parts else (url_parts, '')
        if ':' not in host_and_port:
            port = 443 if protocol == 'https' else 80
            host_and_port = f'{host_and_port}:{port}'
        host, port = tuple(host_and_port.split(':', 1))
        self.host = host
        self.port = port
        self.protocol = protocol
        self.path = path
        self.method = None

    def from_raw(self, raw: str) -> None:
        if not raw:
            return
        raw_headers, body = tuple(raw.split('\r\n\r\n', 1))
        self.text = body
        header_lines = raw_headers.splitlines()
        method_line = header_lines[0]
        method, http_ver = tuple(method_line.split(' ', 1))
        self.http_ver = http_ver
        self.method = method
        self.headers = {}
        for h in header_lines[1:]:
            key, val = tuple(h.split(':', 1))
            self.headers[key] = val.strip()

    def to_raw(self):
        raw_headers = '\r\n'.join(list(map(lambda x: f'{x[0]}: {x[1]}', self.headers.items())))
        if raw_headers:
            raw_headers = f'\r\n{raw_headers}'
        request = f'POST /{self.path} HTTP/1.1{raw_headers}\r\nContent-Length: {len(self.text)}\r\nHost: {self.host}:{self.port}\r\nConnection: close\r\n\r\n{self.text}'
        return request

    def __str__(self) -> str:
        return self.text
