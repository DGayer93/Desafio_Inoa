from celery import shared_task
from .utils import fetch_stock_data,convert_minutes_to_seconds,send_alert
from .models import Order
from django.core.mail import send_mail


def import_django_instance():
    import django
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'desafio_inoa.settings')
    django.setup()
@shared_task
def monitor_stock(order_id):
    order_obj = Order.objects.get(pk=order_id)
    stock = fetch_stock_data(order_obj.id)
    interval = convert_minutes_to_seconds(order_obj.interval)
    if stock.close_price > order_obj.upper_limit:
        send_mail(f"Alerta de preço para {stock.name} (Venda)",
              f"{stock.name} passou do limite superior de {order_obj.upper_limit}, "
              f"seu valor agora é {stock.close_price}",
              "teste@gmail.com",
              [order_obj.user.email])
    elif stock.close_price < order_obj.lower_limit:
        send_mail(f"Alerta de preço para {stock.name} (Compra)",
              f"{stock.name} passou do limite inferior de {order_obj.lower_limit}, "
              f"seu valor agora é {stock.close_price}",
              "teste@gmail.com",
              [order_obj.user.email])
    
    monitor_stock.apply_async((order_id,),countdown=interval)


