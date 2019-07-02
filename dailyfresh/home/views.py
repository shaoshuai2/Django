from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


class HomeView(GenericAPIView):
    def get(self,request):
        data = {
            "status":HTTP_200_OK,
            "msg":"ok",
            "data":"xxx",
        }
        return Response(data)
        # return render(request, "../static/html/home.html", locals())


