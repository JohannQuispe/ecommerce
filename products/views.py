from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Product
from django.db.models import Q

# Create your views here.
class ProductListView(ListView):
    template_name='index.html'
    queryset=Product.objects.all().order_by('-id')
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message']='Lista de Productos'
        return context
class ProductDetailView(DetailView):#id->PK
    model=Product
    template_name='products/product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print('/n')
        print(context)
        print('/n')
        return context

class ProductSearchListView(ListView):
    template_name='products/search.html'
    def get_queryset(self):
        filters = Q(tittle__icontains=self.query())|Q(category__tittle__icontains=self.query())
        return Product.objects.filter(filters)
    def query(self):
        return self.request.GET.get('q')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query']=self.query()
        context['count']= context['product_list'].count()

        return context
