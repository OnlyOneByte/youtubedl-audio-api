from urllib.request import Request, urlopen
from urllib.error import HTTPError

from werkzeug.datastructures import Headers


def pipe(request, url, proxy):
    headers = {}
    if request.headers.get('Range'):
        headers['Range'] = request.headers.get('Range')
    request = Request(url, headers=headers)
    if proxy is not None:
        request.set_proxy(proxy, 'http')
        request.set_proxy(proxy, 'https')
    try:
        client = urlopen(request)

        def stream():
            continue_reading = True
            while continue_reading:
                bytes_read = client.read(10000)
                if len(bytes_read) == 0:
                    continue_reading = False
                else:
                    yield bytes_read

        headers = Headers()
        headers.add('Content-Type', client.getheader('Content-Type'))
        headers.add('Content-Length', client.getheader('Content-Length'))
        headers.add('Accept-Ranges', 'bytes')
        headers.add('Content-Range', client.getheader('Content-Range')) if request.headers.get('Range') else None

        return stream(), headers
    except HTTPError:
        return None, None


def pipe_headers(request, url, proxy):
    headers = {}
    if request.headers.get('Range'):
        headers['Range'] = request.headers.get('Range')
    request = Request(url, headers=headers, method="HEAD")
    if proxy is not None:
        request.set_proxy(proxy, 'http')
        request.set_proxy(proxy, 'https')
    try:
        client = urlopen(request)
        client.read()
        headers = Headers()
        headers.add('Content-Type', client.getheader('Content-Type'))
        headers.add('Content-Length', client.getheader('Content-Length'))
        headers.add('Accept-Ranges', 'bytes')
        headers.add('Content-Range', client.getheader('Content-Range')) if request.headers.get('Range') else None
        return headers
    except HTTPError:
        return None
