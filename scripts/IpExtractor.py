def extract_ip(request):
    # Check if the request has the 'X-Forwarded-For' header
    if 'X-Forwarded-For' in request.headers:
        # The first IP in the list is the original client IP
        ip = request.headers['X-Forwarded-For'].split(',')[0]
    else:
        # Fallback to the remote address of the request
        ip = request.remote_addr

    return ip


