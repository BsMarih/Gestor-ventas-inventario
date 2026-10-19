from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "core/index.html")

def sales(request):
    return render(request, "core/sales.html")

def inventory(request):
    return render(request, "core/inventory.html")

