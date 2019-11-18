from django.shortcuts import render


def index(request):
    return render(request, 'htmls_t/test.html', {})
