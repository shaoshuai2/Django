from django.conf.urls import url

from user import views

urlpatterns = [
    url(r'',views.UsersView.as_view()),
]