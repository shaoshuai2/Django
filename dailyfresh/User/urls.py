from django.conf.urls import url

from User import views

urlpatterns = [
    url(r'^$',views.index)
]