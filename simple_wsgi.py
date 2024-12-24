from urllib.parse import parse_qs

HELLO_WORLD = b"Hello world!\n"

def simple_app(environ, start_response):
    status = '200 OK'
    print("WSGI Environ:", environ)
    
    query_params = parse_qs(environ.get('QUERY_STRING', ''))
    print("Query Params:", query_params)
    
    try:
        content_length = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError, TypeError):
        content_length = 0

    body = environ['wsgi.input'].read(content_length)
    post_params = parse_qs(body.decode())
    print("Parsed Body:", post_params)
    
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return [HELLO_WORLD]

application = simple_app
