from django.conf.urls import url

from order import views

urlpatterns = [
    url(r'^user/$',views.UsersView.as_view()),
]