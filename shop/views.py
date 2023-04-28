from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from .forms import *
from django.views.generic import CreateView, View, ListView, FormView
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
def getCategory():
    return Category.objects.all()
class HomeView(View):
    def get(self,req):
        data={
            "products":Product.objects.all(),
            "category":getCategory,
        }
        return render(req,"home.html",data)

class PublicView(CreateView):
    model=User
    form_class= PublicCreateFrom
    template_name="Form/singup.html"
    success_url="/"
    def get_context_data(self,**kwargs):
        kwargs['user_type']="Public"
        return super().get_context_data(**kwargs)
    def form_valid(self,form):
        user = form.save()
        login(self.request,user)
        return redirect("home")

class PrivateView(CreateView):
    model=User
    form_class=PrivateCreateForm
    template_name="Form/singup.html"
    success_url="/"
    def get_context_data(self,**kwargs):
        kwargs['user_type']="Private"
        return super().get_context_data(**kwargs)
    def form_valid(self,form):
        user=form.save()
        login(self.request,user)
        return redirect("home")

class LoginView(FormView):
    template_name="Form/login.html"
    form_class=AuthenticationForm
    success_url="/"
    def post(self,request):
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                back=request.GET.get("next","/")
                return redirect(back)
            else:
                return HttpResponse("Inactivated")
        else:
            return HttpResponse("login cheeking is failed")

class LogoutView(View):
    def get(self,req):
        logout(req)
        return redirect("login_user")
    
def filterProduct(req,slug):
    data = {}
    data['category'] = getCategory()
    data['products'] = Product.objects.filter(p_category__slug=slug)
    return render(req, "home.html", data)

def search(req):
    data = {}
    data['category'] = getCategory()
    data['products'] = Product.objects.filter(p_name__icontains=req.GET.get('search'))
    return render(req,"home.html",data)

def viewProduct(r, slug):
    data = {}
    data['category']  = getCategory()
    data['product'] = Product.objects.get(slug=slug)
    return render(r, "singleView.html", data)
@login_required()
def addToCard(req,slug):
    product=get_object_or_404(Product,slug=slug)
    order_item,created=OrderItem.objects.get_or_create(user=req.user,ordered=False,item=product)
    order_qs=Order.objects.filter(user=req.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # order is exist
        if(order.items.filter(item__slug=slug).exists()):
            order_item.qty +=1
            order_item.save()
        else:
            order.items.add(order_item)
        return redirect(myCart)
    else:
        # new order
            order = Order.objects.create(user=req.user)
            order.items.add(order_item)
            return redirect(myCart)
@login_required()
def removeToCart(req,slug):
    product=get_object_or_404(Product,slug=slug)
    order=Order.objects.get(user=req.user,ordered=False)
    order_item=OrderItem.objects.get(user=req.user,ordered=False,item=product)
    if order:
        if(order.items.filter(item__slug=slug).exists()):
            if order_item.qty<=1:
                order_item.delete()
            else:
                order_item.qty-=1
                order_item.save()
        return redirect(myCart)
@login_required()
def myCart(r):
    data = {} 
    data['order'] = Order.objects.filter(user=r.user,ordered=False)
    return render(r, "cart.html",data)
