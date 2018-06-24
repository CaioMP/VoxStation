from django.shortcuts import render


def IndexView(request):
    return render(request, './home/index.html', {'logado': request.user.is_active})


def search(request):
    return render(request, './home/search.html')
