
from django.shortcuts import render


def home_view(request):
    hello = 'Hello World'

    context = {
        'hello': hello,
    }
    return render(request, 'main/home.html', context)