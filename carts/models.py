from django.db import models
from users.models import User
from products.models import Product

# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User, null=True,blank=True, on_delete=models.CASCADE)#uno a muchos entre carrito con usuarios
    products = models.ManyToManyField(Product)#muchos a muchos entre carrito y productos
    subtotal = models.DecimalField(default=0.0,max_digits=8, decimal_places=2)
    total = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add = True)

    def __Str__(self):
        return ''
