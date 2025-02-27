def get_url_full(request):
    return f"{request.scheme}://{request.get_host()}{request.get_full_path()}"
