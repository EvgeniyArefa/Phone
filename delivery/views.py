from django.shortcuts import render


def delivery(request):
    
    context ={
        'page_header': 'Home page title',

    }
    return render(request, 'delivery/delivery.html', context)