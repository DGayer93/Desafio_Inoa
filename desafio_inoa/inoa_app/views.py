from django.shortcuts import render,redirect
from .models import Stock, Order
from .forms import UserRegistrationForm, OrderForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.urls import reverse_lazy,reverse
from django.contrib.auth.decorators import login_required
from .tasks import monitor_stock
from django.contrib import messages
# Create your views here.
class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    def get_success_url(self):
        user_id = self.request.user.id
        return reverse_lazy('visualizar', kwargs={'user_id': user_id})

def signup(request):
     if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  
     else:
        form = UserRegistrationForm()
     return render(request, 'accounts/signup.html', {'form': form})
def logout_view(request):
    logout(request)
    return redirect('login')
@login_required
def visualizar_ativos(request, user_id):
    order = Order.objects.filter(user_id=user_id)
    stocks = Stock.objects.filter(order__in=order)
    stocks = stocks.order_by('-date')
    return render(request, "inoa_app/visualization.html", {"stocks": stocks})

@login_required
def alertas(request, user_id):
    user_orders = Order.objects.filter(user_id=user_id)
    alerts = []
    for order in user_orders:
        stocks = Stock.objects.filter(order=order)
        for stock in stocks:
            if stock.close_price > order.upper_limit or stock.close_price < order.lower_limit:
                alerts.append(stock)
    alerts.reverse()
    return render(request, "inoa_app/alerts.html", {"user_id": user_id,'alerts':alerts})

@login_required
def registrar_ativo(request, user_id):
    user = request.user
    orders = Order.objects.filter(user_id=user_id)
    order_form = OrderForm()
    if request.method == "POST":
        order_form = OrderForm(request.POST)

        if order_form.is_valid():
            order_obj = order_form.save(commit=False)
            order_obj.user = user
            order_obj.save()
            monitor_stock(order_obj.id)
              
  
    return render(request, 'inoa_app/registrarativo.html', {'orders': orders, 'order_form': order_form})
@login_required
def editar_ativo(request,user_id,id):
    orders = Order.objects.filter(user_id=user_id)
    order_to_edit = orders.get(id=id)
    order_form = OrderForm(instance=order_to_edit)
    if request.method == "POST":
        order_to_edit = orders.get(id=id)
        order_form = OrderForm(request.POST,instance=order_to_edit)
        if order_form.is_valid():
            order_form.save()
            return redirect(reverse('registrar_ativo',args=[user_id]))
    return render(request,'inoa_app/edit.html',{'order_form':order_form})

@login_required
def deletar_ativo(request,user_id,id):
    orders = Order.objects.filter(user_id=user_id)
    if request.method =="POST":
       orders = orders.get(id=id)
       orders.delete()
    return redirect(reverse('registrar_ativo',args=[user_id]))