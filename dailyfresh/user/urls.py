from django.conf.urls import url

from user import views

urlpatterns = [
    url(r'^user/$',views.UsersView.as_view()),
]