from django.db import models
from django.contrib.auth.models import User

# Create your models here.
INTERVAL_CHOICES = (
    ('1m','1 Minuto'),
    ('2m','2 Minutos'),
    ('5m','5 Minutos'),
    ('15m','15 Minutos'),
    ('30m','30 Minutos'),
    ('60m','60 Minutos'),
    ('90m','90 Minutos'),
)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    interval = models.CharField(max_length=50, choices=INTERVAL_CHOICES)
    lower_limit = models.FloatField(default=0)
    upper_limit = models.FloatField(default=1000)

class Stock(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)  
    date = models.DateTimeField()
    open_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    close_price = models.FloatField()
    
    def __str__(self) -> str:
        return self.name
    
