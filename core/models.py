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

    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=False,blank=False)

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

    description = models.TextField(blank=True)
    content=models.TextField(blank=True)
    price = models.PositiveIntegerField(default=0)
    quantity= models.PositiveIntegerField(default=0)
    min_quantity= models.PositiveIntegerField(default=0)
    available= models.BooleanField(default=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    type= models.ForeignKey(Type, on_delete=models.CASCADE)
    distributor = models.ForeignKey(Distributor, on_delete=models.CASCADE,default="",blank=True, null=True)
    prod_website = models.URLField(max_length=255, default='', blank=True, null=True)
    created= models.DateTimeField(auto_now_add=True)
    updated= models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.quantity == 0:
            self.available = False
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Sale(models.Model):
    date = models.DateField()
    element = models.ForeignKey(Element, on_delete=models.CASCADE, related_name="sales")
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"Venta #{self.pk}"
