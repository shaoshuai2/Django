from django.conf.urls import url

from goods import views

urlpatterns = [
    url(r'',views.HomeView.as_view()),
]


