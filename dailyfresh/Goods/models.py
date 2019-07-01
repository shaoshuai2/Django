from django.db import models

# Create your models here.
class Goods(models.Model):
    goods_id = models.IntegerField(primary_key=True,auto_created=True)
    goods_name = models.CharField(max_length=64,unique=True,null=False,blank=False)
    goods_price = models.FloatField(null=False,blank=False)


    class Meta:
        db_table = 'goods'