from django.conf.urls import url

from Goods import views

urlpatterns = [
    url(r'^$',views.index1)
]