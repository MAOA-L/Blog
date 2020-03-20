def django_http_filter(request):
    print(request.path)
    return True
