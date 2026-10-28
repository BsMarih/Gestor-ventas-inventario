from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.core.paginator import Paginator
from .forms import CreateElementForm
from django.http import HttpResponseRedirect

from .models import Element

# Create your views here.
def index(request):
    return render(request, "core/index.html")

def detail(request,pk):
    element = get_object_or_404(Element, pk=pk)
    return render(request, "core/detail.html", {"element": element})

def sales(request):
    return render(request, "core/sales.html")

def inventory(request):
    elements = Element.objects.all()
    paginator = Paginator(elements, 1)  
    page_number = request.GET.get('page')
    return render(request, "core/inventory.html", {"elements": paginator.get_page(page_number)})

def create_element(request):
    form = CreateElementForm()
    return render(request, "core/create_product.html", {"form": form})
