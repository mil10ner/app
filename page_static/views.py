from django.shortcuts import render,redirect
from .models import Table

def index(request):
    list_static = Table.objects.all()
    #print(list_static)
    return render(request, 'page_static/index.html', {'title': "Kanalservis", "list_static": list_static})
