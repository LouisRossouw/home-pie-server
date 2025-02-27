def get_url(request):
    return f"{request.scheme}://{request.get_host()}"
