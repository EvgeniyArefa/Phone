from django.shortcuts import render


def home(request):
    
    context ={
        'page_header': 'Home page title',

    }
    return render(request, 'home/home.html', context)