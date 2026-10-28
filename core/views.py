from django.shortcuts import get_object_or_404, render,redirect
from django.views.generic import ListView
from django.core.paginator import Paginator
from .forms import CreateElementForm
from django.http import HttpResponseRedirect
from django.utils.text import slugify
from django.http import JsonResponse

from .models import Element,Type,Category

# Create your views here.
def index(request):
    return render(request, "core/index.html")

# vista que muestra detalles de productos
def detail(request,pk):
    element = get_object_or_404(Element, pk=pk)
    return render(request, "core/detail.html", {"element": element})

def sales(request):
    return render(request, "core/sales.html")

def get_types(request):
    category_name = request.GET.get('category')
    try:
        category = Category.objects.get(name=category_name)
        types = list(Type.objects.filter(category=category).values_list('name', flat=True))
    except Category.DoesNotExist:
        types = []

    return JsonResponse(types, safe=False)

def inventory(request):
    elements = Element.objects.all().order_by('-id')

    paginator = Paginator(elements, 10)
    page_number = request.GET.get('page')
    elements_page = paginator.get_page(page_number)

    return render(request, "core/inventory.html", {"elements": elements_page})

# agregar productos al inventario
def create_element(request):
    if request.method == "POST":
        form = CreateElementForm(request.POST)

        if form.is_valid():
            category_name = form.cleaned_data.pop("category").strip()
            type_name = form.cleaned_data.pop("type").strip()

            category, _ = Category.objects.get_or_create(name=category_name, defaults={"slug": slugify(category_name)})
            type_obj, _ = Type.objects.get_or_create(
                name=type_name,
                category=category,
                defaults={"slug": f"{category.slug}-{slugify(type_name)}"},
            )
            element = form.save(commit=False)

            element.category = category
            element.type = type_obj

            element.slug = slugify(element.name)

            element.save()

            return redirect("inventory")
        else:
            print(form.errors)

    else:
        form = CreateElementForm()

    context = {"form": form,"categories": Category.objects.all(),"types": Type.objects.all(),}

    return render(request,"core/create_product.html",context)

    