class Elapsed:
    def __init__(self, elapsed: float) -> None:
        self.elapsed = elapsed

    def total_seconds(self):
        return self.elapsed


class Response:
    def __init__(self, headers: dict = {}, text: str = '', res_code: int = 200, reason: str = 'OK') -> None:
        self.reason = reason
        self.status_code = res_code
        self.headers = headers
        self.text = text

    def from_raw(self, raw: str) -> None:
        if not raw:
            return
        raw_headers, body = tuple(raw.split('\r\n\r\n', 1))
        self.text = body
        header_lines = raw_headers.splitlines()
        status_line = header_lines[0]
        http_ver, status_code, reason = tuple(status_line.split(' ', 2))
        self.http_ver = http_ver
        self.status_code = int(status_code)
        self.reason = reason
        self.headers = {}
        for h in header_lines[1:]:
            key, val = tuple(h.split(':', 1))
            self.headers[key] = val.strip()

    def to_raw(self, ):
        res = f'HTTP/1.1 {self.status_code} {self.reason}'
        raw_headers = '\r\n'.join(list(map(lambda x: f'{x[0]}: {x[1]}', self.headers.items())))
        if raw_headers:
            raw_headers = f'\r\n{raw_headers}'
        return f'{res}{raw_headers}\r\nContent-Length: {len(self.text)}\r\nConnection: close\r\n\r\n{self.text}'

    def __str__(self) -> str:
        return self.text
