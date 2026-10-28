from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Type(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Distributor(models.Model):
    name = models.CharField(max_length=255)
    number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    

    class Meta:
        verbose_name = "Distributor"
        verbose_name_plural = "Distributors"

    def __str__(self):
        return self.name

class Element(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    description = models.TextField()
    content=models.TextField()
    price= models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quantity= models.IntegerField(default=0)
    min_quantity= models.IntegerField(default=0)
    available= models.BooleanField(default=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    type= models.ForeignKey(Type, on_delete=models.CASCADE)
    distributor = models.ForeignKey(Distributor, on_delete=models.CASCADE,default="",blank=True, null=True)
    prod_website = models.URLField(max_length=255, default='', blank=True, null=True)
    created= models.DateTimeField(auto_now_add=True)
    updated= models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return self.name

