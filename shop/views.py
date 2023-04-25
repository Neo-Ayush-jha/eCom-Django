from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from .forms import *
from django.views.generic import CreateView, View, ListView, FormView
from django.contrib.auth import login,authenticate,logout

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